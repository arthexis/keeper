import logging

from django.views.generic import TemplateView
from orgs.models import Profile

logger = logging.getLogger(__name__)

__all__ = (
    'MyCalendar',
)


class MyCalendar(TemplateView):
    template_name = 'orgs/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = profile = \
            Profile.objects.get(user=self.request.user)
        context['upcoming_events'] = profile.upcoming_events()
        context['full_calendar'] = True
        return context

