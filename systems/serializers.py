from rest_framework import serializers

from .models import CharacterTemplate, Splat, SplatOption


class SplatOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SplatOption
        fields = ('name', )


class SplatSerializer(serializers.ModelSerializer):
    splats = SplatOptionSerializer(many=True, required=False)

    class Meta:
        model = Splat
        fields = ('name', 'flavor', 'splats')


class TemplateSerializer(serializers.ModelSerializer):
    splat_categories = SplatSerializer(many=True, required=False)

    class Meta:
        model = CharacterTemplate
        fields = (
            'name',
            'game_line',
            'integrity_name',
            'power_stat_name',
            'resource_name',
            'primary_anchor_name',
            'secondary_anchor_name',
            'character_group_name',
            'experiences_prefix',
            'splat_categories',
        )



