import logging

from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models import CASCADE, CharField, ForeignKey, IntegerField, Manager, Model, SET_NULL, URLField, \
    DO_NOTHING, TextField
from django_extensions.db.fields import AutoSlugField
from model_utils import Choices
from model_utils.managers import QueryManager
from model_utils.models import StatusModel, TimeStampedModel

logger = logging.getLogger(__name__)

__all__ = (
    'Chapter',
    'Domain',
    'Membership',
    'Prestige',
)


class Organization(Model):
    name = CharField(
        max_length=200, help_text="Required. Must be unique.", unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.name}'


class Chapter(Organization):

    # Chapters represent regional play organizations with multiple domains
    # Prestige is granted at Chapter level

    site = ForeignKey(Site, DO_NOTHING, related_name='chapters', null=True)  # Django Site
    rules_url = URLField('Rules URL', blank=True, help_text='URL pointing to the Chapter rules document.')
    reference_code = AutoSlugField(populate_from='name')

    class Meta:
        verbose_name = 'Chapter'

    def get_membership(self, user):
        return self.memberships.get(user=user)


class Domain(Organization):

    # Domains represent one or more venues sharing the same fictional universe
    # Characters are approved at Domain level

    rules_url = URLField('Rules URL', blank=True, help_text='URL pointing to the Domain game and approval rules.')
    chapter = ForeignKey('Chapter', CASCADE, related_name='domains')
    reference_code = AutoSlugField(populate_from=('name', 'chapter__name'))

    class Meta:
        verbose_name = 'Domain'

    def __str__(self):
        return f'{self.name} ({self.chapter})'


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
    chapter = ForeignKey(Chapter, CASCADE, related_name="memberships")
    title = CharField(max_length=20, choices=TITLES, blank=True)
    external_id = CharField(max_length=20, blank=True)

    objects = Manager()
    storytellers = QueryManager(title='storyteller')
    coordinators = QueryManager(title='coordinator')

    class Meta:
        unique_together = ('user', 'chapter',)
        ordering = ('chapter__name', 'user__username')

    def __str__(self):
        return f'#{self.external_id or self.pk} {self.user}'


class PrestigeReport(TimeStampedModel):
    chapter = ForeignKey('Chapter', CASCADE, related_name='prestige')
    description = TextField()

    class Meta:
        verbose_name = 'Prestige Report'


class Prestige(Model):
    membership = ForeignKey('Membership', CASCADE, related_name='prestige')
    report = ForeignKey('PrestigeReport', CASCADE, related_name='lines')
    amount = IntegerField()
    notes = CharField(max_length=400, blank=True)

    class Meta:
        verbose_name = 'Prestige Line'

