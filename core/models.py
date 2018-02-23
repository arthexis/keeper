import logging

from django.db.models import CharField, DateTimeField, BooleanField
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.conf import settings
from django.apps import apps

logger = logging.getLogger(__name__)

__all__ = (
    'UserProfile',
)


# Each individual user has a Profile
class UserProfile(AbstractUser):
    phone = CharField(max_length=20, blank=True, help_text="Optional.")
    last_visit = DateTimeField(blank=True, null=True, editable=False)
    email_opt_out = BooleanField(default=False)

    class Meta:
        verbose_name = 'User Profile'

    def __str__(self):
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}"
        return f'{self.username}'

    def can_change_password(self, user=None):
        if user and user.username == settings.ADMIN_LOGIN_USERNAME:
            return False
        return True

    def change_password(self, user=None):
        return redirect('account_change_password')

    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)

        # Create memberships on save when invited
        if created and not self.is_superuser:
            apps.get_model('organization', 'Invitation').redeem(self)

    def send_mail(self, subject, message=None, template=None, context=None):
        if self.email_opt_out:
            return
        if not self.email:
            logger.error(f"Unable to send email to {self.username}; address missing.")
            return
        kwargs = {'fail_silently': True}
        if template is not None:
            kwargs['html_message'] = render_to_string(template, context)
        send_mail(
            subject, message, settings.DEFAULT_FROM_EMAIL,
            [self.email], **kwargs)
