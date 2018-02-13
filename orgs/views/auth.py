import logging

from django.views.generic import FormView, RedirectView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse_lazy, reverse
from django.http.response import HttpResponseRedirect

from orgs.forms import PasswordRecoveryForm
from orgs.models import Profile

logger = logging.getLogger(__name__)

__all__ = (
    'Login',
    'Logout',
    'RequestPasswordRecovery',
)


class Login(FormView):
    template_name = 'index.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def form_invalid(self, form):
        username = form.cleaned_data['username']
        logger.warning(f"Failed login. username={username}.")
        return super().form_invalid(form)

    def form_valid(self, form):
        username = form.cleaned_data['username']
        profile = Profile.objects.get(username=username)
        if profile.is_verified:
            login(self.request, form.user_cache)
            logger.info(f"Successful login. username={username}")
            return super().form_valid(form)
        else:
            return HttpResponseRedirect(reverse('orgs:pending-verify'))


class Logout(RedirectView):
    url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)


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
