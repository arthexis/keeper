from django.views.generic import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse_lazy, reverse
from django.http.response import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils.http import urlencode

from orgs.models import *
from orgs.forms import *

import logging
logger = logging.getLogger(__name__)


class Registration(CreateView):
    template_name = 'orgs/register.html'
    form_class = RegistrationForm
    model = Profile
    success_url = reverse_lazy('orgs:pending-verify')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        org_pk = self.request.GET.get('org', None)
        if org_pk:
            try:
                context["invite_org"] = Organization.objects.get(pk=org_pk)
            except Organization.DoesNotExist:
                logger.warning(f"User register with invalid org={org_pk}")
        return context

    def form_valid(self, form):
        username = form.cleaned_data['username']
        initial_org_pk = form.cleaned_data['initial_org_pk']
        response = super().form_valid(form)
        profile = Profile.objects.get(username=username)
        profile.initiate_verification()
        if initial_org_pk:
            try:
                initial_org = Organization.objects.get(pk=initial_org_pk)
                Membership.objects.create(
                    user=profile.user, organization=initial_org)
            except Organization.DoesNotExist:
                logger.warning(f"User join invalid org={initial_org_pk}")
        return response


class Login(FormView):
    template_name = 'index.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def form_invalid(self, form):
        username = form.cleaned_data['username']
        logger.warning(f"Failed login. username={username}.")
        return super().form_invalid(form)

    def form_valid(self, form):
        username = form.cleaned_data['username']
        response = super().form_valid(form)
        profile = Profile.objects.get(username=username)
        if profile.is_verified:
            login(self.request, form.user_cache)
            logger.info(f"Successful login. username={username}")
        else:
            return HttpResponseRedirect(reverse('orgs:pending'))
        return response


class RequestPasswordRecovery(FormView):
    template_name = 'orgs/recovery.html'
    form_class = PasswordRecoveryForm
    success_url = reverse_lazy('orgs:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        email = form.cleaned_data.get('email')
        try:
            profile = Profile.objects.get(email=email)
            profile.send_recovery_email()
        except Profile.DoesNotExist:
            logger.warning(f"Recovery: No profile found with email={email}")
            pass
        return response


class Logout(RedirectView):
    url = reverse_lazy('orgs:index')

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)


class EditProfile(UpdateView):
    template_name = 'orgs/profile.html'
    model = Profile
    fields = ("email", "first_name", "last_name", "phone", "information")
    model_name = "Profile"


