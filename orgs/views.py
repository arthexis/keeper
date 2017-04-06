from django.views.generic import \
    TemplateView, CreateView, FormView, RedirectView, UpdateView, DetailView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from orgs.models import *
from orgs.forms import *
from django.core.urlresolvers import reverse_lazy, reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib import messages

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
            context['req_member_form'] = RequestMembershipForm()
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


class LogoutView(RedirectView):
    url = reverse_lazy('orgs:index')

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)


class EditProfileView(UpdateView):
    template_name = 'orgs/profile.html'
    model = Profile
    fields = ("email", "phone",)
    model_name = "Profile"


class RedirectMyProfileView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        profile = Profile.objects.get(user=self.request.user)
        return reverse('orgs:profile', kwargs={'pk': profile.pk})


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
        return reverse_lazy('orgs:organization', kwargs={'pk': self.object.pk})


class CreateOrganizationView(OrganizationMixin, CreateView):
    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        response = super().form_valid(form)
        logger.info(f"Creating new organization <{name}>.")
        messages.add_message(
            self.request, messages.SUCCESS,
            f"Organization {name} created successfully. You may change it again below.")
        return response


class EditOrganizationView(OrganizationMixin, UpdateView):
    pass


class DetailOrganizationView(OrganizationMixin, DetailView):
    template_name = 'orgs/organization/details.html'


class MembershipView(FormView):
    form_class = RequestMembershipForm
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
        if not created:
            messages.add_message(
                self.request, messages.INFO,
                f"You have already requested Membership on {organization.name}.")
            return HttpResponseRedirect(reverse('orgs:membership'))
        else:
            messages.add_message(
                self.request, messages.SUCCESS,
                f"Membership requested for {organization.name}. Pending organization approval.")
        return response


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
)
