import importlib
import logging

from django.db.models import Model, ManyToOneRel
from typing import Type
from django.conf import settings
from rest_framework.serializers import ModelSerializer

__all__ = (
    'SERIALIZERS',
    'REF_FIELD',
    'import_object',
    'get_model_serializer'
)

logger = logging.getLogger(__name__)

SERIALIZERS = settings.SEED_DATA_SERIALIZERS

REF_FIELD = getattr(settings, 'SEED_DATA_REF_FIELD', 'reference_code')


def import_object(path) -> (Type[Model], Type[ModelSerializer]):
    if not isinstance(path, str):
        return path
    module_path, obj_name = path.rsplit('.', 1)
    module = importlib.import_module(module_path)
    return getattr(module, obj_name)


def get_model_serializer(entity: str):
    entry = SERIALIZERS[entity]
    model_cls = import_object(entry.get('model'))
    serializer_path = entry.get('serializer')
    if serializer_path:
        serializer_cls = import_object(serializer_path)
    else:
        serializer_cls = serializer_factory(model_cls)
    return (model_cls, serializer_cls)


def serializer_factory(model_cls: Type[Model], create=True, nested=True, exclude=None):
    attrs = {}
    class_name = f"{model_cls.__name__}Serializer"

    field_names = []
    nested_serializers = {}
    nested_fields = {}

    for field in model_cls._meta.get_fields(include_parents=True):
        if exclude and field.name in exclude:
            continue
        elif nested and isinstance(field, ManyToOneRel):
            related_name = field.related_name
            if not related_name or related_name == '+':
                continue
            remote_names = [field.remote_field.name]
            serializer_cls = serializer_factory(field.related_model, create=False, exclude=remote_names)
            attrs[field.name] = serializer_cls(many=True, required=False)
            nested_serializers[field.name] = serializer_cls
            nested_fields[field.name] = field
        elif not field.serialize:
            continue

        field_names.append(field.name)

    if create:
        def _create(self, validated_data):
            nested_data_map = {}
            for nested_field_name in self.nested_fields.keys():
                data = validated_data.pop(nested_field_name, None)
                if data:
                    nested_data_map[nested_field_name] = data

            obj = self.Meta.model.objects.create(**validated_data)

            for nested_key, nested_data in nested_data_map.items():
                nested_cls = self.nested_serializers[nested_key]
                nested_field = self.nested_fields[nested_key]
                for child_obj_data in nested_data:
                    child_obj_data[nested_field.remote_field.name] = obj
                    _create(nested_cls, child_obj_data)

            return obj

        attrs['create'] = _create

    attrs['nested_serializers'] = nested_serializers
    attrs['nested_fields'] = nested_fields
    serializer_cls = type(class_name, (ModelSerializer,), attrs)

    meta_attrs = {
        'model': model_cls,
        'fields': tuple(field_names),
    }
    serializer_cls.Meta = type('Meta', (), meta_attrs)

    return serializer_cls



