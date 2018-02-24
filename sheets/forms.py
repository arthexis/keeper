
from django.forms import Form, CharField, Textarea, ModelChoiceField, FileField
from game_rules.models import CharacterTemplate


class RequestCharacterForm(Form):
    character_name = CharField(
        help_text='Your character name or alias. Please ensure it complies with Domain rules.')
    character_template = ModelChoiceField(
        queryset=CharacterTemplate.objects.all(),
        help_text='This will determine which Storyteller team will approve your request.')
    character_sheet_image = FileField(
        help_text='Upload your character sheet in PDF or image format.')
    description = CharField(
        widget=Textarea(),
        help_text='Please provide additional background or information about your character. Be concise.')
