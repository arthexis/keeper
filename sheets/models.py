import logging

from django.db.models import Model, CharField, ForeignKey, TextField, PositiveIntegerField, DateField, \
    PROTECT, DO_NOTHING, CASCADE, BooleanField, F, Manager
from django.contrib.auth.models import User, Group
from model_utils.managers import InheritanceManager, QueryManager

from orgs.models import Organization
from systems.models import CharacterTemplate, Splat, Power, Merit
from systems.fields import DotsField
from model_utils import Choices

logger = logging.getLogger(__name__)


__all__ = (
    "Character",
    "CharacterMerit",
    "CharacterPower",
    "SkillSpeciality",
)


SKILLS = Choices(
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


ATTRIBUTES = Choices(
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


class Character(Model):

    # Character basic info
    name = CharField(max_length=40, verbose_name="Character Name")
    template = ForeignKey(CharacterTemplate, PROTECT)
    power_stat = DotsField(default=1, clear=False)
    integrity = DotsField(default=7)
    background = TextField(blank=True)
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
    secondary_splat = ForeignKey(Splat, PROTECT, related_name='+', null=True, blank=True)
    tertiary_splat = ForeignKey(Splat, PROTECT, related_name='+', null=True, blank=True)

    # Character Advancement related
    beats = PositiveIntegerField(default=0)
    experiences = PositiveIntegerField(default=0)
    template_beats = DotsField()
    template_experiences = PositiveIntegerField(default=0)

    # Organization related fields
    user = ForeignKey(
        User, DO_NOTHING, null=True, blank=True, related_name='characters')
    organization = ForeignKey(Organization, CASCADE, null=True, blank=True)
    created_on = DateField(auto_now_add=True, editable=False)
    modified_on = DateField(auto_now=True, editable=False)

    # Derived traits, they are not handled automatically because
    # their values can be manually adjusted
    size = DotsField(default=5, clear=False)
    health_levels = PositiveIntegerField(default=0)
    damage_track = CharField(max_length=100, blank=True, null=True)
    willpower = PositiveIntegerField(blank=True, null=True)
    willpower_max = PositiveIntegerField(blank=True, null=True, editable=False)
    perm_willpower_spent = PositiveIntegerField(blank=True, null=True)

    # Character Anchors (ie. Virtue / Vice)
    primary_anchor = CharField(max_length=40, blank=True)
    secondary_anchor = CharField(max_length=40, blank=True)

    version = PositiveIntegerField(default=0)
    is_active = BooleanField(default=True)

    objects = Manager()
    active = QueryManager(is_active=True)

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

    def create_revision(self):
        self.is_active = False
        self.save()

        # By removing the PK a new instance is created on save()
        old_pk, self.pk, self.is_active = self.pk, None, True
        self.version = F('version') + 1
        self.save()
        for cls in (CharacterMerit, CharacterPower, SkillSpeciality):
            for elem in cls.objects.filter(character_id=old_pk):
                elem.pk, elem.character_id = None, self.pk
                elem.save()


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
        return '{} {}'.format(self.power.name, self.rating)

    def category(self):
        return self.power.power_category.name


class SkillSpeciality(CharacterElement):
    character = ForeignKey(Character, CASCADE, related_name='specialities')
    skill = CharField(max_length=20, choices=SKILLS)
    speciality = CharField(max_length=200)

    def __str__(self):
        return "{} ({})".format(self.speciality, self.get_skill_display())

    class Meta:
        verbose_name = "Skill Speciality"
        verbose_name_plural = "Skill Specialities"



