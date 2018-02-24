from django.contrib import messages
from django.views.generic import FormView

from .forms import RequestCharacterForm


class RequestCharacter(FormView):
    form_class = RequestCharacterForm
    template_name = 'change_form.html'
    title = 'Request Character'
    submit_label = 'Submit Request'

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error processing your request.')
        return super().form_invalid(form)

    def form_valid(self, form):
        return super().form_valid(form)
