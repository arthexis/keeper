import logging

from django.db.models import Model, ForeignKey, CASCADE, CharField, TextField

from orgs.models import Event
from sheets.models import Character

logger = logging.getLogger(__name__)


class DowntimeAction(Model):
    character = ForeignKey(Character, CASCADE, related_name='downtime_actions')
    target_event = ForeignKey(Event, CASCADE, related_name='downtime_actions')
    description = TextField()


