from django.views.generic import FormView

from .forms import RequestForm


class RequestCharacter(FormView):
    form_class = RequestForm
    template_name = 'change_form.html'
    title = 'Request Character'
    submit_label = 'Submit Request'

    def form_valid(self, form):
        return super().form_valid(form)
