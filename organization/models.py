import logging

from django.conf import settings
from django.db.models import CASCADE, CharField, ForeignKey, IntegerField, Manager, Model, SET_NULL, SlugField, \
    TextField
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
    information = TextField(blank=True)
    reference_code = SlugField('URL Prefix', unique=True, help_text='Required. Must be unique.')

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.name}'


class Chapter(Organization):

    # Chapters represent regional play organizations with multiple domains
    # Prestige is granted at Chapter level

    class Meta:
        verbose_name = 'Chapter'

    def get_membership(self, user):
        return self.memberships.get(user=user)


class Domain(Organization):

    # Domains represent one or more venues sharing the same fictional universe
    # Characters are approved at Domain level

    chapter = ForeignKey('Chapter', CASCADE, related_name='domains')

    class Meta:
        verbose_name = 'Domain'


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
        return f'#{self.external_id or self.pk}'


class Prestige(TimeStampedModel):
    membership = ForeignKey('Membership', CASCADE, related_name='prestige')
    amount = IntegerField()
    notes = CharField(max_length=2000)
    witness = ForeignKey(settings.AUTH_USER_MODEL, SET_NULL, null=True, related_name='+')

    class Meta:
        verbose_name = 'Prestige Record'


