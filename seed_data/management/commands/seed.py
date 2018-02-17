import os.path

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings

from seed_data.utils import import_object, REF_FIELD


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
        parser.add_argument('--skip', action='store_true')
        parser.add_argument('--update', action='store_true')
        parser.add_argument('--migrate', action='store_true')

    def handle(self, *args, **options):
        if options['dir']:
            self.directory = getattr(settings, options['dir'])
        if options['plan']:
            self.plan = getattr(settings, options['plan'])
        if options['action'] == 'generate':
            self.generate_data()
        elif options['action'] == 'install':
            if options['migrate']:
                call_command('migrate')
            self.install_data(options['skip'], options['update'])

    def generate_data(self):
        for entity, refs in self.plan.items():
            if callable(refs):
                model_cls = import_object(settings.SEED_DATA_SERIALIZERS[entity]['model'])
                refs = [getattr(obj, REF_FIELD) for obj in model_cls.objects.all() if refs(obj)]
            outfile = os.path.join(self.directory, entity)
            print("Seed", entity, "->", ", ".join(refs))
            call_command('export', entity, '-o', outfile, '--refs', *refs)
        print("All seed data generated.")

    def install_data(self, skip=False, update=False):
        # Ensure the imports are made in the correct order
        for entity in self.plan.keys():
            source = os.path.join(self.directory, entity)
            print("Seeding ", entity)
            params = []
            if skip:
                params.append('--skip')
            if update:
                params.append('--update')
            call_command('import', source, *params)
        print("Missing seed data imported.")

