from rest_framework import routers, serializers, viewsets
from rest_framework.relations import StringRelatedField

from organization.models import Chapter
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


class ChapterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Chapter
        fields = ('name', 'rules_url')


# View sets


class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer


class MeritViewSet(viewsets.ModelViewSet):
    queryset = Merit.objects.all()
    serializer_class = MeritSerializer


class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer


router = routers.DefaultRouter()
router.register(r'character', CharacterViewSet)
router.register(r'merit', MeritViewSet)
router.register(r'chapter', ChapterViewSet)

