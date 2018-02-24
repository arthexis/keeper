
from django.forms import Form, CharField, URLField, Textarea, ModelChoiceField
from s3direct.widgets import S3DirectWidget
from game_rules.models import CharacterTemplate


class RequestCharacterForm(Form):
    character_name = CharField(
        help_text='Your character name or alias. Please ensure it complies with Domain rules.')
    character_template = ModelChoiceField(
        queryset=CharacterTemplate.objects.all(),
        help_text='This will determine which Storyteller team will approve your request.')
    character_sheet_image = URLField(
        widget=S3DirectWidget(dest='sheet-uploads'),
        help_text='Upload your character in PDF or image format.')
    description = CharField(
        widget=Textarea(),
        help_text='Please provide additional background or information about your character. Be concise.')
