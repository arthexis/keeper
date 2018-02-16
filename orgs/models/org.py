import logging

from django.db.models import CharField, ForeignKey, TextField, BooleanField, SlugField, SET_NULL
from model_utils.managers import QueryManager
from model_utils.models import TimeStampedModel

logger = logging.getLogger(__name__)

__all__ = (
    'Organization',
)


# Users can create Organizations
class Organization(TimeStampedModel):
    name = CharField(
        max_length=200, unique=True,
        help_text="Required. Must be unique across all Organizations.")
    parent_org = ForeignKey(
        'Organization', SET_NULL, verbose_name="Parent Organization",
        blank=True, null=True,
        help_text="Optional. If set, you will inherit settings and staff.")
    information = TextField(
        blank=True,
        help_text="Information about your organization. If you set this Organization to be "
        "public, everyone will be able to see this information.")
    is_public = BooleanField(
        default=True, verbose_name="Open to the Public",
        help_text="Allow finding the organization and requesting membership.")

    reference_code = SlugField('URL Prefix', unique=True)

    public = QueryManager(is_public=True)

    def __str__(self):
        return self.name

    def get_membership(self, user):
        return self.memberships.get(user=user)

    def upcoming_events(self):
        from .event import UpcomingEvent
        return UpcomingEvent.objects.filter(organization=self)



