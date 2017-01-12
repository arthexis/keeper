from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.conf import settings

from systems.fields import *
from systems.models import *


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
                   .aggregate(x=models.Sum('member_beats'))['x'] / settings.BEATS_PER_PRESTIGE)

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
        return "{}".format(str(self.member_beats))


SKILLS = (
    ("academics", "Academics"),
    ("computer", "Computer"),
    ("crafts", "Crafts"),
    ("investigation", "Investigation"),
    ("medicine", "Medicine"),
    ("occult", "Occult"),
    ("politics", "Politics"),
    ("science", "Science"),
    ("athletics", "Athletics"),
    ("brawl", "Brawl"),
    ("drive", "Drive"),
    ("firearms", "Firearms"),
    ("larceny", "Larceny"),
    ("stealth", "Stealth"),
    ("survival", "Survival"),
    ("weaponry", "Weaponry"),
    ("animal_ken", "Animal Ken"),
    ("empathy", "Empathy"),
    ("expression", "Expression"),
    ("intimidation", "Intimidation"),
    ("persuasion", "Persuasion"),
    ("socialize", "Socialize"),
    ("streetwise", "Streetwise"),
    ("subterfuge", "Subterfuge"),
)

ATTRIBUTES = (
    ("strength", "Strength"),
    ("dexterity", "Dexterity"),
    ("stamina", "Stamina"),
    ("intelligence", "Intelligence"),
    ("wits", "Wits"),
    ("resolve", "Resolve"),
    ("presence", "Presence"),
    ("manipulation", "Manipulation"),
    ("composure", "Composure"),
)


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
        ordering = ('-event_date', )


class Character(models.Model):

    # Character basic info
    name = models.CharField(max_length=40, verbose_name="Character")
    template = models.ForeignKey(Template, on_delete=models.PROTECT)
    power_stat = DotsField(default=1, clear=False)
    integrity = DotsField(default=7)
    background = models.TextField(blank=True)
    resource = models.PositiveIntegerField(default=10)
    concept = models.CharField(max_length=200, blank=True)
    faction = models.CharField(max_length=200, blank=True)
    character_group = models.CharField(max_length=100, blank=True)

    # Physical Attributes
    strength = DotsField(default=1, clear=False)
    dexterity = DotsField(default=1, clear=False)
    stamina = DotsField(default=1, clear=False)

    # Mental Attributes
    intelligence = DotsField(default=1, clear=False)
    wits = DotsField(default=1, clear=False)
    resolve = DotsField(default=1, clear=False)

    # Social Attributes
    presence = DotsField(default=1, clear=False)
    manipulation = DotsField(default=1, clear=False)
    composure = DotsField(default=1, clear=False)

    # Mental Skills
    academics = DotsField()
    computer = DotsField()
    crafts = DotsField()
    investigation = DotsField()
    medicine = DotsField()
    occult = DotsField()
    politics = DotsField()
    science = DotsField()

    # Physical Skills
    athletics = DotsField()
    brawl = DotsField()
    drive = DotsField()
    firearms = DotsField()
    larceny = DotsField()
    stealth = DotsField()
    survival = DotsField()
    weaponry = DotsField()

    # Social Skills
    animal_ken = DotsField()
    empathy = DotsField()
    expression = DotsField()
    intimidation = DotsField()
    persuasion = DotsField()
    socialize = DotsField()
    streetwise = DotsField()
    subterfuge = DotsField()

    # Splat foreign Keys
    primary_splat = models.ForeignKey(SplatOption, on_delete=models.PROTECT, related_name='+', null=True, blank=True)
    secondary_splat = models.ForeignKey(SplatOption, on_delete=models.PROTECT, related_name='+', null=True, blank=True)
    tertiary_splat = models.ForeignKey(SplatOption, on_delete=models.PROTECT, related_name='+', null=True, blank=True)

    # Character Advancement related
    beats = DotsField()
    experiences = models.PositiveIntegerField(default=0)
    template_beats = DotsField()
    template_experiences = models.PositiveIntegerField(default=0)

    # Organization related fields
    player = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='characters')
    chronicle = models.ForeignKey(
        Chronicle, on_delete=models.PROTECT, null=True, blank=True, related_name='characters')
    created_on = models.DateField(auto_now_add=True, editable=False)
    modified_on = models.DateField(auto_now=True, editable=False)

    # Derived traits, they are not handled automatically because in some situations
    # their values can be manually adjusted
    health_levels = models.PositiveIntegerField(default=0)
    willpower = DotsField(default=1, clear=False)

    # Character Anchors (ie. Virtue / Vice)
    primary_anchor = models.CharField(max_length=40, blank=True)
    secondary_anchor = models.CharField(max_length=40, blank=True)

    # Character Advancement
    spent_experience = models.SmallIntegerField('Spent Exp', default=0, editable=False)
    is_current = models.BooleanField(default=True, editable=False)

    # Derived Traits

    def speed(self):
        return 5 + self.strength + self.dexterity

    def initiative(self):
        return self.dexterity + self.composure

    def defense(self):
        return min((self.dexterity, self.wits)) + self.defense_skill()

    def defense_skill(self):
        return self.athletics

    def size(self):
        return 5

    def health(self):
        return self.size() + self.stamina

    def merit_value(self, merit_name):
        qs = self.merits.filter(merit__name=merit_name)
        return qs.first().rating if qs.exists() else 0

    # Experience related calculations

    def storyteller_beats(self):
        return Assistance.objects.filter(character=self).aggregate(x=models.Sum('storyteller_beats'))['x']
    storyteller_beats.short_description = "Story beats"

    def coordinator_beats(self):
        return Assistance.objects.filter(character=self).aggregate(x=models.Sum('coordinator_beats'))['x']
    coordinator_beats.short_description = "Coord. beats"

    def prestige_beats(self):
        return (Prestige.objects
                .filter(membership__user=self.user).aggregate(x=models.Sum('prestige_beats'))['x'])
    prestige_beats.short_description = "Prestige"

    def accumulated_experience(self):
        return int((self.storyteller_beats() + self.coordinator_beats() + self.prestige_beats())
                   / settings.BEATS_PER_EXPERIENCE)
    accumulated_experience.short_description = "Total Exp"

    def available_experience(self):
        return self.accumulated_experience() - self.spent_experience
    available_experience.short_description = "Available Exp"

    # Other model methods

    def __str__(self):
        return str(self.name)

    def player_email(self):
        return self.player.email

    def player_name(self):
        return self.player.get_full_name()

    def last_approved(self):
        return ApprovalRequest.objects.filter(character=self, status="approved").latest(field_name='completed_on')

    def version(self):
        return self.last_approved().version

    def save(self, **kwargs):
        created = not bool(self.pk)
        super().save(**kwargs)
        if created:
            ApprovalRequest.objects.create(
                character=self,
                version=1,
                status="approved",
                details="New character approval.",
            )


