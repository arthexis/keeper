import logging

from django.db.models import CharField, TextField, SlugField, Manager, Model
logger = logging.getLogger(__name__)

__all__ = (
    'Organization',
)


class Organization(Model):

    name = CharField(
        max_length=200, help_text="Required. Must be unique.", unique=True)
    information = TextField(
        blank=True,
        help_text="Information about your organization.")
    reference_code = SlugField(
        'URL Prefix', unique=True,
        help_text='Required. Must be unique across all organizations.')

    class Meta:
        verbose_name = 'Organization'

    def __str__(self):
        return f'{self.name}'

    def get_membership(self, user):
        return self.memberships.get(user=user)


