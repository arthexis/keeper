import logging
import uuid

from django.db.models import Model, CharField, ForeignKey, TextField, PositiveIntegerField, \
    PROTECT, DO_NOTHING, CASCADE, UUIDField, SET_NULL, Manager, BinaryField
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect
from django.conf import settings
from model_utils import Choices
from model_utils.managers import InheritanceManager, QueryManager
from model_utils.models import TimeStampedModel, StatusModel

from organization.models import Domain
from game_rules.models import CharacterTemplate, Splat, Power, Merit, SplatCategory, ATTRIBUTE_KEYS, SKILLS, SKILL_KEYS
from game_rules.fields import DotsField
from keeper.utils import missing

logger = logging.getLogger(__name__)


__all__ = (
    'ApprovalRequest',
    "Character",
    "CharacterMerit",
    "CharacterPower",
    "SkillSpeciality",
)


class Character(TimeStampedModel, StatusModel):
    objects = Manager()

    STATUS = Choices(
        ('in_progress', 'In Progress'),
        ('approved', 'Approved'),
        ('archived', 'Archived'),
    )

    # Character basic info
    name = CharField("Name or Alias", max_length=40, db_index=True)
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
    user = ForeignKey(settings.AUTH_USER_MODEL, SET_NULL, null=True, blank=True, related_name='characters')
    domain = ForeignKey(Domain, SET_NULL, null=True, blank=True, related_name='characters')

    # Tracking of spent resources
    bashing_damage = PositiveIntegerField(default=0)
    lethal_damage = PositiveIntegerField(default=0)
    aggravated_damage = PositiveIntegerField(default=0)
    willpower_points_spent = PositiveIntegerField(default=0)
    willpower_dots_spent = PositiveIntegerField(default=0)
    supernatural_energy = PositiveIntegerField(default=0)
    extra_health_levels = PositiveIntegerField(default=0)

    # Character Anchors (ie. Virtue / Vice)
    primary_anchor = CharField(max_length=40, blank=True)
    secondary_anchor = CharField(max_length=40, blank=True)

    # Versioning fields. The highest number is the latest version
    version = PositiveIntegerField(default=0)
    created_by = ForeignKey(settings.AUTH_USER_MODEL, DO_NOTHING, related_name='+', null=True, blank=True)

    active = QueryManager(status__in=('in_progress', 'approved'))

    # This UUID is shared by all versions of the same character
    uuid = UUIDField(default=uuid.uuid4, editable=False, db_index=True)

    class Meta:
        pass
        # unique_together = (('uuid', 'version'),)

    def __str__(self):
        return f'[{self.template.game_line.upper()}] {self.name}'

    # Derived Traits

    def speed(self):
        return 5 + self.strength + self.dexterity

    def initiative(self):
        return self.dexterity + self.composure

    def defense(self):
        return min((self.dexterity, self.wits)) + self.defense_skill()

    def defense_skill(self):
        return self.athletics

    def willpower_dots(self):
        return (self.resolve + self.composure) - self.willpower_dots_spent

    def health_levels(self):
        return 5 + self.stamina + self.extra_health_levels

    # Retrieve related or summarized values

    def merit_value(self, merit_name):
        qs = self.merits.filter(merit__name=merit_name)
        return qs.first().rating

    def splats(self):
        flavors = SplatCategory.FLAVORS
        return [x for x in (getattr(self, s, None) for k, s in flavors) if x is not None]

    def attributes_total(self):
        return sum(int(getattr(self, k)) for k in ATTRIBUTE_KEYS)

    def skills_total(self):
        return sum(int(getattr(self, k)) for k in SKILL_KEYS)

    # The following methods are useful to have around for template rendering

    @missing("Virtue")
    def primary_anchor_name(self):
        return self.template.primary_anchor_name

    @missing("Vice")
    def secondary_anchor_name(self):
        return self.template.secondary_anchor_name

    # Methods related to revisions and approvals

    def is_locked(self):
        return self.status != 'in_progress'

    def can_create_revision(self, user=None):
        return self.is_locked() and user.is_staff

    def create_revision(self, user=None):
        # By removing the PK a new instance is created on save()
        old_pk, self.pk = self.pk, None
        self.status = 'in_progress'
        self.created_by = user
        self.version += 1
        self.save()

        # Copy character elements
        for cls in (CharacterMerit, CharacterPower, SkillSpeciality):
            cls.objects.filter(character_id=old_pk).update(id=None, character_id=self.pk)

        # Move pending approval requests to new revision
        ApprovalRequest.objects.filter(uuid=self.uuid, status='pending').update(character=self)

        # Return a redirect to new revision
        return redirect('admin:sheets_character_change', object_id=self.pk)

    def save(self, **kwargs):
        # When a sheet becomes approved, all other approved sheets for the same character are archived
        if self.status == 'approved':
            self.revisions().filter(status='approved').update(status='archived')
        super().save(**kwargs)

    def revisions(self):
        return Character.objects.filter(uuid=self.uuid).order_by('version')

    def approval_history(self):
        return ApprovalRequest.objects.filter(uuid=self.uuid).order_by('character__version')

    def request_approval(self):
        return ApprovalRequest.objects.create()


class CharacterElement(Model):
    objects = InheritanceManager()

    class Meta:
        abstract = True


class CharacterMerit(CharacterElement):
    character = ForeignKey(Character, CASCADE, related_name='merits')
    merit = ForeignKey(Merit, PROTECT, related_name='+')
    rating = DotsField(default=1, clear=False)
    details = CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Merit"

    def __str__(self):
        return f'{self.merit.name} self.rating'


class CharacterPower(CharacterElement):
    character = ForeignKey(Character, CASCADE, related_name='powers')
    power = ForeignKey(Power, PROTECT, related_name='+')
    rating = DotsField(default=1, clear=False)
    details = CharField(max_length=200, blank=True)

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


class ApprovalRequest(TimeStampedModel, StatusModel):
    STATUS = Choices(
        ('pending', 'Pending'),
        ('complete', 'Complete'),
    )

    character = ForeignKey(Character, DO_NOTHING, related_name='approval_requests')
    user = ForeignKey(settings.AUTH_USER_MODEL, DO_NOTHING, null=True, related_name='approval_requests')
    request = TextField('Request Information')
    attachment = BinaryField(blank=True)

    # Keep track of the character UUID
    uuid = UUIDField(editable=False, db_index=True, null=True)

    class Meta:
        verbose_name = "Approval Request"

    def __str__(self):
        return f'{self.character.name} #{self.pk}'

    def save(self, **kwargs):
        self.uuid = self.character.uuid
        if not self.user and self.character.user:
            self.user = self.character.user
        super().save(**kwargs)