class CharacterElement(models.Model):

    def save(self, **kwargs):
        super().save(**kwargs)

    class Meta:
        abstract = True


class CharacterMerit(CharacterElement):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='merits')
    merit = models.ForeignKey(Merit, on_delete=models.PROTECT, related_name='+')
    rating = DotsField(default=1, clear=False)
    details = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Merit"

    def category(self):
        return self.merit.get_category_display()

    def origin(self):
        return self.merit.template.name if self.merit.template else 'Any'

    def __str__(self):
        return '{} ({})'.format(self.merit.name, self.rating)


class CharacterPower(CharacterElement):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='powers')
    power = models.ForeignKey(Power, on_delete=models.PROTECT, related_name='+')
    rating = DotsField(default=1, clear=False)
    details = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Power"

    def __str__(self):
        if self.details:
            return '{} {} ({})'.format(self.power.name, self.rating, self.details)
        else:
            return '{} {}'.format(self.power.name, self.rating)

    def category(self):
        return self.power.category.name


class SkillSpeciality(CharacterElement):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='specialities')
    skill = models.CharField(max_length=20, choices=SKILLS)
    speciality = models.CharField(max_length=200)

    def __str__(self):
        return "{} ({})".format(self.speciality, self.get_skill_display())

    class Meta:
        verbose_name = "Skill Speciality"
        verbose_name_plural = "Skill Specialities"


class ApprovalRequest(models.Model):
    STATUSES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    created_on = models.DateField(auto_now_add=True, editable=False)
    completed_on = models.DateField(null=True, blank=True, editable=False)
    character = models.ForeignKey(
        Character, on_delete=models.CASCADE, related_name='approval_requests', null=True)
    player_notes = models.TextField(blank=True)
    details = models.TextField(help_text='First 80 characters of the first line will show as a summary.')
    status = models.CharField(max_length=20, default='pending', choices=STATUSES)
    spent_experience = models.SmallIntegerField('Spent Exp', default=0)
    version = models.IntegerField(null=True, blank='')

    def request_id(self):
        return "{:06d}".format(int(self.pk))

    def __str__(self):
        return self.request_id()

    def summary(self):
        return self.details[:80].splitlines()[0] if self.details else '<< Blank >>'

    def save(self, **kwargs):
        if self.status != 'pending' and not self.completed_on:
            self.completed_on = timezone.now().date()
            if not self.version:
                self.version = ApprovalRequest.objects\
                    .filter(character=self.character)\
                    .latest(field_name='completed_on').version + 1
        super().save(**kwargs)

    def chronicle(self):
        return self.character.chronicle

    def player_name(self):
        return self.character.player.get_full_name()

    def player_email(self):
        return self.character.player.email

    def template(self):
        return self.character.template

    def venue_storyteller(self):
        try:
            return self.character.chronicle.venue_storyteller
        except AttributeError:
            return None

    def domain_storyteller(self):
        try:
            return self.character.chronicle.domain_storyteller
        except AttributeError:
            return None

    def storytelling_group(self):
        try:
            return self.character.chronicle.storytelling_group
        except AttributeError:
            return None

    def can_approve(self, user: User):
        return (
            user.is_superuser or
            user == self.venue_storyteller() or
            user == self.domain_storyteller() or
            user in self.storytelling_group()
        )


class PendingApprovalManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(status="pending")


class PendingApproval(ApprovalRequest):
    objects = PendingApprovalManager()

    class Meta:
        proxy = True


class Assistance(models.Model):
    character = models.ForeignKey(Character, on_delete=models.PROTECT, related_name='+')
    event = models.ForeignKey(Event, on_delete=models.PROTECT, related_name='+')
    storyteller_beats = models.SmallIntegerField('Story beats', default=0)
    coordinator_beats = models.SmallIntegerField('Org beats', default=0)
    details = models.CharField(max_length=200, blank=True)

    def event_short_name(self):
        return self.event.short_name()

    def __str__(self):
        return self.event_short_name()

