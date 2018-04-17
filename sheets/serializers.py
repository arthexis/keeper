from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from .models import Character


class CharacterSerializer(serializers.HyperlinkedModelSerializer):
    template = StringRelatedField()

    class Meta:
        model = Character
        fields = (
            'name', 'url', 'template', 'uuid', 'status', 'version'
        )