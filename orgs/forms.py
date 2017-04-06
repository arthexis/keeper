from django.contrib.auth.hashers import make_password
from django_select2.forms import ModelSelect2Widget
from orgs.models import *
from django.forms import *
from django.shortcuts import get_object_or_404


class RegistrationForm(ModelForm):
    email = EmailField(
        required=True, help_text="Required. A confirmation email will be sent to this address.")
    password = CharField(
        widget=PasswordInput, required=True,
        help_text="At least 8 characters and alphanumeric."
    )
    confirm_password = CharField(widget=PasswordInput, required=True)

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
        fields = ("username", "email", "password", "confirm_password", "phone")


class PublicOrganizationWidget(ModelSelect2Widget):
    model = Organization
    search_fields = ['name__icontains']

    def label_from_instance(self, obj):
        return obj.name


class RequestMembershipForm(Form):
    organization = IntegerField(widget=PublicOrganizationWidget)


__all__ = (
    'RegistrationForm',
    'RequestMembershipForm',
)