class RedirectMyProfile(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        profile = Profile.objects.get(user=self.request.user)
        return reverse('orgs:edit-profile', kwargs={'pk': profile.pk})


# Class used to make sure certain Membership privileges are required
class MemberPermissionMixin(SingleObjectMixin, View):
    def __init__(self):
        self.user_membership = None
        super().__init__()

    def has_permission(self):
        return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_membership"] = self.user_membership
        if self.user_membership:
            context["user_organization"] = self.user_membership.organization
        return context

    def get_membership(self, obj):
        raise NotImplemented()

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not self.request.user.is_anonymous():
            self.user_membership = self.get_membership(obj)
        else:
            self.user_membership = None
        try:
            if not self.has_permission():
                return Http404()
        except AttributeError:
            return Http404()
        return obj


# Base settings shared by CreateOrganizationView and EditOrganizationView
class OrganizationMixin(object):
    template_name = 'orgs/organization/change_form.html'
    model = Organization
    model_name = "Organization"
    fields = ("name", "parent_org", "information", "is_public")
    context_object_name = 'organization'

    def __init__(self):
        self.object = None

    def get_success_url(self):
        return reverse_lazy(
            'orgs:view-organization', kwargs={'pk': self.object.pk})


class CreateOrganization(OrganizationMixin, CreateView):
    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        logger.info(f"Creating new organization <{name}>.")
        Membership.objects.create(
            user=self.request.user, organization=form.instance, title='Founder',
            is_active=True, is_officer=True, is_owner=True)
        messages.add_message(
            self.request, messages.SUCCESS,
            f"Organization {name} created. You may change it below.")
        return response


class OrgMemberPermMixin(MemberPermissionMixin):
    def get_membership(self, obj: Organization):
        return obj.get_membership(self.request.user)


class EditOrganization(OrganizationMixin, OrgMemberPermMixin, UpdateView):
    def has_permission(self):
        return self.user_membership.is_officer


class ViewOrganization(OrganizationMixin, OrgMemberPermMixin, DetailView):
    template_name = 'orgs/organization/overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = self.request.GET.get('tab', None)
        return context


class ViewMembership(FormView):
    template_name = 'orgs/membership.html'
    success_url = reverse_lazy('orgs:index')

    def form_invalid(self, form):
        return super().form_invalid(form)

    def form_valid(self, form):
        response = super().form_valid(form)
        org_pk = form.cleaned_data['organization']
        organization = get_object_or_404(Organization, pk=org_pk)
        membership, created = Membership.objects.get_or_create(
            user=self.request.user, organization=organization)
        name = organization.name
        if not created:
            messages.success(
                self.request, f"You have already requested to join {name}.")
            return HttpResponseRedirect(reverse('orgs:request-membership'))
        else:
            messages.success(
                self.request,
                "Membership requested. Pending organization approval.")
        return response

    def get_form(self, form_class=None):
        return RequestMembershipForm(self.request.POST, request=self.request)


class CancelMembership(RedirectView):
    url = reverse_lazy('orgs:index')

    def dispatch(self, request, *args, pk=None, **kwargs):
        membership = get_object_or_404(Membership, pk=pk)
        user = self.request.user
        if not user.is_superuser or user != membership.user:
            logger.warning(
                f"Unauthorized cancel membership {membership.pk} user={user}")
            return Http404()
        if not membership.is_active and not membership.is_blocked:
            logger.info(
                f"Cancel membership request {membership.pk} user={user}")
            membership.delete()
        return super().dispatch(request, *args, **kwargs)


# Base settings shared by CreateOrganizationView and EditOrganizationView
class EventMixin(object):
    template_name = 'orgs/event/change_form.html'
    model = Event
    model_name = "Event"
    context_object_name = 'event'
    form_class = EventForm

    def __init__(self):
        self.object = None
        self.organization = None
        self.user_membership = None

    def get_success_url(self):
        return reverse('orgs:view-event', kwargs={'pk': self.object.pk})


class CreateEvent(EventMixin, MemberPermissionMixin, CreateView):

    def dispatch(self, request, *args, org_pk=None, **kwargs):
        self.organization = get_object_or_404(Organization, pk=org_pk)
        self.user_membership = \
            self.organization.get_membership(self.request.user)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if not self.user_membership.is_officer:
            return HttpResponse(status=403)  # Forbidden
        form.instance.organization = self.organization
        response = super().form_valid(form)
        messages.success(
            self.request, 'Event created. Now viewing your new event.')
        return response


class EventMemberPermissionMixin(MemberPermissionMixin):
    def get_membership(self, obj: Event):
        return obj.organization.get_membership(self.request.user)


class ViewEvent(EventMixin, EventMemberPermissionMixin, DetailView):
    template_name = 'orgs/event/overview.html'


class EditEvent(EventMixin, UpdateView):
    def has_permission(self):
        return self.user_membership.is_officer

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, 'Event updated. Now showing the modified event..')
        return response


class DeleteEvent(EventMixin, RedirectView):

    def has_permission(self):
        return self.user_membership.is_officer

    def get_redirect_url(self, *args, **kwargs):
        event = get_object_or_404(Event, pk=self.kwargs['pk'])
        organization = event.organization
        event.delete()
        messages.success(self.request, 'The event has been deleted.')
        return reverse(
            'orgs:view-organization',
            kwargs={'pk': organization.pk}) + '?' + urlencode({'tab': 'events'})


class MyCalendar(TemplateView):
    template_name = 'orgs/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = profile = \
            Profile.objects.get(user=self.request.user)
        context['upcoming_events'] = profile.upcoming_events()
        context['full_calendar'] = True
        return context


class PendingVerify(TemplateView):
    template_name = "orgs/pending-verify.html"

