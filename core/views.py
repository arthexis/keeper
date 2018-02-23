import logging

from django.shortcuts import redirect
from django.views.generic import TemplateView, UpdateView

from .models import UserProfile

logger = logging.getLogger(__name__)

__all__ = (
    'Index',
    'EditMyProfile',
)


# The IndexView has been declared here to keep it separate from the rest
# This is because it doesn't belong to any specific application
class Index(TemplateView):
    template_name = 'index.html'
    title = "Dashboard"

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return redirect('account_login')
        return super().dispatch(request, *args, **kwargs)


class EditMyProfile(UpdateView):
    template_name = 'change_form.html'
    model = UserProfile
    fields = (
        "username", "email",
        "first_name", "last_name", "phone",
    )
    model_name = "Profile"

    def get_object(self, queryset=None):
        return self.request.user


