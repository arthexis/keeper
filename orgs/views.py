from django.views.generic import \
    TemplateView, CreateView, FormView, RedirectView, UpdateView, DetailView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from orgs.models import *
from orgs.forms import *
from django.core.urlresolvers import reverse_lazy, reverse
from django.http.response import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User

import logging
logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = 'orgs/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if not user.is_authenticated:
            context['form'] = AuthenticationForm()
        else:
            try:
                context['profile'] = Profile.objects.get(user=user)
            except Profile.DoesNotExist:
                logger.error(f"User <{user}> is missing a Profile object.")
                context['profile'] = None
            context['req_member_form'] = RequestMembershipForm(request=self.request)
        return context


class PendingView(TemplateView):
    template_name = 'orgs/pending.html'


class VerificationView(TemplateView):
    template_name = 'orgs/verification.html'

    def dispatch(self, request, *args, pk=None, code=None, **kwargs):
        profile = get_object_or_404(Profile, pk=pk, verification_code=code)
        profile.is_verified = True
        profile.verification_code = None
        profile.code_sent_on = None
        profile.save()
        return super().dispatch(request, *args, **kwargs)


class RegistrationView(CreateView):
    template_name = 'orgs/register.html'
    form_class = RegistrationForm
    model = Profile
    success_url = reverse_lazy('orgs:pending')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        response = super().form_valid(form)
        profile = Profile.objects.get(username=username)
        profile.send_verification_email()
        return response


class LoginView(FormView):
    template_name = 'orgs/index.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('orgs:index')

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


class RequestPasswordRecoveryView(FormView):
    template_name = 'orgs/recovery.html'
    form_class = PasswordRecoveryForm
    success_url = reverse_lazy('orgs:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        email = form.cleaned_data.get('email')
        try:
            profile = Profile.objects.get(email=email)

        except Profile.DoesNotExist:
            logger.warning(f"Recovery: No profile found with email={email}")
            pass
        return response


class LogoutView(RedirectView):
    url = reverse_lazy('orgs:index')

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)


class EditProfileView(UpdateView):
    template_name = 'orgs/profile.html'
    model = Profile
    fields = ("email", "first_name", "last_name", "phone", "information")
    model_name = "Profile"


class RedirectMyProfileView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        profile = Profile.objects.get(user=self.request.user)
        return reverse('orgs:edit-profile', kwargs={'pk': profile.pk})


# Base settings shared by CreateOrganizationView and EditOrganizationView
class OrganizationMixin(object):
    template_name = 'orgs/organization/change_form.html'
    model = Organization
    model_name = "Organization"
    fields = ("name", "parent_org", "information", "is_public")
    context_object_name = 'organization'

    def __init__(self):
        self.object = None
        self.user_membership = None

    def get_success_url(self):
        return reverse_lazy('orgs:view-organization', kwargs={'pk': self.object.pk})


class CreateOrganizationView(OrganizationMixin, CreateView):
    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        Membership.objects.create(
            user=self.request.user, organization=form.instance, is_active=True, is_officer=True, is_owner=True)
        logger.info(f"Creating new organization <{name}>.")
        messages.add_message(
            self.request, messages.SUCCESS,
            f"Organization {name} created successfully. You may change it again below.")
        return response


class EditOrganizationView(OrganizationMixin, UpdateView):
    def get_object(self, queryset=None):
        # Prevent non-officers from accessing this view
        obj = super().get_object(queryset)
        self.user_membership = obj.get_membership(self.request.user)
        if not self.user_membership or not self.user_membership.is_officer:
            return Http404()
        return obj


class DetailOrganizationView(OrganizationMixin, DetailView):
    template_name = 'orgs/organization/overview.html'

    def get_object(self, queryset=None):
        # Prevent blocked users from accessing this view
        obj = super().get_object(queryset)
        self.user_membership = obj.get_membership(self.request.user)
        if self.user_membership and self.user_membership.is_blocked:
            return Http404()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_membership"] = self.user_membership
        return context


class MembershipView(FormView):
    template_name = 'orgs/membership.html'
    success_url = reverse_lazy('orgs:index')

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_form(self, form_class=None):
        return RequestMembershipForm(self.request.POST, request=self.request)

    def form_valid(self, form):
        response = super().form_valid(form)
        org_pk = form.cleaned_data['organization']
        organization = get_object_or_404(Organization, pk=org_pk)
        membership, created = Membership.objects.get_or_create(
            user=self.request.user, organization=organization)
        if not created:
            messages.add_message(
                self.request, messages.INFO,
                f"You have already requested Membership on {organization.name}.")
            return HttpResponseRedirect(reverse('orgs:request-membership'))
        else:
            messages.add_message(
                self.request, messages.SUCCESS,
                f"Membership requested for {organization.name}. Pending organization approval.")
        return response


class CancelMembershipView(RedirectView):
    url = reverse_lazy('orgs:index')

    def dispatch(self, request, *args, pk=None, **kwargs):
        membership = get_object_or_404(Membership, pk=pk)
        user = self.request.user
        if not user.is_superuser or user != membership.user:
            logger.warning(f"Unauthorized cancel membership request {membership.pk} user={user}")
            return Http404()
        if not membership.is_active and not membership.is_blocked:
            logger.info(f"Cancelled membership request {membership.pk} user={user}")
            membership.delete()
        return super().dispatch(request, *args, **kwargs)


# Base settings shared by CreateOrganizationView and EditOrganizationView
class EventMixin(object):
    template_name = 'orgs/event/change_form.html'
    model = Event
    model_name = "Event"
    fields = ("name", "parent_org", "information", "is_public")
    context_object_name = 'organization'

    def __init__(self):
        self.object = None
        self.user_membership = None

    def get_success_url(self):
        return reverse_lazy('orgs:view-event', kwargs={'pk': self.object.pk})


class CreateEventView(CreateView):
    pass


class DetailEventView(DetailView):
    pass


__all__ = (
    'IndexView',
    'RegistrationView',
    'EditProfileView',
    'PendingView',
    'LoginView',
    'LogoutView',
    'VerificationView',
    'CreateOrganizationView',
    'EditOrganizationView',
    'DetailOrganizationView',
    'MembershipView',
    'RedirectMyProfileView',
    'CancelMembershipView',
    'RequestPasswordRecoveryView',
    'CreateEventView',
    'DetailEventView',
)
