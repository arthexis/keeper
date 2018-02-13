import logging

from django.views.generic import *
from django.urls import reverse

from orgs.models import *

logger = logging.getLogger(__name__)


__all__ = (
    'EditProfile',
    'RedirectMyProfile',
)


class EditProfile(UpdateView):
    template_name = 'orgs/profile.html'
    model = Profile
    fields = ("email", "first_name", "last_name", "phone", "information")
    model_name = "Profile"


class RedirectMyProfile(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        profile = Profile.objects.get(user=self.request.user)
        return reverse('orgs:edit-profile', kwargs={'pk': profile.pk})




