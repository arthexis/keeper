from rest_framework import routers, serializers, viewsets
from rest_framework.relations import StringRelatedField

from sheets.models import Character
from game_rules.models import Merit


__all__ = (
    'router',
)


class CharacterSerializer(serializers.HyperlinkedModelSerializer):
    template = StringRelatedField()

    class Meta:
        model = Character
        fields = (
            'name', 'template', 'uuid', 'status', 'version'
        )


class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer


class MeritSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Merit
        fields = ('name',)


class MeritViewSet(viewsets.ModelViewSet):
    queryset = Merit.objects.all()
    serializer_class = MeritSerializer


router = routers.DefaultRouter()
router.register(r'character', CharacterViewSet)
router.register(r'merit', MeritViewSet)

