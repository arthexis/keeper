import logging

from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy

from orgs.models import Organization, Profile, Membership
from orgs.forms import RegistrationForm

logger = logging.getLogger(__name__)

__all__ = (
    'Registration',
    'PendingVerify',
)


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


class PendingVerify(TemplateView):
    template_name = "orgs/pending-verify.html"


