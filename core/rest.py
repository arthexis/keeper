from rest_framework import routers, serializers, viewsets
from rest_framework.relations import StringRelatedField

from organization.models import Organization
from sheets.models import Character, ApprovalRequest
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


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organization
        fields = ('name', 'rules_url')


class ApprovalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ApprovalRequest
        fields = (
            'character', 'user', 'status',
            'base_experience_cost', 'quantity', 'detail', 'total_experience_cost', 'prestige_level'
        )


# View sets


class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer


class MeritViewSet(viewsets.ModelViewSet):
    queryset = Merit.objects.all()
    serializer_class = MeritSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class ApprovalViewSet(viewsets.ModelViewSet):
    queryset = ApprovalRequest.objects.all()
    serializer_class = ApprovalSerializer


router = routers.DefaultRouter()
router.register(r'character', CharacterViewSet)
router.register(r'merit', MeritViewSet)
router.register(r'organization', OrganizationViewSet)
router.register(r'approval', ApprovalViewSet)
