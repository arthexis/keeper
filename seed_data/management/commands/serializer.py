from django.core.management.base import BaseCommand
from seed_data.utils import import_object, serializer_factory


class Command(BaseCommand):
    help = 'Construct a serializer for a given model and output the python code.'

    def add_arguments(self, parser):
        parser.add_argument('model')

    def handle(self, *args, **options):
        model_cls = import_object(options['model'])
        serializer_cls = serializer_factory(model_cls)
        print()
        self._print(serializer_cls)

    def _print(self, serializer_cls, top=True):
        for nested_cls in serializer_cls.nested_serializers.values():
            self._print(nested_cls, top=False)
        print(f'class {serializer_cls.__name__}(ModelSerializer):')
        attrs_list = []
        attrs_cls_list = []
        for nested_field in serializer_cls.nested_fields.values():
            attr_cls = serializer_cls.nested_serializers[nested_field.name]
            attrs_list.append(nested_field)
            attrs_cls_list.append(attr_cls)
            print(f'\t{nested_field.name} = {attr_cls.__name__}(many=True, null=True)')
        print('\tclass Meta:')
        model_cls = serializer_cls.Meta.model
        print(f'\t\tmodel = {model_cls.__name__}')
        print(f'\t\tfields = {serializer_cls.Meta.fields}\n')
        if top:
            print(f'\tdef create(self, validated_data)')
            print(f'\t\traise NotImplemented')
        print()



