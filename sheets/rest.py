from sheets.models import Character
from rest_framework import routers, serializers, viewsets

__all__ = (
    'router',
)


class CharacterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Character
        fields = (
            'name', 'power_stat',
            'strength', 'dexterity', 'stamina',
        )


class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer


router = routers.DefaultRouter()
router.register(r'characters', CharacterViewSet)

