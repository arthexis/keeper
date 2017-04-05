from django.db.models import *
from django.utils import timezone
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from systems.models import Template


# Each individual user has a Profile
class Profile(User):
    user = OneToOneField(User, on_delete=PROTECT, related_name='profile')
    phone = CharField(max_length=20, blank=True)
    is_verified = BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('orgs:profile', kwargs={'pk': self.pk})


# Users can create Organizations
class Organization(Model):
    name = CharField(max_length=200)
    parent_org = ForeignKey('Organization', SET_NULL, blank=True, null=True)


# Membership is a relation between Users and Organizations
class Membership(Model):
    STATUSES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    
    status = CharField(max_length=20, choices=STATUSES, default='inactive')
    user = ForeignKey(User, CASCADE)
    organization = ForeignKey(Organization, CASCADE)


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


__all__ = ('Profile', 'Organization', 'Membership', 'Event')