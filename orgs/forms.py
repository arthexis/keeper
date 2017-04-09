from django.contrib.auth.hashers import make_password
from django_select2.forms import ModelSelect2Widget
from orgs.models import *
from django.forms import *


class RequestFormMixin(Form):
    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request


class RegistrationForm(ModelForm):
    email = EmailField(
        required=True,
        help_text="Required. A confirmation email will be sent to this address."
    )
    password = CharField(
        widget=PasswordInput, required=True,
        help_text="Required. At least 8 characters and alphanumeric."
    )
    confirm_password = CharField(
        widget=PasswordInput, required=True,
        help_text="Required. Please type your password again."
    )
    first_name = CharField(
        required=False,
        help_text="Required. Only shared with Organizations you join."
    )
    last_name = CharField(
        required=False,
        help_text="Required. Only shared with Organizations you join."
    )

    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError('Passwords do not match.')

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.password = make_password(self.cleaned_data.get('password'))
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Profile
        fields = (
            "username", "email", "first_name", "last_name",
            "password", "confirm_password", "phone")


class PublicOrganizationWidget(ModelSelect2Widget):
    model = Organization
    search_fields = ['name__icontains']

    def label_from_instance(self, obj):
        return obj.name


class RequestMembershipForm(RequestFormMixin):
    organization = IntegerField(widget=PublicOrganizationWidget)


class PasswordRecoveryForm(Form):
    email = EmailField(required=True)


class EventForm(ModelForm):

    class Meta:
        model = Event
        fields = ("name", "event_date", "information",)


__all__ = (
    'RegistrationForm',
    'RequestMembershipForm',
    'PasswordRecoveryForm',
    'EventForm',
)
