from django.conf import settings
from django.contrib.auth.models import User


class AdminBackend:
    def authenticate(self, request, username=None, password=None):
        if not hasattr(settings, 'ADMIN_LOGIN'):
            return None
        admin = settings.ADMIN_LOGIN
        if username == admin['username'] and password == admin['password']:
            try:
                user = User.objects.get(username=username)
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


