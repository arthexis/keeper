import logging

from rest_framework import serializers

from .models import CharacterTemplate, SplatCategory, Splat

logger = logging.getLogger(__name__)


class SplatOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Splat
        fields = ('name', )


class SplatSerializer(serializers.ModelSerializer):
    splats = SplatOptionSerializer(many=True, required=False)

    class Meta:
        model = SplatCategory
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
            'reference_code',
        )

    def create(self, validated_data):
        splat_categories_data = validated_data.pop('splat_categories', [])
        template = CharacterTemplate.objects.create(**validated_data)
        for splat_category_data in splat_categories_data:
            splats_data = splat_category_data.pop('splats', [])
            splat_category = SplatCategory.objects.create(splat_template=template, **splat_category_data)
            for splat_data in splats_data:
                Splat.objects.create(splat_category=splat_category, **splat_data)
        return template


