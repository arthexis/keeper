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

    user = OneToOneField(User, on_delete=PROTECT, related_name='profile', editable=False)
    phone = CharField(max_length=20, blank=True,
                      help_text="Optional. Only shared with Organizations you join.")
    is_verified = BooleanField(default=False, editable=False)
    last_visit = DateTimeField(blank=True, null=True, editable=False)
    verification_code = CharField(max_length=VERIFICATION_CHARS, blank=True, null=True, editable=False)
    code_sent_on = DateTimeField(blank=True, null=True, editable=False)
    org_create_cap = SmallIntegerField(default=5, editable=False)
    information = TextField(
        blank=True, null=True,
        help_text="Optional. Personal information that you want to share with Orgs.")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse('orgs:edit-profile', kwargs={'pk': self.pk})

    def make_verification_url(self):
        self.is_verified = False
        self.verification_code = rand_string(self.VERIFICATION_CHARS)
        self.code_sent_on = timezone.now()
        self.save()
        return reverse("orgs:verification", kwargs={'pk': self.pk, 'code': self.verification_code})

    def send_mail(self, subject, message=None, template=None, context=None):
        if not self.email:
            logger.error(f"Unable to send email to {self.username}; address missing.")
            return
        kwargs = {'fail_silently': True}
        if template is not None:
            kwargs['html_message'] = render_to_string(template, context)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.email], **kwargs)

    def send_verification_email(self):
        verification_url = self.make_verification_url()
        logger.info(f"Sending verification email to {self.username}. url={verification_url}")
        self.send_mail(
            'Keeper Email Verification', (
                "Keeper Email Verification\n\n"
                f"Please enter this URL into your browser's navigation bar: \n{verification_url}\n"
                "If you didn't request an account, please ignore this message."
            ),
            'orgs/email/verification.html',
            {'profile': self, 'verification_url': verification_url},
        )

    def send_recovery_email(self):
        verification_url = self.make_verification_url()
        logger.info(f"Sending recovery email to {self.username}. url={verification_url}")
        self.send_mail(
            'Keeper Password Recovery', (
                "Keeper Password Recovery\n\n"
                "You are receiving this email because you or someone else requested to recover"
                f"the password to your Keeper account with username: {self.username}"
                f"To recover your account copy this URL into your browser's navigation bar: \n{verification_url}\n"
                "If you didn't request to recover your password, please ignore this message."
            ),
            'orgs/email/recovery.html',
            {'profile': self, 'verification_url': verification_url},
        )


# Users can create Organizations
class Organization(Model):
    name = CharField(max_length=200, help_text="Required. Must be unique across all Organizations.", unique=True)
    parent_org = ForeignKey(
        'Organization', SET_NULL, verbose_name="Parent Organization", blank=True, null=True,
        help_text="Optional. If set, you will inherit settings and staff from this organization.")
    information = TextField(blank=True)
    is_public = BooleanField(
        default=True, verbose_name="Open to the Public",
        help_text="Allow others to search and find this organization and request membership.")

    def __str__(self):
        return self.name

    def get_membership(self, user):
        return self.memberships.get(user=user)


class PublicOrganizationManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_public=True)


class PublicOrganization(Organization):
    objects = PublicOrganizationManager()

    class Meta:
        proxy = True


# Membership is a relation between Users and Organizations
class Membership(Model):
    user = ForeignKey(User, CASCADE, related_name="memberships")
    organization = ForeignKey(Organization, CASCADE, related_name="memberships")
    title = CharField(max_length=200, blank=True, null=True)
    is_active = BooleanField(default=False)
    is_officer = BooleanField(default=False)
    is_owner = BooleanField(default=False)
    is_blocked = BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'organization',)
        ordering = ('organization__name', )

    def description(self):
        if not self.is_active:
            if self.is_blocked:
                return 'Blocked'
            return 'Inactive'
        if self.is_officer:
            return 'Active Officer'
        return 'Active Member'


class UpcomingEventManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(event_date__gte=timezone.now().date())


# Organizations can create events in the event calendar
class Event(Model):
    upcoming = UpcomingEventManager()

    name = CharField(max_length=40)
    organization = ForeignKey(Organization, CASCADE, null=True, related_name='events')
    event_date = DateField(null=True, blank=True)
    information = TextField(blank=True)
    # seq = SmallIntegerField(null=True, editable=False)

    def __str__(self):
        return self.name

    # def last_org_event(self):
    #     return Event.objects.filter(organization=self.organization).latest('event_date')

    # def save(self, **kwargs):
    #     if not self.seq:
    #         try:
    #             self.seq = self.last_org_event().seq + 1
    #         except Event.DoesNotExist:
    #             self.seq = 1
    #     super().save(**kwargs)

    def is_upcoming(self):
        return self.event_date >= timezone.now().date()
    is_upcoming.boolean = True

    class Meta:
        ordering = ('-event_date',)


__all__ = (
    'Profile',
    'Organization',
    'PublicOrganization',
    'Membership',
    'Event',
)
