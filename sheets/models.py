import logging
import random
import uuid
import os.path
from django.core.exceptions import ValidationError

from django.db.models import Model, CharField, ForeignKey, TextField, PositiveIntegerField, \
    PROTECT, DO_NOTHING, CASCADE, UUIDField, SET_NULL, Manager, BinaryField, PositiveSmallIntegerField, Sum, \
    OneToOneField, F
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect
from django.conf import settings
from django.urls import reverse
from django.utils.html import format_html
from model_utils import Choices
from model_utils.managers import InheritanceManager, QueryManager
from model_utils.models import TimeStampedModel, StatusModel

from organization.models import Chronicle
from game_rules.models import CharacterTemplate, Splat, Power, Merit, SplatCategory, \
    TemplateAnchor, PowerOption
from keeper.settings import ATTRIBUTE_KEYS, SKILLS, SKILL_KEYS
from game_rules.fields import DotsField
from keeper.utils import missing


logger = logging.getLogger(__name__)


__all__ = (
    'ApprovalRequest',
    "Character",
    "CharacterMerit",
    "CharacterPower",
    "CharacterAnchor",
    "SkillSpeciality",
    "Advancement",
    'DowntimeAction',
    'ResourceTracker',
    'HealthTracker',
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
    storyteller_notes = TextField(blank=True, help_text="Hidden from player.")
    player_notes = TextField(blank=True, help_text="Shown in player sheet.")
    resource_start = PositiveIntegerField(default=10, blank=True, null=True)
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
    academics = DotsField(number=5)
    computer = DotsField(number=5)
    crafts = DotsField(number=5)
    investigation = DotsField(number=5)
    medicine = DotsField(number=5)
    occult = DotsField(number=5)
    politics = DotsField(number=5)
    science = DotsField(number=5)

    # Physical Skills
    athletics = DotsField(number=5)
    brawl = DotsField(number=5)
    drive = DotsField(number=5)
    firearms = DotsField(number=5)
    larceny = DotsField(number=5)
    stealth = DotsField(number=5)
    survival = DotsField(number=5)
    weaponry = DotsField(number=5)

    # Social Skills
    animal_ken = DotsField(number=5)
    empathy = DotsField(number=5)
    expression = DotsField(number=5)
    intimidation = DotsField(number=5)
    persuasion = DotsField(number=5)
    socialize = DotsField(number=5)
    streetwise = DotsField(number=5)
    subterfuge = DotsField(number=5)

    # Other traits
    size = PositiveSmallIntegerField(default=5)
    speed = PositiveSmallIntegerField(default=0)
    initiative = PositiveSmallIntegerField(default=0)
    armor_general = PositiveSmallIntegerField(default=0)
    armor_ballistic = PositiveSmallIntegerField(default=0)

    # Splat foreign Keys
    primary_splat = ForeignKey(Splat, PROTECT, related_name='+', null=True, blank=True)
    primary_sub_splat = ForeignKey(Splat, PROTECT, related_name='+', null=True, blank=True)
    secondary_splat = ForeignKey(Splat, PROTECT, related_name='+', null=True, blank=True)
    secondary_sub_splat = ForeignKey(Splat, PROTECT, related_name='+', null=True, blank=True)
    tertiary_splat = ForeignKey(Splat, PROTECT, related_name='+', null=True, blank=True)

    # Organization related fields
    user = ForeignKey(settings.AUTH_USER_MODEL, SET_NULL, null=True, blank=True, related_name='characters')
    chronicle = ForeignKey(Chronicle, SET_NULL, null=True, blank=True, related_name='characters')

    # Tracking of spent resources
    willpower_max = DotsField()
    health_boxes = DotsField(number=20, break_after=10)

    # Character Anchors (ie. Virtue / Vice)
    primary_anchor = CharField(max_length=40, blank=True)
    secondary_anchor = CharField(max_length=40, blank=True)

    # Version fields. The highest number is the latest version
    version = PositiveIntegerField(default=0)
    active = QueryManager(status__in=('in_progress', 'approved'))

    # This UUID is shared by all versions of the same character
    uuid = UUIDField(default=uuid.uuid4, editable=False, db_index=True)

    def __str__(self):
        return f'[{self.template.game_line.upper()}] {self.name}'

    def get_absolute_url(self):
        return reverse('character-detail', kwargs={'pk': self.pk})

    def get_admin_link(self, full=False):
        url = reverse('admin:sheets_character_change', kwargs={'object_id': self.pk})
        name = url if full else str(self)
        return format_html('<a href="{}">{}</a>', url, name)

    def member_link(self, full=False):
        url = reverse('character-detail', kwargs={'pk': self.pk})
        name = url if full else str(self)
        return format_html('<a href="{}">{}</a>', url, name)

    # Derived Traits

    def defense(self):
        return min((self.dexterity, self.wits)) + self.defense_skill()

    def defense_skill(self):
        return self.athletics

    # Retrieve related or summarized values

    def merit_value(self, merit_name):
        qs = self.merits.filter(merit__name=merit_name)
        return qs.first().rating

    def splats(self):
        results = []
        for category in self.template.splat_categories.all():
            results.append((category.name, getattr(self, category.storage_column())))
        return results

    def attributes_total(self):
        return sum(int(getattr(self, k)) for k in ATTRIBUTE_KEYS)

    def skills_total(self):
        return sum(int(getattr(self, k)) for k in SKILL_KEYS)

    @missing(0)
    def experiences_gained(self):
        return int(self.experience_awards.aggregate(Sum('experience'))['experience__sum'])

    @missing(0)
    def experiences_used(self):
        return int(self.approval_requests.filter(status='complete').aggregate(x=Sum('total_experience_cost'))['x'])

    def experiences(self):
        return self.experiences_gained() - self.experiences_used()

    # The following methods are useful to have around for template rendering

    @missing("Virtue")
    def primary_anchor_name(self):
        return self.template.primary_anchor_name

    @missing("Vice")
    def secondary_anchor_name(self):
        return self.template.secondary_anchor_name

    def attributes(self):
        return {v: getattr(self, k) for k, v in settings.ATTRIBUTES}

    def attribute_sections(self):
        section = []
        for k, v in settings.ATTRIBUTES:
            section.append((v, getattr(self, k)))
            if len(section) == 3:
                yield section
                section = []

    def __getattribute__(self, name: str):
        if '_specialties' in name:
            skill = name.split('_specialties')[0]
            return self.get_skill_specialities(skill)
        return super().__getattribute__(name)

    def get_skill_specialities(self, skill):
        qs = self.specialities.filter(skill=skill)
        if qs.exists():
            return ', '.join(qs.values_list('speciality', flat=True))
        else:
            return ''

    def powers_by_category(self):
        categories = []
        for category in self.template.power_categories.all():
            powers = [p for p in self.powers.filter(power__power_category=category)]
            if powers:
                categories.append((category.name, powers))
        return categories

    def anchors_by_category(self):
        categories = []
        for category in self.template.template_anchors.all():
            anchors = [p for p in self.anchors.filter(template_anchor=category)]
            if anchors:
                categories.append((category.name, anchors))
        return categories

    def skill_sections(self):
        section = []
        for k, v in settings.SKILLS:
            section.append((v, getattr(self, k), self.get_skill_specialities(k)))
            if len(section) == 8:
                yield section
                section = []

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
        for cls in self.get_character_elements():
            cls.objects.filter(character_id=old_pk).update(id=None, character_id=self.pk)

        # Move pending approval requests and experience awards to new revision
        for cls in self.get_character_trackers():
            cls.objects.filter(uuid=self.uuid).update(character=self)

        # Return a redirect to new revision
        return redirect('admin:sheets_character_change', object_id=self.pk)

    @staticmethod
    def get_character_elements():
        return CharacterMerit, CharacterPower, SkillSpeciality

    @staticmethod
    def get_character_trackers():
        return ApprovalRequest, Advancement, DowntimeAction, ResourceTracker, HealthTracker

    def reset_derived_traits(self):
        self.size = 5
        self.speed = (5 + self.strength + self.dexterity)
        self.initiative = (self.dexterity + self.composure)
        self.resource_max = (self.resource_max * 2)
        self.resource_start = self.resource_start // 2
        self.health_boxes = self.size + self.stamina
        self.willpower_max = self.resolve + self.composure

    def update_derived_traits(self):
        self.size = self.size or 5
        self.speed = self.speed or (5 + self.strength + self.dexterity)
        self.initiative = self.initiative or (self.dexterity + self.composure)
        self.resource_max = self.resource_max or 8 + (self.resource_max * 2)
        self.resource_start = self.resource_start or self.resource_start // 2
        self.health_boxes = self.health_boxes or self.size + self.stamina
        self.willpower_max = self.willpower_max or self.resolve + self.composure

    def save(self, **kwargs):
        self.update_derived_traits()

        # When a sheet becomes approved, all other approved sheets for the same character are archived
        if self.status == 'approved':
            self.revisions().filter(status='approved').update(status='archived')
            self.approval_requests.filter(status='pending').update(status='complete')
        super().save(**kwargs)

        # Stuff that needs to happen after the original charcter is already saved
        self.create_or_update_resources()

    def main_resource(self) -> 'ResourceTracker':
        return self.resources.filter(name=self.template.resource_name).first()

    def willpower(self) -> 'ResourceTracker':
        return self.resources.filter(name='Willpower').first()

    def create_or_update_resources(self):
        resource_name = self.template.resource_name
        if resource_name:
            self._create_or_update_resource(
                cls=ResourceTracker,
                field=self.main_resource(),
                capacity=self.resource_max,
                current=self.resource_max,
                name=resource_name,
            )

        self._create_or_update_resource(
            cls=ResourceTracker,
            field=self.willpower(),
            capacity=self.willpower_max,
            current=self.willpower_max,
            name='Willpower',
        )

        self._create_or_update_resource(
            cls=HealthTracker,
            field='health',
            capacity=self.health_boxes
        )

    def _create_or_update_resource(self, cls, field, capacity, **kwargs):
        params = {'character': self, 'capacity': capacity, **kwargs}
        if isinstance(field, str):
            field = getattr(self, field, None)
        if not field:
            cls.objects.create(**params)
        else:
            if capacity != field.capacity:
                field.capacity = capacity
                field.save()

    def revisions(self):
        return Character.objects.filter(uuid=self.uuid).order_by('version')

    def approval_history(self):
        return ApprovalRequest.objects.filter(uuid=self.uuid).order_by('character__version')

    @classmethod
    def request_initial_approval(cls, user, chronicle, name, template, description=None, attachment=None):
        obj = cls.objects.create(
            name=name,
            user=user,
            template=template,
            chronicle=chronicle,
            player_notes=description,
        )
        approval = obj.request_approval(attachment)
        return obj, approval

    def request_approval(self, attachment=None):
        approval = ApprovalRequest.objects.create(character=self, detail='New Character')
        if attachment:
            approval.add_attachment(attachment)
        return approval

    # Randomize character creation process
    def can_randomize(self, user=None):
        return self.status != 'approved'

    def randomize(self, user=None):
        attr_dots = max(settings.INITIAL_ATTRIBUTE_DOTS - self.attributes_total(), 0)
        self.add_random_traits(settings.ATTRIBUTE_KEYS, attr_dots)

        skill_dots = max(settings.INITIAL_SKILL_DOTS - self.skills_total(), 0)
        self.add_random_traits(settings.SKILL_KEYS, skill_dots)

        self.reset_derived_traits()
        self.save()

    def add_random_traits(self, traits, dots) -> None:
        while dots > 0:
            trait = random.choice(traits)
            trait_value = getattr(self, trait)
            if trait_value < max(5, self.power_stat):
                setattr(self, trait, trait_value + 1)
                dots -= 1


# There are 2 kinds of models related to Character: CharacterTrackers and CharacterElements
# CharacterElements get copied anew with every revision of the character
# CharacterTrackers get moved to the new revision of the character when its created


class CharacterElement(Model):
    character = None
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
        ordering = ('merit__name', )

    def __str__(self):
        return f'{self.merit.name} ({self.rating})'

    def clean(self):
        super().clean()
        if self.merit.variants.exists():
            if not self.merit.variants.filter(dots=self.rating).exists():
                raise ValidationError(f'Not valid, legal values: {self.merit.get_variants_display()}')


class CharacterPower(CharacterElement):
    character = ForeignKey(Character, CASCADE, related_name='powers')
    power = ForeignKey(Power, PROTECT, related_name='+')
    rating = DotsField(default=1, number=5, clear=False)
    details = CharField(max_length=200, blank=True)
    power_option = ForeignKey(PowerOption, CASCADE, blank=True, null=True, verbose_name='Option', related_name='+')

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


class CharacterAnchor(CharacterElement):
    character = ForeignKey(Character, CASCADE, related_name='anchors')
    template_anchor = ForeignKey(TemplateAnchor, PROTECT, related_name='+')
    value = TextField()

    class Meta:
        verbose_name = "Anchor"

    def __str__(self):
        return str(self.template_anchor.name)


class CharacterTracker(Model):
    character = None
    uuid = UUIDField(editable=False, db_index=True, null=True)

    class Meta:
        abstract = True

    def save(self, **kwargs):
        self.uuid = self.character.uuid
        super().save(**kwargs)


class ApprovalRequest(TimeStampedModel, StatusModel, CharacterTracker):

    # When the user sends a request that requires spending Experience, one must be chosen
    # Should be left blank for other kinds of requests

    STATUS = Choices(
        ('pending', 'Pending'),
        ('complete', 'Complete'),
    )

    character = ForeignKey(Character, CASCADE, related_name='approval_requests')
    user = ForeignKey(settings.AUTH_USER_MODEL, DO_NOTHING, null=True, related_name='approval_requests')

    base_experience_cost = PositiveSmallIntegerField(
        'Exp. Cost', default=0, help_text="Base Experience cost based on the trait type.")
    quantity = PositiveSmallIntegerField(
        default=1, help_text="Number of total instances being requested.")
    total_experience_cost = PositiveSmallIntegerField(
        default=0, editable=False, help_text="Total Experiences cost. Calculated automatically.")
    detail = CharField(
        max_length=100, blank=True,
        help_text="Specific trait or approval you are requesting.")
    additional_info = TextField('Additional Information', blank=True)
    prestige_level = PositiveSmallIntegerField(
        default=0, help_text="Specifies that this request is for a Prestige reward.")

    attachment = BinaryField(blank=True)
    attachment_content_type = CharField(max_length=100, blank=True)
    attachment_filename = CharField(max_length=256, blank=True)

    class Meta:
        verbose_name = "Approval Request"

    def __str__(self):
        return f'#{self.pk}'

    def is_prestige(self):
        return bool(self.prestige_level)

    def add_attachment(self, attachment):
        try:
            self.attachment = attachment.read()
            self.attachment_content_type = attachment.content_type
            filename, extension = os.path.splitext(attachment.name)
            self.attachment_filename = f'{self.character.name}{extension}'
            self.save()
        except RuntimeError:
            logger.exception('Problem saving attachment.')

    def save(self, **kwargs):
        if not self.user and self.character.user:
            self.user = self.character.user
        self.total_experience_cost = self.base_experience_cost * self.quantity
        super().save(**kwargs)

    def download_attachment_link(self):
        if not self.attachment:
            return 'Not Available'
        url = reverse('download-attachment', kwargs={'approval': self.pk})
        return format_html('<a href="{}">Download</a>', url)

    download_attachment_link.short_description = 'Attachment'

    def get_character_link(self, full=False):
        return self.character.get_admin_link(full)

    def cost(self):
        result = []
        if self.prestige_level:
            result.append(f'Prestige Level {self.prestige_level}')
        if self.base_experience_cost:
            result.append(f'{self.base_experience_cost} x {self.quantity} = {self.total_experience_cost} Experience')
        if not result:
            return 'None'
        return ', '.join(result)


class Advancement(TimeStampedModel, CharacterTracker):
    game_event = ForeignKey('organization.GameEvent', CASCADE, related_name='experience_awards')
    character = ForeignKey('sheets.Character', CASCADE, related_name='experience_awards')
    experience = PositiveSmallIntegerField(default=0)
    beats = PositiveSmallIntegerField(default=0)
    notes = CharField(max_length=400, blank=True)

    def __str__(self):
        return f'{self.character.name}'


class DowntimeAction(TimeStampedModel, CharacterTracker):
    game_event = ForeignKey('organization.GameEvent', CASCADE, related_name='downtime_actions')
    character = ForeignKey('sheets.Character', CASCADE, related_name='downtime_actions')
    player_request = TextField()
    storyteller_response = TextField(blank=True)

    class Meta:
        verbose_name = "Downtime Action"


class ResourceTracker(CharacterTracker):
    character = ForeignKey('sheets.Character', CASCADE, related_name='resources')
    name = CharField(max_length=40, editable=False)
    capacity = PositiveSmallIntegerField(default=10)
    current = PositiveSmallIntegerField(default=10)

    class Meta:
        unique_together = ('name', 'character')
        verbose_name = 'Resource'

    def __str__(self):
        return self.name

    def range_boxes(self):
        return ((i, i <= self.current) for i in range(1, self.capacity + 1))


class HealthTracker(Model):
    character = OneToOneField('sheets.Character', CASCADE, related_name='health')
    capacity = PositiveSmallIntegerField(default=10)
    bashing_damage = PositiveSmallIntegerField(default=0)
    lethal_damage = PositiveSmallIntegerField(default=0)
    aggravated_damage = PositiveSmallIntegerField(default=0)
    resistant_damage = PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = 'Health'
        verbose_name_plural = 'Health'

    def __str__(self):
        return 'Health'

    def range_boxes(self):
        return ((i, self.get_box(i)) for i in range(1, self.capacity + 1))

    def get_box(self, i: int) -> str:
        if self.aggravated_damage >= i:
            return 'A'
        if self.lethal_damage + self.aggravated_damage >= i:
            return 'L'
        if self.bashing_damage + self.lethal_damage + self.aggravated_damage >= i:
            return 'B'
        return 'N'

    def total_damage(self):
        return int(self.aggravated_damage + self.lethal_damage + self.bashing_damage)

    def take_action(self, action):
        aggravated = int(self.aggravated_damage)
        lethal = int(self.lethal_damage)
        bashing = int(self.bashing_damage)
        boxes = int(self.capacity)

        # First apply the requested action
        if action == '+A':
            aggravated += 1
        elif action == '+L':
            lethal += 1
        elif action == '+B':
            bashing += 1
        elif action == '-A' and aggravated > 0:
            aggravated -= 1
        elif action == '-L' and lethal > 0:
            lethal -= 1
        elif action == '-B' and bashing > 0:
            bashing -= 1
        else:
            return  # Action was not valid

        # Correct or switch damage type as needed
        while aggravated + lethal + bashing > boxes:
            if bashing > 0:
                bashing = max(bashing - 2, 0)
                lethal += 1
            elif lethal > 0:
                lethal = max(lethal - 2, 0)
                aggravated += 1

        self.aggravated_damage = min(aggravated, boxes)
        self.lethal_damage = lethal
        self.bashing_damage = bashing
        self.save()
