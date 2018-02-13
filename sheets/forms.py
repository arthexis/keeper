from sheets.models import Character
from django.forms import ModelForm, CharField, IntegerField, HiddenInput


class BaseCharacterForm(ModelForm):
    merits = CharField(required=False, widget=HiddenInput)
    powers = CharField(required=False, widget=HiddenInput)
    specialities = CharField(required=False, widget=HiddenInput)
    resource = IntegerField(required=False, widget=HiddenInput)
    willpower = IntegerField(required=False, widget=HiddenInput)
    damage_track = CharField(required=False, widget=HiddenInput)
    beats = IntegerField(required=False, widget=HiddenInput)
    experiences = IntegerField(required=False, widget=HiddenInput)
    template_beats = IntegerField(required=False, widget=HiddenInput)
    template_experiences = IntegerField(required=False, widget=HiddenInput)

    def clean_beats(self):
        beats = self.cleaned_data['beats']
        if beats:
            return int(beats)
        return 0

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
            'template', 'organization', 'user', 'health_levels',
        ]

