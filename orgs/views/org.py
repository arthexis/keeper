import logging

from django.views.generic import CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages

from orgs.models import Organization, Membership
from .perms import OrgMemberPermission

logger = logging.getLogger(__name__)

__all__ = (
    'CreateOrganization',
    'EditOrganization',
    'ViewOrganization',
)


# Base settings shared by CreateOrganizationView and EditOrganizationView
class _OrganizationMixin:
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


class CreateOrganization(_OrganizationMixin, CreateView):
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


class EditOrganization(_OrganizationMixin, OrgMemberPermission, UpdateView):
    def has_permission(self):
        return self.user_membership.is_officer


class ViewOrganization(_OrganizationMixin, OrgMemberPermission, DetailView):
    template_name = 'orgs/organization/overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = self.request.GET.get('tab', None)


