from rest_framework import permissions, viewsets
from entity.filters import EntitiesFilter, InterfaceFilter
from entity.models import Interface, Entity, Resource, SSID
from entity.serializers import EntitySerializer, InterfaceSerializer, ResourceSerializer, SSIDSerializer


# noinspection PyUnresolvedReferences
class SSIDViewSet(viewsets.ModelViewSet):
    queryset = SSID.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = SSIDSerializer


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ResourceSerializer


# noinspection PyUnresolvedReferences
class InterfaceViewSet(viewsets.ModelViewSet):
    queryset = Interface.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InterfaceSerializer
    filterset_class = InterfaceFilter


# noinspection PyUnresolvedReferences

class EntityViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EntitySerializer
    filterset_class = EntitiesFilter
