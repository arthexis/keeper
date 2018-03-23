import logging

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, DeleteView, DetailView

from .models import Character, ApprovalRequest
from organization.models import Chronicle
from .forms import RequestCharacterForm

logger = logging.getLogger(__name__)

__all__ = (
    'RequestCharacter',
    'DownloadAttachment',
)


class RequestCharacter(FormView):
    form_class = RequestCharacterForm
    template_name = 'change_form.html'
    title = 'Request Character'
    submit_label = 'Submit Request'
    success_url = reverse_lazy('index')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chronicle = None

    def dispatch(self, request, *args, **kwargs):
        self.chronicle = get_object_or_404(Chronicle, pk=kwargs.get('chronicle'))
        if not self.chronicle.is_member(request.user):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error processing your request.')
        return super().form_invalid(form)

    def form_valid(self, form):
        try:
            Character.request_initial_approval(
                user=self.request.user,
                chronicle=self.chronicle,
                name=form.cleaned_data['character_name'],
                template=form.cleaned_data['character_template'],
                description=form.cleaned_data['description'],
                attachment=self.request.FILES['character_sheet_image'],
            )
        except RuntimeError:
            logger.exception('Error creating initial character request.')
        messages.success(self.request, 'Your character request has been sent successfully.')
        return super().form_valid(form)


class DownloadAttachment(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponse(status=403)
        approval = get_object_or_404(ApprovalRequest, pk=kwargs['approval'])
        response = HttpResponse(content_type=approval.attachment_content_type)
        response['Content-Disposition'] = f'attachment; filename={approval.attachment_filename}'
        response.write(approval.attachment)
        return response


class CharacterDetail(DetailView):
    model = Character
    template_name = 'sheets/character_detail.html'
    context_object_name = 'character'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['five'] = range(5)
        context['ten'] = range(10)
        return context



