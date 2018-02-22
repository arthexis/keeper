import logging

from django.db.models import ForeignKey, CharField, BooleanField, IntegerField, CASCADE, SET_NULL, Manager
from django.conf import settings
from model_utils import Choices
from model_utils.managers import QueryManager
from model_utils.models import TimeStampedModel, StatusModel

from .org import Organization

logger = logging.getLogger(__name__)

__all__ = (
    'Membership',
    'Prestige',
)


# Membership is a relation between Users and Organizations
class Membership(TimeStampedModel, StatusModel):
    STATUS = Choices(
        ('active', 'Active'),
        ('suspended', 'Suspended')
    )
    TITLES = Choices(
        ('storyteller', 'Storyteller'),
        ('coordinator', 'Coordinator')
    )

    user = ForeignKey(settings.AUTH_USER_MODEL, CASCADE, related_name="memberships")
    organization = ForeignKey(Organization, CASCADE, related_name="memberships")
    title = CharField(max_length=20, choices=TITLES, blank=True)
    external_id = CharField(max_length=20, blank=True)

    objects = Manager()
    storytellers = QueryManager(title='storyteller')
    coordinators = QueryManager(title='coordinator')

    class Meta:
        unique_together = ('user', 'organization',)
        ordering = ('organization__name', 'user__username')

    def __str__(self):
        return f'{self.pk}'


class Prestige(TimeStampedModel):
    membership = ForeignKey('Membership', CASCADE, related_name='prestige')
    amount = IntegerField()
    notes = CharField(max_length=2000)
    witness = ForeignKey(settings.AUTH_USER_MODEL, SET_NULL, null=True, related_name='+')

    class Meta:
        verbose_name = 'Prestige Record'
