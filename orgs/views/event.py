import logging

from django.views.generic import CreateView, DetailView, UpdateView, RedirectView
from django.urls import reverse
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils.http import urlencode

from orgs.models import Event, Organization
from orgs.forms import EventForm
from .perms import MemberPermission, EventMemberPermission

logger = logging.getLogger(__name__)

__all__ = (
    'CreateEvent',
    'DeleteEvent',
    'EditEvent',
    'ViewEvent',
)


# Base settings shared by CreateOrganizationView and EditOrganizationView
class _EventMixin(object):
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


class CreateEvent(_EventMixin, MemberPermission, CreateView):

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


class EditEvent(_EventMixin, UpdateView):
    def has_permission(self):
        return self.user_membership.is_officer

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, 'Event updated. Now showing the modified event..')
        return response


class DeleteEvent(_EventMixin, RedirectView):

    def has_permission(self):
        return self.user_membership.is_officer

    def get_redirect_url(self, *args, **kwargs):
        event = get_object_or_404(Event, pk=self.kwargs['pk'])
        organization = event.organization
        event.delete()
        messages.success(self.request, 'The event has been deleted.')
        return reverse('orgs:view-org', kwargs={'pk': organization.pk}) + '?' + urlencode({'tab': 'events'})


class ViewEvent(_EventMixin, EventMemberPermission, DetailView):
    template_name = 'orgs/event/overview.html'

