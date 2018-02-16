import logging

from django.db.models import ForeignKey, CharField, BooleanField, CASCADE
from django.contrib.auth.models import User
from model_utils.models import TimeStampedModel

from .org import Organization

logger = logging.getLogger(__name__)

__all__ = (
    'Membership',
)


# Membership is a relation between Users and Organizations
class Membership(TimeStampedModel):
    user = ForeignKey(User, CASCADE, related_name="memberships")
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
