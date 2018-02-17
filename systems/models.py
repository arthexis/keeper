import logging

from django.db import models
from django.db.models import SET_NULL, CASCADE
from model_utils import Choices

logger = logging.getLogger(__name__)


__all__ = (
    "CharacterTemplate",
    "SplatCategory",
    "Splat",
    "Merit",
    "PowerCategory",
    "Power",
    "AnchorCategory",
)


class ReferenceBook(models.Model):
    name = models.CharField(max_length=100)
    reference_code = models.SlugField('Code', max_length=10, unique=True)

    class Meta:
        verbose_name = "Reference Book"


class CharacterTemplate(models.Model):
    name = models.CharField(max_length=20)
    game_line = models.CharField(max_length=20)
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
        return str(self.name)


class SplatCategory(models.Model):
    FLAVOR = Choices(
        ('1', 'Primary: Nature'),
        ('2', 'Secondary: Faction'),
        ('3', 'Tertiary: Attained'),
    )
    name = models.CharField(max_length=20)
    character_template = models.ForeignKey(
        CharacterTemplate, on_delete=models.CASCADE, related_name='splat_categories')
    flavor = models.CharField(max_length=1, choices=FLAVOR, null=True)

    class Meta:
        ordering = ('character_template', 'flavor', )
        verbose_name = ('Splat Category')
        verbose_name_plural = ('Splat Categories')

    def __str__(self):
        return str(self.name)

    def splat_names(self):
        return ', '.join(self.splats.values_list('name', flat=True))

    def storage_column(self):
        if self.flavor == '1':
            return 'primary_splat'
        elif self.flavor == '2':
            return 'secondary_splat'
        elif self.flavor == '3':
            return 'tertiary_splat'


class Splat(models.Model):
    name = models.CharField(max_length=40)
    splat_category = models.ForeignKey(
        SplatCategory, on_delete=models.CASCADE, related_name='splats')

    class Meta:
        ordering = ('splat_category', 'name', )

    def __str__(self):
        return str(self.name)

    def template(self):
        return self.splat_category.character_template


class Merit(models.Model):
    CATEGORIES = Choices(
        ('mental', 'Mental'),
        ('physical', 'Physical'),
        ('social', 'Social'),
        ('supernatural', 'Supernatural'),
        ('style', 'Style'),
        ('other', 'Other')
    )
    name = models.CharField(max_length=40, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    character_template = models.ForeignKey(
        'CharacterTemplate', on_delete=models.CASCADE, null=True, blank=True, related_name='+',
        verbose_name='Template Restriction', help_text='Optional. Restricts Merit to specific a Template.'
    )

    reference_code = models.SlugField('Code', unique=True)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return str(self.name)


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

    origin_splat = models.ForeignKey('Splat', SET_NULL, related_name='+', null=True)

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

