import logging

from django.views.generic import UpdateView
from django.conf import settings

logger = logging.getLogger(__name__)


__all__ = (
    'EditProfile',
)


class EditProfile(UpdateView):
    template_name = 'change_form.html'
    model = settings
    fields = (
        "username", "email",
        "first_name", "last_name", "phone", "information"
    )
    model_name = "Profile"

