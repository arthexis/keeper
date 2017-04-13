from sheets.models import Character
from systems.models import CharacterTemplate
from django.contrib.auth.models import User
from django.forms import *
from systems.fields import DotsInput


class BaseCharacterForm(ModelForm):
    class Meta:
        model = Character
        exclude = []


class CreateCharacterForm(BaseCharacterForm):
    class Meta:
        model = Character
        exclude = [
            'primary_splat', 'secondary_splat', 'tertiary_splat',
            'power_stat', 'primary_anchor', 'secondary_anchor',
            'beats', 'experiences', 'organization',
            'template_beats', 'template_experiences', 'integrity',
        ]


class EditCharacterForm(BaseCharacterForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Character
        exclude = [
            'template', 'beats', 'experiences', 'organization', 'willpower',
            'template_beats', 'template_experiences', 'health_levels', 'resource',
        ]

