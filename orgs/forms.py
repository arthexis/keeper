from django.contrib.auth.hashers import make_password
from django_select2.forms import ModelSelect2Widget
from orgs.models import *
from django.forms import *
from datetimewidget.widgets import DateWidget


class RequestFormMixin(Form):
    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.configure()

    def configure(self):
        pass


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
    initial_org_pk = IntegerField(widget=HiddenInput, required=False)

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
    model = PublicOrganization
    search_fields = ['name__icontains']

    def label_from_instance(self, obj):
        return obj.name


class RequestMembershipForm(RequestFormMixin):
    organization = IntegerField()

    def configure(self):
        self.fields['organization'].widget = PublicOrganizationWidget(
            queryset=PublicOrganization.objects.exclude(memberships__user=self.request.user))


class PasswordRecoveryForm(Form):
    email = EmailField(required=True)


class EventForm(ModelForm):
    event_date = DateField(
        widget=DateWidget(usel10n=True, bootstrap_version=3), required=True,
        help_text="Required. Date of this event.")

    class Meta:
        model = Event
        fields = ("name", "event_date", "information",)


__all__ = (
    'RegistrationForm',
    'RequestMembershipForm',
    'PasswordRecoveryForm',
    'EventForm',
)
