from django.contrib.auth.models import User

from systems.fields import *
from systems.models import *


# Create your models here.
class Character(models.Model):

    # Character basic info
    name = models.CharField(max_length=40, verbose_name="Character Name")
    template = models.ForeignKey(Template, on_delete=models.PROTECT, verbose_name="Supernatural Template")
    power_stat = DotsField(default=1, clear=False)
    integrity = DotsField(default=7)
    background = models.TextField(blank=True)
    resource = models.PositiveIntegerField(default=10)

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
    primary_splat = models.ForeignKey(SplatOption, on_delete=models.PROTECT, related_name='+', null=True, blank=True)
    secondary_splat = models.ForeignKey(SplatOption, on_delete=models.PROTECT, related_name='+', null=True, blank=True)
    tertiary_splat = models.ForeignKey(SplatOption, on_delete=models.PROTECT, related_name='+', null=True, blank=True)

    # Character Advancement related
    beats = DotsField()
    experiences = models.PositiveIntegerField(default=0)
    template_beats = DotsField()
    template_experiences = models.PositiveIntegerField(default=0)

    # Organization related fields
    player = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='characters')
    storyteller = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='+')
    version = models.PositiveIntegerField(default=0)
    created_on = models.DateField(auto_now_add=True)
    modified_on = models.DateField(auto_now=True)
    is_approved = models.BooleanField(default=False)
    approved_on = models.DateField(null=True)
    is_retired = models.BooleanField(default=False)

    # Derived traits, they are not handled automatically because in some situations
    # their values can be manually adjusted
    health_levels = models.PositiveIntegerField(default=0)
    willpower = DotsField(default=1, clear=False)

    # Character Anchors (ie. Virtue / Vice)
    primary_anchor = models.CharField(max_length=40, blank=True)
    secondary_anchor = models.CharField(max_length=40, blank=True)

    def __str__(self):
        return str(self.name)


class CharacterMerit(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='merits')
    merit = models.ForeignKey(Merit, on_delete=models.PROTECT, related_name='+')
    rating = DotsField(default=1, clear=False)
    notes = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Merit"

    def category(self):
        return self.merit.get_category_display()

    def origin(self):
        return self.merit.template.name if self.merit.template else 'Any'

    def __str__(self):
        return '{} ({})'.format(self.merit.name, self.rating)


class CharacterPower(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='powers')
    power = models.ForeignKey(Power, on_delete=models.PROTECT, related_name='+')
    rating = DotsField(default=1, clear=False)

    class Meta:
        verbose_name = "Power"

    def __str__(self):
        return '{}: {} ({})'.format(self.category(), self.power.name, self.rating)

    def category(self):
        return self.power.category.name



