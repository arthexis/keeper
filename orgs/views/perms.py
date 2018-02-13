import logging

from django.views import View
from django.http.response import Http404
from django.views.generic.detail import SingleObjectMixin

from orgs.models import Event, Organization

logger = logging.getLogger(__name__)

__all__ = (
    'MemberPermission',
    'EventMemberPermission',
    'OrgMemberPermission',
)


# Class used to make sure certain Membership privileges are required
class MemberPermission(SingleObjectMixin, View):
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
        if not self.request.user.is_anonymous:
            self.user_membership = self.get_membership(obj)
        else:
            self.user_membership = None
        try:
            if not self.has_permission():
                return Http404()
        except AttributeError:
            return Http404()
        return obj


class EventMemberPermission(MemberPermission):
    def get_membership(self, obj: Event):
        return obj.organization.get_membership(self.request.user)


class OrgMemberPermission(MemberPermission):
    def get_membership(self, obj: Organization):
        return obj.get_membership(self.request.user)

