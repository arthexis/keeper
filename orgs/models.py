from django.db.models import *
from django.urls import reverse
from django.contrib.auth.models import User, Group
from systems.models import CharacterTemplate
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from keeper.utils import rand_string
from django.utils import timezone

import logging
logger = logging.getLogger(__name__)


__all__ = (
    'Profile',
    'Organization',
    'Membership',
    'Event',
    'UpcomingEvent',
    'PublicOrganization',
)


# Each individual user has a Profile
class Profile(User):
    VERIFICATION_CHARS = 14

    user = OneToOneField(
        User, on_delete=PROTECT, related_name='profile', parent_link=True)
    phone = CharField(
        max_length=20, blank=True,
        help_text="Optional. Only shared with Organizations you join.")
    is_verified = BooleanField(default=False, editable=False)
    last_visit = DateTimeField(blank=True, null=True, editable=False)
    verification_code = CharField(
        max_length=VERIFICATION_CHARS, blank=True, null=True, editable=False)
    code_sent_on = DateTimeField(blank=True, null=True, editable=False)
    org_create_cap = SmallIntegerField(default=5, editable=False)
    information = TextField(
        blank=True, null=True,
        help_text="Optional. Personal information shared with others.")

    class Meta:
        verbose_name = 'Profile'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse('orgs:edit-profile', kwargs={'pk': self.pk})

    def make_verification_url(self):
        self.is_verified = False
        self.verification_code = rand_string(self.VERIFICATION_CHARS)
        self.code_sent_on = timezone.now()
        self.save()
        return reverse(
            "orgs:verification",
            kwargs={'pk': self.pk, 'code': self.verification_code})

    def send_mail(self, subject, message=None, template=None, context=None):
        if not self.email:
            logger.error(
                f"Unable to send email to {self.username}; address missing.")
            return
        kwargs = {'fail_silently': True}
        if template is not None:
            kwargs['html_message'] = render_to_string(template, context)
        send_mail(
            subject, message, settings.DEFAULT_FROM_EMAIL,
            [self.email], **kwargs)

    def initiate_verification(self):
        if not settings.ORGS_AUTO_VERIFY_USERS:
            return self.send_verification_email()
        logger.info("Skipping user verification per settings.")
        self.is_verified = True
        self.save()

    def send_verification_email(self):
        verification_url = self.make_verification_url()
        logger.info(
            f"Send verification to {self.username}. url={verification_url}")
        self.send_mail(
            'Keeper Email Verification', (
                "Keeper Email Verification\n\n"
                f"Please click the following link: \n{verification_url}\n"
                "If you didn't request an account, please ignore this message."
            ),
            'orgs/email/verification.html',
            {'profile': self, 'verification_url': verification_url})

    def send_recovery_email(self):
        verification_url = self.make_verification_url()
        logger.info(
            f"Send recovery email to {self.username}. url={verification_url}")
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

    def upcoming_events(self):
        return Event.objects.filter(
            organization__memberships__user=self.user,
            event_date__gte=timezone.now().date()
        ).exclude(
            organization__memberships__is_active=False,
            organization__memberships__is_blocked=True
        ).order_by('-event_date')


# Users can create Organizations
class Organization(Model):
    name = CharField(
        max_length=200, unique=True,
        help_text="Required. Must be unique across all Organizations.")
    parent_org = ForeignKey(
        'Organization', SET_NULL, verbose_name="Parent Organization",
        blank=True, null=True,
        help_text="Optional. If set, you will inherit settings and staff.")
    information = TextField(blank=True)
    is_public = BooleanField(
        default=True, verbose_name="Open to the Public",
        help_text="Allow finding the organization and requesting membership.")

    def __str__(self):
        return self.name

    def get_membership(self, user):
        return self.memberships.get(user=user)

    def upcoming_events(self):
        return UpcomingEvent.objects.filter(organization=self)


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


# Organizations can create events in the event calendar
class Event(Model):

    name = CharField(max_length=40)
    organization = ForeignKey(
        Organization, CASCADE, null=True, related_name='events', editable=False)
    event_date = DateField(null=True, blank=True)
    information = TextField(
        blank=True,
        help_text='Optional. Basic summary about the event.')
    external_url = URLField(
        null=True, blank=True,
        help_text='Optional. External link containing additional information.')
    is_public = BooleanField(default=False)
    is_published = BooleanField(default=True)

    def __str__(self):
        return self.name

    def is_upcoming(self):
        return self.event_date >= timezone.now().date()
    is_upcoming.boolean = True

    class Meta:
        ordering = ('-event_date',)


class UpcomingEventManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            event_date__gte=timezone.now().date())


class UpcomingEvent(Event):
    upcoming = UpcomingEventManager()
    
    class Meta:
        proxy = True

