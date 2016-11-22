from django.contrib.auth.models import User

from systems.fields import *
from systems.models import *


# Create your models here.
class Character(models.Model):

    # Character basic info
    name = models.CharField(max_length=40)
    template = models.ForeignKey(Template, on_delete=models.PROTECT)
    power_stat = DotsField(default=1)
    integrity = DotsField(default=7)
    description = models.TextField(blank=True)
    background = models.TextField(blank=True)

    # Physical Attributes
    strength = DotsField(default=1)
    dexterity = DotsField(default=1)
    stamina = DotsField(default=1)

    # Mental Attributes
    intelligence = DotsField(default=1)
    wits = DotsField(default=1)
    resolve = DotsField(default=1)

    # Social Attributes
    presence = DotsField(default=1)
    manipulation = DotsField(default=1)
    composure = DotsField(default=1)

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

    # Many 2 Many relationships
    merits = models.ManyToManyField(Merit, related_name='+')
    powers = models.ManyToManyField(Power, related_name='+')

    # Character Advancement related
    beats = DotsField()
    experiences = models.PositiveIntegerField(null=True)
    template_beats = DotsField()
    template_experiences = models.PositiveIntegerField(null=True)

    # Organization related fields
    player = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='characters')
    storyteller = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='+')
    version = models.PositiveIntegerField(null=True)
    created_on = models.DateField(auto_now_add=True)
    modified_on = models.DateField(auto_now=True)
    is_approved = models.BooleanField(default=False)
    approved_on = models.DateField(null=True)
    is_retired = models.BooleanField(default=False)

    # Derived traits, they are not handled automatically because in some situations
    # their values can be manually adjusted
    health_levels = DotsField()
    willpower = DotsField()

    def __str__(self):
        return str(self.name)


class Anchor(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(AnchorCategory, on_delete=models.CASCADE, related_name='anchors')
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='anchors')
    description = models.TextField()

    def __str__(self):
        return str(self.name)

