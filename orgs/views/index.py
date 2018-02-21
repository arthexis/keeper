import logging

from django.shortcuts import redirect
from django.views.generic import TemplateView

from orgs.models import Profile
from orgs.forms import RequestMembershipForm

logger = logging.getLogger(__name__)

__all__ = (
    'Index',
)


# The IndexView has been declared here to keep it separate from the rest
# This is because it doesn't belong to any specific application
class Index(TemplateView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account_login')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        try:
            context['profile'] = profile = Profile.objects.get(user=user)
            upcoming_events = profile.upcoming_events()
            context['upcoming_events'] = upcoming_events[:5]
            context['remaining_events'] = upcoming_events.count() - 5
        except Profile.DoesNotExist:
            logger.error(f"User <{user}> has no profile.")
            context['profile'] = None
        context['req_member_form'] = RequestMembershipForm(request=self.request)
        return context
