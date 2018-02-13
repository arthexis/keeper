import logging

from django.views.generic import FormView, RedirectView
from django.urls import reverse_lazy, reverse
from django.http.response import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.contrib import messages

from orgs.models import Organization, Membership
from orgs.forms import RequestMembershipForm

logger = logging.getLogger(__name__)

__all__ = (
    'CancelMembership',
    'ViewMembership',
)


class ViewMembership(FormView):
    template_name = 'orgs/membership.html'
    success_url = reverse_lazy('index')

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
    url = reverse_lazy('index')

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
