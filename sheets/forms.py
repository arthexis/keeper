
from django.forms import Form, CharField


class RequestForm(Form):
    character_name = CharField()

