import django_filters
from django.db import models
from entity.models import Interface, Entity


class AddressFilter(django_filters.FilterSet):
    port = django_filters.NumberFilter(field_name="resources__port", lookup_expr="iexact")
    type = django_filters.CharFilter(field_name="resources__type", lookup_expr="iexact")

    class Meta:
        model = Interface
        fields = ['hostname', 'ip_v4', 'ip_v6', 'mac_address', 'mac_vendor', 'port', 'type']
        filter_overrides = {
            models.GenericIPAddressField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            }
        }


class EntitiesFilter(django_filters.FilterSet):
    ipv4 = django_filters.CharFilter(field_name="address__ip_v4", lookup_expr='icontains')
    ipv6 = django_filters.CharFilter(field_name="address__ip_v6", lookup_expr='icontains')
    hostname = django_filters.CharFilter(field_name="address__hostname", lookup_expr='icontains')
    mac_address = django_filters.CharFilter(field_name="address__mac_address", lookup_expr='icontains')
    vendor = django_filters.CharFilter(field_name="address__mac_vendor", lookup_expr='icontains')
    port = django_filters.CharFilter(field_name="address__resources__port", lookup_expr='iexact')
    type = django_filters.CharFilter(field_name="address__resources__type", lookup_expr='iexact')

    class Meta:
        model = Entity
        fields = ['name', 'notes', 'ipv4', 'ipv6', 'hostname', 'mac_address', 'vendor',
                  'os', 'type', 'hardware', 'status',
                  'port', 'type',
                  ]
