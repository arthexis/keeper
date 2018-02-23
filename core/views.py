import logging

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['approvals'] = approvals = self.request.user.approval_requests
        if not approvals.exists():
            context['new_guide'] = True
        return context


class EditMyProfile(UpdateView):
    template_name = 'change_form.html'
    model = UserProfile
    fields = (
        "username", "email",
        "first_name", "last_name", "phone",
    )
    model_name = "Profile"
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Your profile has been updated successfully.')
        return super().form_valid(form)




