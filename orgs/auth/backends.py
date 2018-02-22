from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class AdminBackend:
    def authenticate(self, request, username=None, password=None):
        admin_username = settings.ADMIN_LOGIN_USERNAME
        admin_password = settings.ADMIN_LOGIN_PASSWORD
        if not admin_username or not admin_password:
            return None
        if username == admin_username and password == admin_password:
            try:
                user = User.objects.get(username=admin_username)
            except User.DoesNotExist:
                user = User.objects.create(username=username, is_staff=True, is_superuser=True)
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def has_perm(self, user_obj, perm, obj=None):
        if not hasattr(settings, 'ADMIN_LOGIN'):
            return
        return user_obj.username == settings.ADMIN_LOGIN['username']


