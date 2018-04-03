import os.path
import json
import sys

from django.conf import settings
from django.core.management.base import BaseCommand
from zipfile import ZipFile
from django.db import transaction

from seed_data.utils import get_model_serializer, REF_FIELD


class Command(BaseCommand):
    help = 'Export Emoveo Configuration.'

    def add_arguments(self, parser):
        parser.add_argument('filename')
        parser.add_argument('--update', action='store_true')

    def handle(self, *args, **options):

        # Determine the source zipfile name
        filename = options['filename']
        if not filename.endswith('zip'):
            filename += '.zip'
        source = os.path.join(settings.SEED_DATA_DIRECTORY, filename)
        print("Loading file {}".format(source))

        if not os.path.isfile(source):
            print("File not found, skipping import.")
            return

        # Open the zipfile for reading
        with transaction.atomic():

            errors = 0
            with ZipFile(source, 'r') as z:
                for name in z.namelist():
                    update = False

                    # Prepare the serializer from the file name and contents
                    entity, ref = name.replace('.json', '').split('_')
                    display = f'<{entity}: {ref}>'

                    model_cls, serializer_cls = get_model_serializer(entity)

                    data = json.loads(z.read(name).decode(settings.DEFAULT_CHARSET))
                    serializer = serializer_cls(data=data)

                    if options['update']:
                        ref = data[REF_FIELD]
                        instance = model_cls.objects.filter(**{REF_FIELD: ref})
                        if instance.exists():
                            update = True
                            instance.delete()

                    if serializer.is_valid():
                        if update:
                            print(f'{display} is valid, already exists, updating.')
                        else:
                            print(f'{display} is valid, creating.')
                        serializer.save()
                    else:
                        print(f"{display} failed to import with errors:")
                        for key, val in serializer.errors.items():
                            print(f"- {key}: {val}")
                            errors += 1

                if errors:
                    print(f'{errors} errors.')
                    sys.exit(1)

        print(f"Import of {filename} complete, changes saved.")
