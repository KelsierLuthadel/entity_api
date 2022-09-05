from rest_framework import permissions, viewsets
from entity.filters import EntitiesFilter, AddressFilter
from entity.models import Interface, Entity, Resource
from entity.serializers import EntitySerializer, AddressSerializer, ResourceSerializer


# noinspection PyUnresolvedReferences

class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ResourceSerializer


# noinspection PyUnresolvedReferences
class InterfaceViewSet(viewsets.ModelViewSet):
    queryset = Interface.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AddressSerializer
    filterset_class = AddressFilter


# noinspection PyUnresolvedReferences

class EntityViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EntitySerializer
    filterset_class = EntitiesFilter
