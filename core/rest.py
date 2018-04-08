from rest_framework import routers, serializers, viewsets
from rest_framework.relations import StringRelatedField

from organization.models import Organization
from sheets.models import Character, ApprovalRequest, ResourceTracker
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


class MeritSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merit
        fields = ('name',)


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organization
        fields = ('name', 'rules_url', 'reference_code', 'chronicle')


class ApprovalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ApprovalRequest
        fields = (
            'character', 'user', 'status',
            'base_experience_cost', 'quantity', 'detail', 'total_experience_cost', 'prestige_level'
        )


class ResourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ResourceTracker
        fields = ('id', 'name', 'capacity', 'current', 'character')


# View sets


class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer


class MeritViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Merit.objects.all()
    serializer_class = MeritSerializer


class OrganizationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class ApprovalViewSet(viewsets.ModelViewSet):
    queryset = ApprovalRequest.objects.all()
    serializer_class = ApprovalSerializer


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = ResourceTracker.objects.all()
    serializer_class = ResourceSerializer


router = routers.DefaultRouter()
router.register(r'character', CharacterViewSet)
router.register(r'merit', MeritViewSet)
router.register(r'organization', OrganizationViewSet)
router.register(r'approval', ApprovalViewSet)
router.register(r'resource', ResourceViewSet)
