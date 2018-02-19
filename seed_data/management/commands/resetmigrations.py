import os
import os.path

from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Delete all migrations and create them again from scratch.'

    def handle(self, *args, **options):
        for app in settings.LOCAL_APPS:
            mig_dir = os.path.join(settings.BASE_DIR, app, 'migrations')
            for fn in os.listdir(mig_dir):
                if fn == '__init__.py':
                    continue
                if fn.endswith('.py'):
                    print(f'Deleting {app} migration {fn}')
                    os.remove(os.path.join(mig_dir, fn))
        call_command('makemigrations')

