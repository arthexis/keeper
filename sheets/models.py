import logging
import uuid

from django.db import transaction
from django.db.models import Model, CharField, ForeignKey, TextField, PositiveIntegerField, \
    PROTECT, DO_NOTHING, CASCADE, UUIDField, Manager
from django.contrib.auth.models import User, Group
from model_utils import Choices
from model_utils.managers import InheritanceManager, QueryManager
from model_utils.models import TimeStampedModel, StatusModel

from orgs.models import Organization
from systems.models import CharacterTemplate, Splat, Power, Merit, SKILLS, SplatCategory
from systems.fields import DotsField

logger = logging.getLogger(__name__)


__all__ = (
    "Character",
    "CharacterMerit",
    "CharacterPower",
    "SkillSpeciality",
)


class Character(TimeStampedModel, StatusModel):

    STATUS = Choices(
        ('in_progress', 'In Progress'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('archived', 'Archived'),
    )

    # Character basic info
    name = CharField("Name or Alias", max_length=40)
    template = ForeignKey(CharacterTemplate, CASCADE, null=True)
    power_stat = DotsField(default=1, clear=False)
    integrity = DotsField(default=7)
    background = TextField(blank=True)
    alt_names = CharField("Other Names", max_length=500, blank=True)
    resource = PositiveIntegerField(default=10, blank=True, null=True)
    resource_max = PositiveIntegerField(default=10, blank=True, null=True)
    concept = CharField(max_length=200, blank=True)
    faction = CharField(max_length=200, blank=True)
    character_group = CharField(max_length=100, blank=True)

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
    academics = DotsField(circles=5)
    computer = DotsField(circles=5)
    crafts = DotsField(circles=5)
    investigation = DotsField(circles=5)
    medicine = DotsField(circles=5)
    occult = DotsField(circles=5)
    politics = DotsField(circles=5)
    science = DotsField(circles=5)

    # Physical Skills
    athletics = DotsField(circles=5)
    brawl = DotsField(circles=5)
    drive = DotsField(circles=5)
    firearms = DotsField(circles=5)
    larceny = DotsField(circles=5)
    stealth = DotsField(circles=5)
    survival = DotsField(circles=5)
    weaponry = DotsField(circles=5)

    # Social Skills
    animal_ken = DotsField(circles=5)
    empathy = DotsField(circles=5)
    expression = DotsField(circles=5)
    intimidation = DotsField(circles=5)
    persuasion = DotsField(circles=5)
    socialize = DotsField(circles=5)
    streetwise = DotsField(circles=5)
    subterfuge = DotsField(circles=5)

    # Splat foreign Keys
    primary_splat = ForeignKey(Splat, PROTECT, related_name='+', null=True, blank=True)
    primary_sub_splat = ForeignKey(Splat, PROTECT, related_name='+', null=True, blank=True)
    secondary_splat = ForeignKey(Splat, PROTECT, related_name='+', null=True, blank=True)
    secondary_sub_splat = ForeignKey(Splat, PROTECT, related_name='+', null=True, blank=True)
    tertiary_splat = ForeignKey(Splat, PROTECT, related_name='+', null=True, blank=True)

    # Organization related fields
    user = ForeignKey(
        User, DO_NOTHING, null=True, blank=True, related_name='characters')
    organization = ForeignKey(Organization, CASCADE, null=True, blank=True)

    # Derived traits, they are not handled automatically because
    # their values can be manually adjusted
    size = DotsField(default=5, clear=False, editable=False)
    health_levels = PositiveIntegerField(default=0)
    damage_track = CharField(max_length=100, blank=True, null=True)
    willpower = PositiveIntegerField(blank=True, null=True)
    willpower_max = PositiveIntegerField(blank=True, null=True, editable=False)
    perm_willpower_spent = PositiveIntegerField(blank=True, null=True)

    # Character Anchors (ie. Virtue / Vice)
    primary_anchor = CharField(max_length=40, blank=True)
    secondary_anchor = CharField(max_length=40, blank=True)

    # Versioning fields. The highest number is the latest version

    version = PositiveIntegerField(default=0)
    uuid = UUIDField(default=uuid.uuid4, editable=False)

    objects = Manager()
    active = QueryManager(status__in=('in_progress', 'submitted', 'approved'))
    submitted = QueryManager(status='submitted')
    approved = QueryManager(status='approved')

    class Meta:
        unique_together = (('uuid', 'version'),)

    # Derived Traits

    def speed(self):
        return 5 + self.strength + self.dexterity

    def initiative(self):
        return self.dexterity + self.composure

    def defense(self):
        return min((self.dexterity, self.wits)) + self.defense_skill()

    def defense_skill(self):
        return self.athletics

    def merit_value(self, merit_name):
        qs = self.merits.filter(merit__name=merit_name)
        return qs.first().rating if qs.exists() else 0

    def splats(self):
        flavors = SplatCategory.FLAVORS
        return [x for x in (getattr(self, s, None) for k, s in flavors) if x is not None]

    def __str__(self):
        return str(self.name)

    # The following methods are useful to have around for template rendering

    def splat_1_pk(self):
        return self.primary_splat.pk if self.primary_splat else ""

    def splat_2_pk(self):
        return self.secondary_splat.pk if self.secondary_splat else ""

    def splat_3_pk(self):
        return self.tertiary_splat.pk if self.tertiary_splat else ""

    def primary_anchor_name(self):
        return self.template.primary_anchor_name if self.template else "Virtue"

    def secondary_anchor_name(self):
        return self.template.secondary_anchor_name if self.template else "Vice"

    def available_health_track(self):
        return str(self.damage_track)[:int(self.health_levels)] + \
               ('_' * (self.health_levels - len(self.damage_track or '')))

    # Calculate some stuff automatically on save
    def save(self, **kwargs):
        if self.power_stat:
            self.resource_max = int(self.power_stat) + 10

        self.willpower_max = int(self.resolve) + int(self.composure) - int(self.perm_willpower_spent or 0)
        self.health_levels = int(self.stamina) + int(self.size)
        if self.willpower is None:
            self.willpower = self.willpower_max

        super().save(**kwargs)

    # Methods related to revisions and approvals

    def is_locked(self):
        return self.status in ('archived', 'approved')

    def is_active(self):
        return self.status != 'archived'

    def submit(self):
        self.status = 'submitted'
        self.save()

    def approve(self):
        self.status = 'approved'
        self.save()

    def reject(self):
        self.rejected = 'in_progress'
        self.save()

    def create_revision(self):
        with transaction.atomic():
            self.status = 'archived'
            self.save()

            # By removing the PK a new instance is created on save()
            old_pk, self.pk, self.status = self.pk, None, 'in_progress'
            self.version += 1
            self.save()
            for cls in (CharacterMerit, CharacterPower, SkillSpeciality):
                for elem in cls.objects.filter(character_id=old_pk):
                    elem.pk, elem.character_id = None, self.pk
                    elem.save()
        return self

    def revisions(self):
        return Character.objects.filter(uuid=self.uuid).order_by('version')

    def active_revision(self):
        return self.revisions().exclude(status='archived').first()


class CharacterElement(Model):
    objects = InheritanceManager()

    def save(self, **kwargs):
        super().save(**kwargs)

    class Meta:
        abstract = True


class CharacterMerit(CharacterElement):
    character = ForeignKey(Character, CASCADE, related_name='merits')
    merit = ForeignKey(Merit, PROTECT, related_name='+')
    rating = DotsField(default=1, clear=False)
    details = CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Merit"

    def origin(self):
        return self.merit.character_template.name if self.merit.character_template else 'Any'

    def __str__(self):
        return '{} ({})'.format(self.merit.name, self.rating)


class CharacterPower(CharacterElement):
    character = ForeignKey(Character, CASCADE, related_name='powers')
    power = ForeignKey(Power, PROTECT, related_name='+')
    rating = DotsField(default=1, clear=False)

    class Meta:
        verbose_name = "Power"

    def __str__(self):
        return f'{self.power.name} {self.rating}'

    def category(self):
        return self.power.power_category.name


class SkillSpeciality(CharacterElement):
    character = ForeignKey(Character, CASCADE, related_name='specialities')
    skill = CharField(max_length=20, choices=SKILLS, blank=True)
    speciality = CharField(max_length=200, blank=True)

    def __str__(self):
        return "{} ({})".format(self.speciality, self.get_skill_display())

    class Meta:
        verbose_name = "Skill Speciality"
        verbose_name_plural = "Skill Specialities"



