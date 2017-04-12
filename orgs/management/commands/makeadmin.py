from django.core.management.base import BaseCommand
from orgs.models import Profile


class Command(BaseCommand):
    help = 'Make a normal user/profile a site admin with all permissions.'

    def add_arguments(self, parser):
        parser.add_argument('username')

    def handle(self, *args, **options):
        username = options["username"]
        profile = Profile.objects.get(username=username)
        profile.is_staff = True
        profile.is_verified = True
        profile.is_superuser = True
        profile.save()
        print("User modified successfully.")