import logging

from django.db.models import CharField, ForeignKey, TextField, BooleanField, SlugField, CASCADE, Manager, Model
from model_utils import Choices
from model_utils.managers import QueryManager
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


class Organization(Model):

    MEMBERSHIP_MODES = Choices(
        ('direct', 'Direct Memberships'),
        ('inherit', 'Inherit Memberships')
    )

    name = CharField(
        max_length=200, help_text="Required. Two orgs in the same region cannot have the same name.")
    region = ForeignKey(
        Region, CASCADE, related_name='organizations',
        help_text="Required. Region where the organization operates.")
    information = TextField(
        blank=True,
        help_text="Information about your organization. If you set this Organization to be "
        "public, everyone will be able to see this information.")
    reference_code = SlugField('URL Prefix', unique=True)

    # Managers
    objects = Manager()

    class Meta:
        unique_together = ('name', 'region')

    def __str__(self):
        return f'{self.name} ({self.region})'

    def get_membership(self, user):
        return self.memberships.get(user=user)

    def upcoming_events(self):
        from .event import UpcomingEvent
        return UpcomingEvent.objects.filter(organization=self)



