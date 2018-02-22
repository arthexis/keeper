import logging

from django.db import IntegrityError
from django.views.generic import UpdateView

from orgs.models import Profile

logger = logging.getLogger(__name__)


__all__ = (
    'EditProfile',
)


class EditProfile(UpdateView):
    template_name = 'change_form.html'
    model = Profile
    fields = (
        "username", "email",
        "first_name", "last_name", "phone", "information"
    )
    model_name = "Profile"

    def get_object(self, queryset=None):
        try:
            profile, created = Profile.objects.get_or_create(user=self.request.user)
        except IntegrityError:
            profile = None
        return profile


