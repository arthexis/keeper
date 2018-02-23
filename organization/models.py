import logging

from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models import CASCADE, CharField, ForeignKey, Manager, Model, URLField, \
    DO_NOTHING, DateField, PositiveSmallIntegerField, PositiveIntegerField, SET_NULL, Sum, EmailField, BooleanField
from django.urls import reverse
from django.utils.html import format_html
from django_extensions.db.fields import AutoSlugField, RandomCharField
from model_utils import Choices
from model_utils.managers import QueryManager
from model_utils.models import StatusModel, TimeStampedModel, TimeFramedModel

logger = logging.getLogger(__name__)

__all__ = (
    'Chapter',
    'Domain',
    'Membership',
    'Prestige',
    'PrestigeReport',
    'PrestigeLevel',
    'Invitation',
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
    prestige_cutoff = DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'Chapter'
        verbose_name_plural = 'Chapters and Domains'

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
    external_id = CharField(max_length=20, blank=True, verbose_name='External ID')

    prestige_total = PositiveIntegerField(default=0, editable=False)
    prestige_level = ForeignKey('PrestigeLevel', SET_NULL, null=True, editable=False, related_name='memberships')

    objects = Manager()
    storytellers = QueryManager(title='storyteller')
    coordinators = QueryManager(title='coordinator')

    class Meta:
        unique_together = ('user', 'chapter',)
        ordering = ('chapter__name', 'user__username')

    def __str__(self):
        return f'#{self.external_id or self.pk} {self.user}'

    def recalculate_prestige(self):
        total = self.prestige.filter(amount__gt=0).all().aggregate(Sum('amount'))['amount__sum']
        self.prestige_total = total
        try:
            self.prestige_level = PrestigeLevel.objects.filter(
                chapter=self.chapter, prestige_required__lte=total).order_by('-prestige_required').first()
        except PrestigeLevel.DoesNotExist:
            logger.error(f'Missing prestige level for total >= {total}')
        self.save()


class PrestigeReport(TimeFramedModel):
    chapter = ForeignKey('Chapter', CASCADE, related_name='prestige')

    class Meta:
        verbose_name = 'Prestige Report'

    def __str__(self):
        return f'Prestige {self.chapter} {self.start}'


class Prestige(TimeStampedModel):
    membership = ForeignKey('Membership', CASCADE, related_name='prestige')
    report = ForeignKey('PrestigeReport', CASCADE, related_name='lines')
    amount = PositiveSmallIntegerField()
    notes = CharField(max_length=400, blank=True)

    class Meta:
        verbose_name = 'Prestige Line'

    def __str__(self):
        return f'{self.membership} +{self.amount}'

    def save(self, **kwargs):
        super().save(**kwargs)
        self.membership.recalculate_prestige()


class PrestigeLevel(Model):
    level = CharField(max_length=40)
    prestige_required = PositiveSmallIntegerField()
    chapter = ForeignKey(Chapter, CASCADE, related_name='prestige_levels')

    class Meta:
        verbose_name = 'Prestige Level'
        ordering = ('prestige_required', )
        unique_together = ('chapter', 'level')

    def __str__(self):
        return str(self.level)

    def save(self, **kwargs):
        super().save(**kwargs)
        for membership in self.memberships:
            membership.recalculate_prestige()


class Invitation(TimeStampedModel):
    chapter = ForeignKey(Chapter, CASCADE, related_name='invitations')
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
            Membership.objects.create(user=user, chapter=inv.chapter, external_id=inv.external_id, status='active')
        invitations.delete()

    def invite_link(self):
        if self.code and self.chapter.site:
            path = reverse('accept_invite', args=[self.code])
            url = f'{self.chapter.site.domain}{path}'
            return format_html(f'<a href="{url}">{url}</a>')
