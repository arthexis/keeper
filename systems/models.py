from django.db import models
from systems.fields import DotsField


class Template(models.Model):
    name = models.CharField(max_length=20)
    alias = models.CharField(max_length=20, blank=True)
    integrity_name = models.CharField(max_length=20, verbose_name="Integrity")
    power_stat_name = models.CharField(max_length=20, verbose_name="Power Stat")
    resource_name = models.CharField(max_length=20, verbose_name="Resource")

    def __str__(self):
        return str(self.name)


class SplatCategory(models.Model):
    name = models.CharField(max_length=20)
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name='splat_categories')
    is_required = models.BooleanField('Splat is required on creation', default=False)
    is_editable = models.BooleanField('Splat can be changed after assigned', default=True)

    class Meta:
        verbose_name = 'Splat Category'
        verbose_name_plural = 'Splat Categories'

    def __str__(self):
        return str(self.name)

    def splat_names(self):
        return ', '.join(self.splats.values_list('name', flat=True))


class Splat(models.Model):
    name = models.CharField(max_length=40)
    category = models.ForeignKey(SplatCategory, on_delete=models.CASCADE, related_name='splats')
    alias = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    is_playable = models.BooleanField(default=True)

    class Meta:
        ordering = ('category', 'name', )

    def __str__(self):
        return str(self.name)

    def template(self):
        return self.category.template


# Note that there can be multiple versions of the same merit with different dots
class Merit(models.Model):
    name = models.CharField(max_length=40)
    is_style = models.BooleanField(default=False)
    description = models.TextField()
    template = models.ForeignKey('Template', on_delete=models.CASCADE, null=True)
    dots = DotsField()

    class Meta:
        unique_together = ('name', 'dots')

    def __str__(self):
        return str(self.name)


class PowerCategory(models.Model):
    name = models.CharField(max_length=20)
    template = models.ManyToManyField('Template', related_name='powers')

    class Meta:
        verbose_name = "Power Category"
        verbose_name_plural = "Power Categories"

    def __str__(self):
        return str(self.name)


# Just like for Merits, each level of a Power is its own record with different dots
class Power(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField(blank=True)
    category = models.ForeignKey('PowerCategory', on_delete=models.PROTECT, related_name='powers')
    dots = DotsField()

    class Meta:
        unique_together = ('name', 'category', 'dots')

    def __str__(self):
        return str(self.name)


class AnchorCategory(models.Model):
    name = models.CharField(max_length=20)
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name='anchor_categories')
    is_required = models.BooleanField(default=False)
    description = models.TextField()

    class Meta:
        verbose_name = "Anchor Category"
        verbose_name_plural = "Anchor Categories"

    def __str__(self):
        return str(self.name)


