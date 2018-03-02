import logging

from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models import CASCADE, CharField, ForeignKey, Manager, Model, URLField, \
    DO_NOTHING, DateField, PositiveSmallIntegerField, PositiveIntegerField, SET_NULL, Sum, EmailField, BooleanField, \
    TextField, SlugField
from django.urls import reverse
from django.utils.html import format_html
from django_extensions.db.fields import AutoSlugField, RandomCharField
from model_utils import Choices
from model_utils.managers import QueryManager
from model_utils.models import StatusModel, TimeStampedModel, TimeFramedModel

logger = logging.getLogger(__name__)

__all__ = (
    'Organization',
    'Chronicle',
    'GameEvent',
    'ExperienceAward',
    'Membership',
    'Prestige',
    'PrestigeReport',
    'PrestigeLevel',
    'Invitation',
)


class BaseOrganization(Model):
    name = CharField(max_length=200, help_text="Required. Must be unique.", unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.name}'


class Organization(BaseOrganization):

    # organizations represent regional play organizations with multiple chronicles
    # Prestige is granted at organization level

    site = ForeignKey(Site, DO_NOTHING, related_name='organizations', null=True)  # Django Site
    rules_url = URLField('Rules URL', blank=True, help_text='URL pointing to the organization rules document.')
    reference_code = SlugField('Unique short name or acronym.')
    prestige_cutoff = DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'Organization'

    def get_membership(self, user):
        return self.memberships.get(user=user)


class Chronicle(BaseOrganization):

    # chronicles represent one or more venues sharing the same fictional universe
    # Characters are approved at chronicle level

    rules_url = URLField('Rules URL', blank=True, help_text='URL pointing to the chronicle game and approval rules.')
    organization = ForeignKey('Organization', CASCADE, related_name='chronicles')
    short_description = TextField(blank=True)
    reference_code = SlugField('Unique short name or acronym.')

    class Meta:
        verbose_name = 'Chronicle'

    def __str__(self):
        return f'{self.name} ({self.organization})'

    def name_and_chronicle(self):
        return str(self.name)

    def is_member(self, user):
        return Membership.objects.filter(organization=self.organization, user=user).exists()


class GameEvent(Model):
    chronicle = ForeignKey(Chronicle, CASCADE, related_name='game_events')
    event_date = DateField(null=True, blank=True)
    number = PositiveSmallIntegerField(null=True, blank=True, editable=False)
    title = CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ('number', 'chronicle')
        ordering = ('-event_date', )

    def __str__(self):
        return f'{self.chronicle.reference_code} {self.number}'

    def save(self, **kwargs):
        if not self.number:
            self.number = 1 + GameEvent.objects.filter(chronicle=self.chronicle).count()
        super().save(**kwargs)


class ExperienceAward(TimeStampedModel):
    game_event = ForeignKey(GameEvent, CASCADE, related_name='experience_awards')
    character = ForeignKey('sheets.Character', CASCADE, related_name='experience_awards')
    experience = PositiveSmallIntegerField(default=0)
    beats = PositiveSmallIntegerField(default=0)
    notes = CharField(max_length=400, blank=True)

    def __str__(self):
        return f'{self.character.name}'


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
    external_id = CharField(max_length=20, blank=True, verbose_name='External ID')

    prestige_total = PositiveIntegerField(default=0, editable=False)
    prestige_level = ForeignKey('PrestigeLevel', SET_NULL, null=True, editable=False, related_name='memberships')

    objects = Manager()
    storytellers = QueryManager(title='storyteller')
    coordinators = QueryManager(title='coordinator')

    class Meta:
        unique_together = ('user', 'organization',)
        ordering = ('organization__name', 'user__username')

    def __str__(self):
        return f'#{self.external_id or self.pk} {self.user}'

    def recalculate_prestige(self):
        total = self.prestige.filter(amount__gt=0).all().aggregate(Sum('amount'))['amount__sum']
        self.prestige_total = total
        try:
            self.prestige_level = PrestigeLevel.objects.filter(
                organization=self.organization, prestige_required__lte=total).order_by('-prestige_required').first()
        except PrestigeLevel.DoesNotExist:
            logger.error(f'Missing prestige level for total >= {total}')
        self.save()


class PrestigeReport(Model):
    organization = ForeignKey('Organization', CASCADE, related_name='prestige_reports')
    start = DateField()
    end = DateField()

    class Meta:
        verbose_name = 'Prestige Report'

    def __str__(self):
        return f'Prestige {self.organization} {self.start}'


class Prestige(TimeStampedModel):
    membership = ForeignKey('Membership', CASCADE, related_name='prestige')
    report = ForeignKey('PrestigeReport', CASCADE, related_name='lines')
    amount = PositiveSmallIntegerField()
    notes = CharField(max_length=400, blank=True)

    class Meta:
        verbose_name = 'Prestige Line'
        ordering = ('membership', )

    def __str__(self):
        return f'{self.membership} +{self.amount}'

    def save(self, **kwargs):
        super().save(**kwargs)
        self.membership.recalculate_prestige()


class PrestigeLevel(Model):
    level = CharField(max_length=40)
    prestige_required = PositiveSmallIntegerField()
    organization = ForeignKey(Organization, CASCADE, related_name='prestige_levels')

    class Meta:
        verbose_name = 'Prestige Level'
        ordering = ('prestige_required', )
        unique_together = ('organization', 'level')

    def __str__(self):
        return str(self.level)

    def save(self, **kwargs):
        super().save(**kwargs)
        for membership in self.memberships:
            membership.recalculate_prestige()


class Invitation(TimeStampedModel):
    organization = ForeignKey(Organization, CASCADE, related_name='invitations')
    code = RandomCharField(length=8, unique=True)
    is_accepted = BooleanField(default=False)
    external_id = CharField(max_length=20, blank=True, verbose_name='External ID')
    email_address = EmailField()

    def __str__(self):
        return f'{self.email_address}'

    def save(self, **kwargs):
        # TODO Actually send notification email
        super().save(**kwargs)

    @classmethod
    def redeem(cls, user):
        invitations = cls.objects.filter(email_address=user.email, is_accepted=True)
        for inv in invitations:
            Membership.objects.create(
                user=user, organization=inv.organization, external_id=inv.external_id, status='active')
        invitations.delete()

    def invite_link(self):
        if self.code and self.organization.site:
            path = reverse('accept_invite', args=[self.code])
            url = f'{self.organization.site.domain}{path}'
            return format_html(f'<a href="{url}">{url}</a>')
