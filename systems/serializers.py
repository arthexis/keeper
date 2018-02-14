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

    def create(self, validated_data):
        splat_categories = validated_data.pop('splat_categories', [])
        template = CharacterTemplate.objects.create(**validated_data)
        for sc_data in splat_categories:
            sc_data['template'] = template
            options = sc_data.pop('splats', [])
            category = Splat.objects.create(**sc_data)
            for so_data in options:
                so_data['category'] = category
                SplatOption.objects.create(**so_data)
        return template


