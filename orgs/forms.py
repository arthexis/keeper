from django_select2.forms import ModelSelect2Widget
from django.forms import Form, ModelForm, IntegerField, DateField
from datetimewidget.widgets import DateWidget

from orgs.models import Event, Organization

__all__ = (
    'RequestMembershipForm',
    'EventForm',
)


class RequestFormMixin(Form):
    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.configure()

    def configure(self):
        pass


class PublicOrganizationWidget(ModelSelect2Widget):
    model = Organization
    search_fields = ['name__icontains']

    def get_queryset(self):
        return Organization.objects.all()

    def label_from_instance(self, obj):
        return obj.name


class RequestMembershipForm(RequestFormMixin):
    organization = IntegerField()

    def configure(self):
        self.fields['organization'].widget = PublicOrganizationWidget(
            queryset=Organization.objects.exclude(memberships__user=self.request.user))


class EventForm(ModelForm):
    event_date = DateField(
        widget=DateWidget(usel10n=True, bootstrap_version=3), required=True,
        help_text="Required. Date of this event.")

    class Meta:
        model = Event
        fields = ("name", "event_date", "information",)

