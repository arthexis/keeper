import logging

from django.views.generic import FormView
from django.urls import reverse_lazy

from orgs.forms import PasswordRecoveryForm
from orgs.models import Profile

logger = logging.getLogger(__name__)

__all__ = (
    'RequestPasswordRecovery',
)


class RequestPasswordRecovery(FormView):
    template_name = 'orgs/recovery.html'
    form_class = PasswordRecoveryForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)
        email = form.cleaned_data.get('email')
        try:
            profile = Profile.objects.get(email=email)
            profile.send_recovery_email()
        except Profile.DoesNotExist:
            logger.warning(f"Recovery: No profile with email={email}")
            pass
        return response
