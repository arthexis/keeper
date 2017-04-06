from django.db.models import *
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from systems.models import Template
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from keeper.utils import rand_string
from django.utils import timezone

import logging
logger = logging.getLogger(__name__)


# Each individual user has a Profile
class Profile(User):
    VERIFICATION_CHARS = 14

    user = OneToOneField(User, on_delete=PROTECT, related_name='profile')
    phone = CharField(max_length=20, blank=True)
    is_verified = BooleanField(default=False)
    last_visit = DateTimeField(blank=True, null=True)
    verification_code = CharField(max_length=VERIFICATION_CHARS, blank=True, null=True)
    code_sent_on = DateTimeField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('orgs:profile', kwargs={'pk': self.pk})

    def make_verification_url(self):
        self.is_verified = False
        self.verification_code = rand_string(self.VERIFICATION_CHARS)
        self.code_sent_on = timezone.now()
        self.save()
        return reverse("orgs:verification", kwargs={'pk': self.pk, 'code': self.verification_code})

    def send_verification_email(self):
        if not self.email:
            logger.error(f"Unable to send verification email to {self.username}; address missing.")
        else:
            verification_url = self.make_verification_url()
            logger.info(f"Sending verification email to {self.username}. url={verification_url}")
            message = (
                "Keeper Email Verification\n\n"
                f"Please enter ths URL into your browser's navigation bar: \n{verification_url}\n"
                "If you didn't request an account, please ignore this message."
            )
            context = {'profile': self, 'verification_url': verification_url}
            send_mail(
                'Keeper Email Verification',
                message,
                settings.DEFAULT_FROM_EMAIL,
                [self.email],
                fail_silently=True,
                html_message=render_to_string('orgs/email/verification.html', context)
            )


# Users can create Organizations
class Organization(Model):
    name = CharField(max_length=200, help_text="Required. Must be unique across all Organizations.", unique=True)
    parent_org = ForeignKey(
        'Organization', SET_NULL, verbose_name="Parent Organization", blank=True, null=True,
        help_text="Optional. If set, you will inherit settings and staff from this organization.")
    information = TextField(blank=True)
    owner = ForeignKey(User, PROTECT, blank=True, null=True, editable=False)
    is_public = BooleanField(
        default=True, verbose_name="Open to the Public",
        help_text="Allow others to search and find this organization and request membership.")

    def save(self, **kwargs):
        super().save(**kwargs)
        if self.owner:
            logger.debug(f"Assigning user={self.owner} to own org={self}")
            membership, created = Membership.objects.get_or_create(user=self.owner, organization=self)
            membership.active = True
            membership.rank = 'owner'
            membership.save()
            logger.debug(f"Assign successful, membership pk={membership.pk}")

    def __str__(self):
        return self.name


class PublicOrganizationManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_public=True)


class PublicOrganization(Organization):
    objects = PublicOrganizationManager()

    class Meta:
        proxy = True


# Membership is a relation between Users and Organizations
class Membership(Model):
    STATUSES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    RANKS = (
        ('owner', 'Owner'),
        ('staff', 'Staff'),
        ('member', 'Member'),
    )
    
    status = CharField(max_length=40, choices=STATUSES, default='inactive')
    user = ForeignKey(User, CASCADE, related_name="memberships")
    organization = ForeignKey(Organization, CASCADE, related_name="memberships")
    rank = CharField(max_length=40, choices=RANKS, default="member")

    class Meta:
        unique_together = ('user', 'organization',)


# Organizations can create events in the event calendar
class Event(Model):
    name = CharField(max_length=40, verbose_name="Event Name")
    organization = ForeignKey(Organization, CASCADE, null=True)
    event_date = DateField(null=True, blank=True)
    information = TextField(blank=True)
    seq = SmallIntegerField(null=True, editable=False)

    def __str__(self):
        return self.name

    def last_org_event(self):
        return Event.objects.filter(organization=self.organization).latest('event_date')

    def save(self, **kwargs):
        if not self.seq:
            try:
                self.seq = self.last_org_event().seq + 1
            except Event.DoesNotExist:
                self.seq = 1
        super().save(**kwargs)

    def is_scheduled(self):
        return self.event_date >= timezone.now().date()

    is_scheduled.boolean = True

    class Meta:
        ordering = ('-event_date',)


__all__ = (
    'Profile',
    'Organization',
    'PublicOrganization',
    'Membership',
    'Event'
)
