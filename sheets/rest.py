from sheets.models import Character
from rest_framework import routers, serializers, viewsets


# Serializers define the API representation.
class CharacterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Character
        fields = (
            'name', 'power_stat',
            'strength', 'dexterity', 'stamina',
        )


# ViewSets define the view behavior.
class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'characters', CharacterViewSet)

