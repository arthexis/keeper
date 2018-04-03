import logging

from django.db import models
from django.db.models import CASCADE, CharField, SlugField, PositiveSmallIntegerField
from model_utils import Choices

logger = logging.getLogger(__name__)


__all__ = (
    "CharacterTemplate",
    "SplatCategory",
    "Splat",
    "PowerCategory",
    "PowerOption",
    "Merit",
    "Power",
    "TemplateAnchor",
)


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

    # Used for seed data storage
    reference_code = models.SlugField('Code', unique=True)

    class Meta:
        verbose_name = "Character Template"
        ordering = ('name', 'game_line')

    def __str__(self):
        return f'{self.name} [{self.game_line.upper()}]'

    def get_experience_costs(self):
        costs = [
            (4, 'Attribute +1 = 4 XP'),
            (2, 'Skill +1 = 2 XP'),
            (1, 'Speciality = 1 XP'),
            (1, 'Merit = 1 XP per dot'),
            (5, f'{self.power_stat_name} +1 = 5 XP'),
            (2, f'{self.integrity_name} +1 = 2 XP'),
            (1, 'Recover 1 Willpower = 1 XP'),
        ]
        for pc in self.power_categories.all():
            if pc.experience_splat_cost and pc.splat_discount_name:
                costs.append((
                    pc.experience_splat_cost,
                    f'{pc.name} +1 ({pc.splat_discount_name}) = {pc.base_experience_cost} XP'
                ))
                costs.append((pc.experience_cost, f'{pc.name} +1 (Others) = {pc.base_experience_cost} XP'))
            else:
                costs.append((pc.experience_cost, f'{pc.name} +1 = {pc.base_experience_cost} XP'))
        costs.append((0, 'Prestige / Other = 0 XP'))
        return costs


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
    splat_category = models.ForeignKey(SplatCategory, on_delete=models.CASCADE, related_name='splats')

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


class PowerCategory(models.Model):
    name = models.CharField(max_length=20)
    character_template = models.ForeignKey(
        'CharacterTemplate', on_delete=models.CASCADE, related_name='power_categories', null=True)

    experience_cost = PositiveSmallIntegerField(default=4)
    experience_splat_cost = PositiveSmallIntegerField(default=0)
    splat_discount_name = CharField(max_length=20, blank=True)

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

    def character_template(self):
        return str(self.power_category.character_template.name)


class PowerOption(models.Model):
    name = models.CharField(max_length=40)
    power_category = models.ForeignKey('PowerCategory', CASCADE, related_name='power_options')

    class Meta:
        unique_together = ('name', 'power_category',)
        ordering = ('power_category', 'name',)

    def __str__(self):
        return str(self.name)


class TemplateAnchor(models.Model):
    name = models.CharField(max_length=20)
    character_template = models.ForeignKey(
        CharacterTemplate, on_delete=models.CASCADE, related_name='template_anchors')

    class Meta:
        verbose_name = "Template Anchor"
        verbose_name_plural = "Template Anchors"

    def __str__(self):
        return str(self.name)
