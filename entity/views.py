from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets

from entity.filters import EntitiesFilter, AddressFilter
from entity.models import Address, Entity, Resource
from entity.serializers import EntitySerializer, AddressSerializer, ResourceSerializer


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    filterset_class = AddressFilter


class EntityViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
    filterset_class = EntitiesFilter

