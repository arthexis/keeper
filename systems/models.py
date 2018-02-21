import logging

from django.db import models
from django.db.models import CASCADE, CharField, PositiveSmallIntegerField, ForeignKey, SlugField
from model_utils import Choices

logger = logging.getLogger(__name__)


__all__ = (
    "SKILLS",
    "SKILL_KEYS",
    "ATTRIBUTES",
    "ATTRIBUTE_KEYS",
    "CharacterTemplate",
    "SplatCategory",
    "Splat",
    "PowerCategory",
    "Merit",
    "Power",
    "AnchorCategory",
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

ATTRIBUTE_KEYS = [k for k, _ in ATTRIBUTES]

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

SKILL_KEYS = [k for k, _ in SKILLS]


class ReferenceBook(models.Model):
    name = models.CharField(max_length=100)
    reference_code = models.SlugField('Code', max_length=10, unique=True)

    class Meta:
        verbose_name = "Reference Book"


class CharacterTemplate(models.Model):
    GAME_LINES = Choices(
        ('gmc', 'God Machine Chronicles'),
        ('vtr', 'Vampire the Requiem'),
        ('ctl', 'Changeling the Lost'),
        ('mtaw', 'Mage the Awakening'),
        ('wtf', 'Werewolf the Forsaken'),
        ('gts', 'Geist the Sin-Eaters'),
    )

    name = models.CharField(max_length=20)
    game_line = models.CharField(max_length=20, choices=GAME_LINES)
    integrity_name = models.CharField(
        max_length=20, verbose_name="Integrity", default="Integrity", blank=True)
    power_stat_name = models.CharField(max_length=20, verbose_name="Power Stat", blank=True)
    resource_name = models.CharField(max_length=20, verbose_name="Resource", blank=True)
    primary_anchor_name = models.CharField(
        max_length=20, verbose_name="Primary Anchor", default="Virtue", blank=True)
    secondary_anchor_name = models.CharField(
        max_length=20, verbose_name="Secondary Anchor", default="Vice", blank=True)
    character_group_name = models.CharField(
        max_length=20, verbose_name="Group Name", default="Group", blank=True)
    experiences_prefix = models.CharField(
        max_length=20, verbose_name="Experiences Prefix", blank=True, null=True)

    # Used for seed data storage
    reference_code = models.SlugField('Code', unique=True)

    class Meta:
        verbose_name = "Character Template"
        ordering = ('name', 'game_line')

    def __str__(self):
        return f'{self.name} [{self.game_line.upper()}]'


class SplatCategory(models.Model):
    FLAVORS = Choices(
        ('primary', 'Primary Kind'),
        ('primary_sub', 'Secondary Kind'),
        ('secondary', 'Major Faction'),
        ('secondary_sub', 'Minor Faction'),
        ('tertiary', 'Tertiary Kind'),
    )
    name = models.CharField(max_length=20)
    character_template = models.ForeignKey(
        CharacterTemplate, on_delete=models.CASCADE, related_name='splat_categories')
    flavor = models.CharField(max_length=20, choices=FLAVORS)
    is_required = models.BooleanField(default=False)

    class Meta:
        unique_together = ('character_template', 'flavor')
        ordering = ('character_template', 'flavor', )
        verbose_name = ('Splat Category')
        verbose_name_plural = ('Splat Categories')

    def __str__(self):
        return str(self.name)

    def splat_names(self):
        return ', '.join(self.splats.values_list('name', flat=True))

    def storage_column(self):
        return f'{self.flavor}_splat'


class Splat(models.Model):
    name = models.CharField(max_length=40)
    splat_category = models.ForeignKey(
        SplatCategory, on_delete=models.CASCADE, related_name='splats')

    class Meta:
        unique_together = ('name', 'splat_category')
        ordering = ('splat_category', 'name', )

    def __str__(self):
        return str(self.name)

    def template(self):
        return self.splat_category.character_template


class Merit(models.Model):
    name = CharField(max_length=40, unique=True)
    reference_code = SlugField('Code', unique=True)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return str(self.name)


class Prerequisite(models.Model):
    pass


class AttributePrerequisite(Prerequisite):
    attribute = CharField(max_length=20, choices=ATTRIBUTES)
    min_value = PositiveSmallIntegerField()
    merit = ForeignKey(Merit, CASCADE, related_name='attribute_prerequisites')


class PowerCategory(models.Model):
    name = models.CharField(max_length=20)
    character_template = models.ForeignKey(
        'CharacterTemplate', on_delete=models.CASCADE, related_name='power_categories', null=True)

    class Meta:
        verbose_name = "Power Category"
        verbose_name_plural = "Power Categories"

    def __str__(self):
        return str(self.name)

    def power_names(self):
        return ', '.join(self.powers.values_list('name', flat=True))


class Power(models.Model):
    name = models.CharField(max_length=40)
    power_category = models.ForeignKey('PowerCategory', CASCADE, related_name='powers')

    class Meta:
        unique_together = ('name', 'power_category', )
        ordering = ('power_category', 'name', )

    def __str__(self):
        return str(self.name)


class AnchorCategory(models.Model):
    name = models.CharField(max_length=20)
    character_template = models.ForeignKey(
        CharacterTemplate, on_delete=models.CASCADE, related_name='anchor_categories')
    is_required = models.BooleanField(default=False)
    description = models.TextField()

    class Meta:
        verbose_name = "Anchor Category"
        verbose_name_plural = "Anchor Categories"

    def __str__(self):
        return str(self.name)

