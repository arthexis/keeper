from rest_framework import routers, serializers, viewsets
from . import models


class MeritSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Merit
        fields = ('name', 'category', 'template', 'reference_book', 'reference_page',)


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = models.Merit.objects.all()
    serializer_class = MeritSerializer

