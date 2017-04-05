from django.views.generic import TemplateView, CreateView, DetailView
from django.contrib.auth.forms import AuthenticationForm
from orgs.models import *
from orgs.forms import *
from django.core.urlresolvers import reverse_lazy


class IndexView(TemplateView):
    template_name = 'orgs/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            context['login_form'] = AuthenticationForm()
        return context


class PendingView(TemplateView):
    template_name = 'orgs/pending.html'


class RegistrationView(CreateView):
    template_name = 'orgs/register.html'
    form_class = RegistrationForm
    model = Profile
    success_url = reverse_lazy('orgs:pending')


class ProfileDetailView(DetailView):
    template_name = 'orgs/profile.html'
    model = Profile


__all__ = ('IndexView', 'RegistrationView', 'ProfileDetailView', 'PendingView')
