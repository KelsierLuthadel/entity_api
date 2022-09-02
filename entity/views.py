from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets

from entity.models import Address, Entity
from entity.serializers import EntitySerializer, AddressSerializer


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class EntityViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer


