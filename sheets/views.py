from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView

from .models import Character
from organization.models import Domain
from .forms import RequestCharacterForm


class RequestCharacter(FormView):
    form_class = RequestCharacterForm
    template_name = 'change_form.html'
    title = 'Request Character'
    submit_label = 'Submit Request'
    success_url = reverse_lazy('index')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.domain = None

    def dispatch(self, request, *args, **kwargs):
        self.domain = get_object_or_404(Domain, pk=kwargs.get('domain'))
        if not self.domain.is_member(request.user):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error processing your request.')
        return super().form_invalid(form)

    def form_valid(self, form):
        # Character.request_initial_approval()
        messages.success(self.request, 'Your character request has been sent successfully.')
        return super().form_valid(form)
