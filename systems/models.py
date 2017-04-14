from django.db import models


class CharacterTemplate(models.Model):
    name = models.CharField(max_length=20)
    alias = models.CharField(max_length=20, blank=True)
    integrity_name = models.CharField(max_length=20, verbose_name="Integrity", default="Integrity")
    power_stat_name = models.CharField(max_length=20, verbose_name="Power Stat")
    resource_name = models.CharField(max_length=20, verbose_name="Resource")
    primary_anchor_name = models.CharField(max_length=20, verbose_name="Primary Anchor", default="Virtue")
    secondary_anchor_name = models.CharField(max_length=20, verbose_name="Secondary Anchor", default="Vice")
    character_group_name = models.CharField(max_length=20, verbose_name="Group Name", default="Group")

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Template"


class Splat(models.Model):
    FLAVOR = (
        ('1', 'Primary (Nature)'),
        ('2', 'Secondary (Faction)'),
        ('3', 'Tertiary (Attained)'),
    )
    name = models.CharField(max_length=20)
    template = models.ForeignKey(CharacterTemplate, on_delete=models.CASCADE, related_name='splat_categories')
    flavor = models.CharField(max_length=10, choices=FLAVOR, null=True)

    class Meta:
        ordering = ('template', 'flavor', )

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


class SplatOption(models.Model):
    name = models.CharField(max_length=40)
    category = models.ForeignKey(Splat, on_delete=models.CASCADE, related_name='splats')

    class Meta:
        ordering = ('category', 'name', )

    def __str__(self):
        return str(self.name)

    def template(self):
        return self.category.template


class Merit(models.Model):
    CATEGORIES = (
        ('mental', 'Mental'),
        ('physical', 'Physical'),
        ('social', 'Social'),
        ('supernatural', 'Supernatural'),
        ('style', 'Style'),
    )
    name = models.CharField(max_length=40, unique=True)
    template = models.ForeignKey('CharacterTemplate', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return str(self.name)


class PowerCategory(models.Model):
    name = models.CharField(max_length=20)
    template = models.ForeignKey('CharacterTemplate', on_delete=models.PROTECT, related_name='power_categories', null=True)

    class Meta:
        verbose_name = "Power Category"
        verbose_name_plural = "Power Categories"

    def __str__(self):
        return str(self.name)

    def power_names(self):
        return ', '.join(self.powers.values_list('name', flat=True))


class Power(models.Model):
    name = models.CharField(max_length=40)
    category = models.ForeignKey('PowerCategory', on_delete=models.PROTECT, related_name='powers')

    class Meta:
        unique_together = ('name', 'category', )
        ordering = ('category', 'name', )

    def __str__(self):
        return str(self.name)


class AnchorCategory(models.Model):
    name = models.CharField(max_length=20)
    template = models.ForeignKey(CharacterTemplate, on_delete=models.CASCADE, related_name='anchor_categories')
    is_required = models.BooleanField(default=False)
    description = models.TextField()

    class Meta:
        verbose_name = "Anchor Category"
        verbose_name_plural = "Anchor Categories"

    def __str__(self):
        return str(self.name)


__all__ = (
    "CharacterTemplate",
    "Splat",
    "SplatOption",
    "Merit",
    "PowerCategory",
    "Power",
    "AnchorCategory",
)