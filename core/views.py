import logging

from django.contrib import messages
from django.db.models import F
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, UpdateView

from .models import UserProfile

logger = logging.getLogger(__name__)

__all__ = (
    'Index',
    'EditMyProfile',
    'UpdateAjax',
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
        else:
            context['pending_approvals'] = approvals.filter(status='pending')
        context['characters'] = characters = self.request.user.characters
        if characters.exists():
            context['approved_characters'] = characters.filter(status='approved')
        return context


class EditMyProfile(UpdateView):
    template_name = 'change_form.html'
    model = UserProfile
    fields = (
        "username", "email", "first_name", "last_name", "phone", "email_opt_out",
    )
    model_name = "Profile"
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Your profile has been updated successfully.')
        return super().form_valid(form)


class UpdateAjax(View):
    model = None
    owner_field = 'user'
    fields = []

    def dispatch(self, request, *args, **kwargs):
        if request.method != 'POST' or request.user.is_anonymous:
            return HttpResponse(status=401)
        pk = request.POST.get('pk', None) or request.POST.get('id')
        obj = get_object_or_404(self.model, pk=pk)
        owner = getattr(obj, self.owner_field, None)
        if owner and request.user != owner and not request.user.is_superuser:
            return HttpResponse(status=403)
        self.update(request, obj, request.POST)
        return HttpResponse()

    def update(self, request, obj, data):
        field = data.get('field')
        if field in self.fields:
            val = data.get('value')
            if getattr(obj, field) != val:
                setattr(obj, field, val)
                obj.save()
