import logging

from django.contrib.auth.signals import user_logged_in

logger = logging.getLogger(__name__)


def user_login_callback(sender, request=None, user=None, **kwargs):
    if user.is_superuser:
        from orgs.models import Profile
        profile, created = Profile.objects.get_or_create(user=user)
        if created:
            profile.username = user.username
            profile.password = user.password
            profile.email = user.email
            profile.is_staff = True
            profile.is_superuser = True
            profile.save()
            logger.info(f'Created admin profile for {user}')
    logger.info(f'Login successful, user={user}')


user_logged_in.connect(user_login_callback)
