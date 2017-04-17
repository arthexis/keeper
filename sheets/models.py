from django.db.models import *
from django.contrib.auth.models import User, Group
from systems.fields import *
from systems.models import *
from orgs.models import *
from systems.fields import DotsField


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


class Character(Model):

    # Character basic info
    name = CharField(max_length=40, verbose_name="Character")
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
    primary_splat = ForeignKey(SplatOption, PROTECT, related_name='+', null=True, blank=True)
    secondary_splat = ForeignKey(SplatOption, PROTECT, related_name='+', null=True, blank=True)
    tertiary_splat = ForeignKey(SplatOption, PROTECT, related_name='+', null=True, blank=True)

    # Character Advancement related
    beats = DotsField()
    experiences = PositiveIntegerField(default=0)
    template_beats = DotsField()
    template_experiences = PositiveIntegerField(default=0)

    # Organization related fields
    user = ForeignKey(
        User, DO_NOTHING, null=True, blank=True, related_name='characters')
    organization = ForeignKey(Organization, CASCADE, null=True, blank=True)
    created_on = DateField(auto_now_add=True, editable=False)
    modified_on = DateField(auto_now=True, editable=False)

    # Derived traits, they are not handled automatically because in some situations
    # their values can be manually adjusted
    size = DotsField(default=5, clear=False)
    health_levels = PositiveIntegerField(default=0)
    willpower = DotsField(default=1, clear=False)

    # Character Anchors (ie. Virtue / Vice)
    primary_anchor = CharField(max_length=40, blank=True)
    secondary_anchor = CharField(max_length=40, blank=True)

    # Derived Traits

    def speed(self):
        return 5 + self.strength + self.dexterity

    def initiative(self):
        return self.dexterity + self.composure

    def defense(self):
        return min((self.dexterity, self.wits)) + self.defense_skill()

    def defense_skill(self):
        return self.athletics

    def health(self):
        return self.size + self.stamina

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


class CharacterElement(Model):

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
        return self.merit.template.name if self.merit.template else 'Any'

    def __str__(self):
        return '{} ({})'.format(self.merit.name, self.rating)


class CharacterPower(CharacterElement):
    character = ForeignKey(Character, CASCADE, related_name='powers')
    power = ForeignKey(Power, PROTECT, related_name='+')
    rating = DotsField(default=1, clear=False)
    details = CharField(max_length=200, blank=True)

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
    character = ForeignKey(Character, CASCADE, related_name='specialities')
    skill = CharField(max_length=20, choices=SKILLS)
    speciality = CharField(max_length=200)

    def __str__(self):
        return "{} ({})".format(self.speciality, self.get_skill_display())

    class Meta:
        verbose_name = "Skill Speciality"
        verbose_name_plural = "Skill Specialities"


__all__ = (
    "Character",
    "CharacterMerit",
    "CharacterPower",
    "SkillSpeciality",
)
