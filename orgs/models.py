from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User, Group
from systems.models import Template


class Membership(models.Model):
    STATUSES = (
        ('hold', 'On Hold'),
        ('provisional', 'Provisional'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    )
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUSES, default='provisional')
    joined_on = models.DateField('Joined', null=True, blank=True)
    starts_on = models.DateField('Starts', null=True, blank=True)
    ends_on = models.DateField('Ends', null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def prestige_level(self):
        return int(Prestige.objects.filter(membership=self)
                   .aggregate(x=models.Sum('prestige_beats'))['x'] / settings.BEATS_PER_PRESTIGE)

    def user_name(self):
        return self.user.get_full_name()

    def user_email(self):
        return self.user.email


class Prestige(models.Model):
    membership = models.ForeignKey(Membership, on_delete=models.PROTECT, related_name='prestige')
    prestige_beats = models.SmallIntegerField(default=0)
    details = models.TextField(blank=True)
    awarded_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return "{}".format(str(self.prestige_beats))


class Chronicle(models.Model):
    name = models.CharField(max_length=40, verbose_name="Chronicle Name")
    code = models.CharField(max_length=10, unique=True)
    venue_storyteller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    domain_storyteller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    venue_coordinator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    domain_coordinator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    storytelling_group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    coordinating_group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    mood = models.CharField(max_length=200, blank=True)
    theme = models.CharField(max_length=200, blank=True)
    default_template = models.ForeignKey(Template, on_delete=models.PROTECT, null=True)
    information = models.TextField(blank=True)

    def __str__(self):
        return "{} - {}".format(self.code, self.name)


class Event(models.Model):
    name = models.CharField(max_length=40, verbose_name="Event Name")
    chronicle = models.ForeignKey(Chronicle, on_delete=models.PROTECT, related_name='events')
    event_date = models.DateField(null=True, blank=True)
    information = models.TextField(blank=True)
    planning_document = models.URLField(blank=True)
    seq = models.SmallIntegerField(null=True, editable=False)

    def short_name(self):
        return "{}-{}".format(self.chronicle.code, str(self.seq))

    def __str__(self):
        return self.short_name()

    def save(self, **kwargs):
        if not self.seq:
            try:
                self.seq = Event.objects.filter(chronicle=self.chronicle).latest('event_date').seq + 1
            except Event.DoesNotExist:
                self.seq = 1
        super().save(**kwargs)

    def is_scheduled(self):
        return self.event_date >= timezone.now().date()

    is_scheduled.boolean = True

    class Meta:
        ordering = ('-event_date',)

