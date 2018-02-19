import logging

from django.db.models import CharField, ForeignKey, TextField, SlugField, CASCADE, Manager, Model
from model_utils import Choices
logger = logging.getLogger(__name__)

__all__ = (
    'Organization',
    'Region',
)


class Region(Model):
    name = CharField(max_length=100, unique=True, help_text='Required, must be unique.')
    reference_code = SlugField('Code', unique=True)

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.reference_code)


class Organization(Model):

    MEMBERSHIP_MODES = Choices(
        ('direct', 'Direct Memberships'),
        ('inherit', 'Inherit Memberships')
    )

    name = CharField(
        max_length=200, help_text="Required. Orgs in a region cannot share names.")
    region = ForeignKey(
        Region, CASCADE, related_name='organizations',
        help_text="Required. Region where the organization operates.")
    information = TextField(
        blank=True,
        help_text="Information about your organization.")
    reference_code = SlugField(
        'URL Prefix', unique=True,
        help_text='Required. Must be unique across all organizations.')

    # Managers
    objects = Manager()

    class Meta:
        unique_together = ('name', 'region')
        verbose_name = 'Organization'

    def __str__(self):
        return f'{self.name} ({self.region})'

    def get_membership(self, user):
        return self.memberships.get(user=user)

    def upcoming_events(self):
        from .event import UpcomingEvent
        return UpcomingEvent.objects.filter(organization=self)



