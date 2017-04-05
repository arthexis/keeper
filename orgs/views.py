from django.views.generic import TemplateView, CreateView, DetailView, FormView, RedirectView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from orgs.models import *
from orgs.forms import *
from django.core.urlresolvers import reverse_lazy, reverse
from django.http.response import HttpResponseRedirect


import logging
logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = 'orgs/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if not user.is_authenticated:
            context['form'] = AuthenticationForm()
        else:
            try:
                context['profile'] = Profile.objects.get(user=user)
            except Profile.DoesNotExist:
                logger.error(f"User <{user}> is missing a Profile object.")
                context['profile'] = None
        return context


class PendingView(TemplateView):
    template_name = 'orgs/pending.html'


class RegistrationView(CreateView):
    template_name = 'orgs/register.html'
    form_class = RegistrationForm
    model = Profile
    success_url = reverse_lazy('orgs:pending')


class LoginView(FormView):
    template_name = 'orgs/index.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('orgs:index')

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
        else:
            return HttpResponseRedirect(reverse('orgs:pending'))
        return super().form_valid(form)


class LogoutView(RedirectView):
    url = reverse_lazy('orgs:index')

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)


class ProfileDetailView(DetailView):
    template_name = 'orgs/profile.html'
    model = Profile


__all__ = (
    'IndexView',
    'RegistrationView',
    'ProfileDetailView',
    'PendingView',
    'LoginView',
    'LogoutView',
)
