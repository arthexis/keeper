import logging

from django.db.models import Manager, Model, CharField, ForeignKey, CASCADE, DateField, TextField, URLField, \
    BooleanField
from django.utils.timezone import now

from .org import Organization

logger = logging.getLogger(__name__)

__all__ = (
    'Event',
)


class UpcomingEventManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(event_date__gte=now().date())


# Organizations can create events in the event calendar
class Event(Model):
    name = CharField(max_length=100)
    organization = ForeignKey(
        Organization, CASCADE, null=True, related_name='events', editable=False)
    event_date = DateField(null=True, blank=True)
    information = TextField(
        blank=True,
        help_text='Optional. Basic summary about the event.')
    external_url = URLField(
        null=True, blank=True,
        help_text='Optional. External link containing additional information.')
    is_published = BooleanField(default=True)

    objects = Manager()
    upcoming = UpcomingEventManager()

    def __str__(self):
        return self.name

    def is_upcoming(self):
        return self.event_date >= now().date()

    is_upcoming.boolean = True

    class Meta:
        ordering = ('-event_date',)


