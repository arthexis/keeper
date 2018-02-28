from rest_framework import routers, serializers, viewsets
from rest_framework.relations import StringRelatedField

from organization.models import Organization
from sheets.models import Character
from game_rules.models import Merit


__all__ = (
    'router',
)


# Serializers

class CharacterSerializer(serializers.HyperlinkedModelSerializer):
    template = StringRelatedField()

    class Meta:
        model = Character
        fields = (
            'name', 'template', 'uuid', 'status', 'version'
        )


class MeritSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Merit
        fields = ('name',)


class organizationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organization
        fields = ('name', 'rules_url')


# View sets


class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer


class MeritViewSet(viewsets.ModelViewSet):
    queryset = Merit.objects.all()
    serializer_class = MeritSerializer


class organizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = organizationSerializer


router = routers.DefaultRouter()
router.register(r'character', CharacterViewSet)
router.register(r'merit', MeritViewSet)
router.register(r'organization', organizationViewSet)

