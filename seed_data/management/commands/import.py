import os.path
import json
import sys

from django.conf import settings
from django.core.management.base import BaseCommand
from zipfile import ZipFile
from django.db import transaction

from seed_data.utils import *


class Command(BaseCommand):
    help = 'Export Emoveo Configuration.'

    def add_arguments(self, parser):
        parser.add_argument('filename')
        parser.add_argument('--skip', action='store_true')
        parser.add_argument('--update', action='store_true')

    def handle(self, *args, **options):

        # Determine the source zipfile name
        filename = options['filename']
        if not filename.endswith('zip'):
            filename += '.zip'
        source = os.path.join(settings.SEED_DATA_DIRECTORY, filename)
        print("Loading file {}".format(source))

        # Open the zipfile for reading
        has_errors = False
        with ZipFile(source, 'r') as z:
            for name in z.namelist():

                # Prepare the serializer from the file name and contents
                entity, pk = name.replace('.json', '').split('_')

                model_cls, serializer_cls = get_model_serializer(entity)

                data = json.loads(z.read(name).decode(settings.DEFAULT_CHARSET))
                serializer = serializer_cls(data=data)

                # Validate and execute the individual import

                if serializer.is_valid():
                    print(f'Import {entity} {pk}: serialized data valid')
                    with transaction.atomic():

                        if options['update']:
                            ref = data[REF_FIELD]
                            instance = model_cls.objects.filter(**{REF_FIELD: ref})
                            if instance.exists():
                                instance.delete()

                        serializer.save()
                else:
                    print(f"Failed to import {name}:")
                    for key, val in serializer.errors.items():
                        has_errors = True
                        print(f"- {key}: {val}")

        print("Import complete.")
        if has_errors and not options['skip']:
            sys.exit(1)
