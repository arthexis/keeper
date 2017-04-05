from orgs.models import *
from django.forms import *


class RegistrationForm(ModelForm):
    email = EmailField(required=True, help_text="Required. A confirmation email will be sent to this address.")

    class Meta:
        model = Profile
        fields = ("username", "email", "password", "phone")


__all__ = ('RegistrationForm', )
