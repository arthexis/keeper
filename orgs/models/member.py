import logging

from django.db.models import ForeignKey, CharField, BooleanField, IntegerField, CASCADE, SET_NULL
from django.conf import settings
from model_utils.models import TimeStampedModel

from .org import Organization

logger = logging.getLogger(__name__)

__all__ = (
    'Membership',
    'Prestige',
)


# Membership is a relation between Users and Organizations
class Membership(TimeStampedModel):
    user = ForeignKey(settings.AUTH_USER_MODEL, CASCADE, related_name="memberships")
    organization = ForeignKey(Organization, CASCADE, related_name="memberships")
    title = CharField(max_length=200, blank=True)

    is_active = BooleanField(default=False)
    is_officer = BooleanField(default=False)
    is_owner = BooleanField(default=False)
    is_blocked = BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'organization',)
        ordering = ('organization__name',)

    def __str__(self):
        return f'{self.pk}'

    def description(self):
        if not self.is_active:
            if self.is_blocked:
                return 'Blocked'
            return 'Inactive'
        if self.is_officer:
            return 'Active Officer'
        return 'Active Member'


class Prestige(TimeStampedModel):
    membership = ForeignKey('Membership', CASCADE, related_name='prestige')
    amount = IntegerField()
    notes = CharField(max_length=2000)
    witness = ForeignKey(settings.AUTH_USER_MODEL, SET_NULL, null=True, related_name='+')

    class Meta:
        verbose_name = 'Prestige Record'
