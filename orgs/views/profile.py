import logging

from django.views.generic import UpdateView, RedirectView
from django.urls import reverse

from orgs.models import Profile

logger = logging.getLogger(__name__)


__all__ = (
    'EditProfile',
)


class EditProfile(UpdateView):
    template_name = 'profile.html'
    model = Profile
    fields = (
        "username", "email",
        "first_name", "last_name", "phone", "information"
    )
    model_name = "Profile"

    def get_object(self, queryset=None):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile


