import os.path
import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from rest_framework.renderers import JSONRenderer
from zipfile import ZipFile

from seed_data.utils import *


class Command(BaseCommand):
    help = 'Export configuration items.'

    def add_arguments(self, parser):
        parser.add_argument('entity', choices=list(SERIALIZERS.keys()))
        parser.add_argument('-o')
        parser.add_argument('--filter', nargs='*')
        parser.add_argument('--pks', nargs='*')
        parser.add_argument('--refs', nargs='*')
        parser.add_argument('--all', action='store_true')

    def handle(self, *args, **options):

        # Get the Model class and serializer for the specified entity
        entity = options['entity']
        model_cls, serializer_cls = get_model_serializer(entity)

        # Construct the queryset for export
        queryset = model_cls.objects.all()
        filters = None
        if options['filter']:
            # Each filter must be in the format column=value (use the Django ORM columns)
            filters = {i[0]: i[1] for i in map(lambda x: x.split('=', 1), options['filter'])}
            queryset = queryset.filter(**filters)

        if options['pks']:
            if filters:
                raise ValueError("Cannot use --pks, --refs or --filter options at the same time.")
            filters = {'pk__in': options['pks']}
            queryset = queryset.filter(**filters)
            missing = set(options['pks']) - set(queryset.values_list('pk', flat=True))
            if missing:
                raise ValueError(f"Unable to find entities: {missing}")

        if options['refs']:
            if filters:
                raise ValueError("Cannot use --pks, --refs or --filter options at the same time.")

            # Special case only for special commands, because they don't have a separate reference code.
            filters = {f'{REF_FIELD}__in': options['refs']}
            missing = set(options['refs']) - set(queryset.values_list(REF_FIELD, flat=True))

            queryset = queryset.filter(**filters)
            if missing:
                raise ValueError(f"Unable to find entities: {missing}")

        if not filters and not options['all']:
            raise ValueError("Use the --all option when not using --pks, --refs or --filters.")
        if not queryset.exists():
            print('No results found for specified filter, pks or refs.')
            return

        # Determine the target zipfile name
        filename = options['o']
        if not filename:
            timestamp = datetime.date.today().strftime('%y%m%d')
            filename = f'{entity}_{timestamp}.zip'
        elif not filename.endswith('zip'):
            filename += '.zip'
        target = os.path.join(settings.SEED_DATA_DIRECTORY, filename)

        with ZipFile(target, 'w') as z:
            for obj in queryset.all():
                print('Serializing:', str(obj))
                serializer = serializer_cls(obj)
                json_data = JSONRenderer().render(serializer.data)
                if options['refs']:
                    reference_code = getattr(obj, REF_FIELD)
                    name = f'{entity}_{reference_code}.json'
                else:
                    name = f'{entity}_{obj.pk}.json'
                print(f"- Extracting {entity} {obj.pk} - {obj}")
                z.writestr(name, json_data)

        print(f"Complete. Export file saved to {target}")

