from sheets.models import Character
from django.forms import *


class BaseCharacterForm(ModelForm):
    merits = CharField(required=False, widget=HiddenInput)
    specialities = CharField(required=False, widget=HiddenInput)

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
            'template', 'beats', 'experiences', 'organization', 'willpower', 'user',
            'template_beats', 'template_experiences', 'health_levels',
        ]

