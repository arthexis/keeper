from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import RequestCharacterForm


class RequestCharacter(FormView):
    form_class = RequestCharacterForm
    template_name = 'change_form.html'
    title = 'Request Character'
    submit_label = 'Submit Request'
    success_url = reverse_lazy('index')

    def get_form(self, form_class=None):
        return super().get_form(form_class)

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error processing your request.')
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, 'Your character request has been sent successfully.')
        return super().form_valid(form)
