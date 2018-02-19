import os.path

import sys
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings

from seed_data.utils import import_object, REF_FIELD

STEPS = settings.SEED_DATA_PLAN.keys()


class Command(BaseCommand):
    help = 'Import seeded data from settings.SEED_DATA'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plan = settings.SEED_DATA_PLAN
        self.directory = settings.SEED_DATA_DIRECTORY

    def add_arguments(self, parser):
        parser.add_argument('action', choices=('generate', 'install'))
        parser.add_argument('--plan', default=None)
        parser.add_argument('--dir', default=None)
        parser.add_argument('--update', action='store_true')
        parser.add_argument('--migrate', action='store_true')
        parser.add_argument('--start', choices=STEPS)

    def handle(self, *args, **options):
        if options['dir']:
            self.directory = getattr(settings, options['dir'])
        if options['plan']:
            self.plan = getattr(settings, options['plan'])
        if options['action'] == 'generate':
            self.generate_data()
        elif options['action'] == 'install':
            if options['migrate']:
                if call_command('migrate') != 0:
                    print('Migrate failed, cancelling import.')
                    sys.exit(1)
            self.install_data(options['update'], options['start'])

    def generate_data(self):
        print(f'Source database: {settings.DATABASES["default"]["NAME"]}')

        for entity, refs in self.plan.items():
            if callable(refs):
                model_cls = import_object(settings.SEED_DATA_SERIALIZERS[entity]['model'])
                refs = [getattr(obj, REF_FIELD) for obj in model_cls.objects.all() if refs(obj)]
            outfile = os.path.join(self.directory, entity)
            print("Seed", entity, "->", ", ".join(refs))
            call_command('export', entity, '-o', outfile, '--refs', *refs)
        print("All seed data generated.")

    def install_data(self, update=False, start=None):
        print(f'Target database: {settings.DATABASES["default"]["NAME"]}')

        # Ensure the imports are made in the correct order
        completed = []
        for entity in self.plan.keys():
            if start:
                if entity != start:
                    print(f'Skipping import of <{entity}>')
                    continue
                start = None
            source = os.path.join(self.directory, entity)
            print(f"Seeding file <{entity}>")
            params = []
            if update:
                params.append('--update')
            try:
                call_command('import', source, *params)
            except SystemExit:
                print(f'Aborting. Steps completed: {", ".join(completed) or None}')
                sys.exit(1)
            completed.append(entity)
        print('Complete. Seed data installed successfully.')

