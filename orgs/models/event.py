import logging

from django.db.models import *
from django.utils import timezone

from .org import Organization

logger = logging.getLogger(__name__)

__all__ = (
    'Event',
    'UpcomingEvent',
)


# Organizations can create events in the event calendar
class Event(Model):
    name = CharField(max_length=40)
    organization = ForeignKey(
        Organization, CASCADE, null=True, related_name='events', editable=False)
    event_date = DateField(null=True, blank=True)
    information = TextField(
        blank=True,
        help_text='Optional. Basic summary about the event.')
    external_url = URLField(
        null=True, blank=True,
        help_text='Optional. External link containing additional information.')
    is_public = BooleanField(default=False)
    is_published = BooleanField(default=True)

    def __str__(self):
        return self.name

    def is_upcoming(self):
        return self.event_date >= timezone.now().date()

    is_upcoming.boolean = True

    class Meta:
        ordering = ('-event_date',)


class UpcomingEventManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            event_date__gte=timezone.now().date())


class UpcomingEvent(Event):
    upcoming = UpcomingEventManager()

    class Meta:
        proxy = True

