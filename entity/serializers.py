from rest_framework import serializers

from .models import Address, Entity


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            'hostname',
            'ip_v4',
            'ip_v6',
            'mac_address',
            'mac_vendor'
        )


class EntitySerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Entity
        fields = (
            'name',
            'notes',
            'address',
            'status',
            'os',
            'type',
            'hardware',
            'first_seen',
            'last_seen',
        )

    def create(self, validated_data):
        validated_address = validated_data.pop('address')
        address = Address.objects.create(**validated_address)
        instance = Entity.objects.create(**validated_data, address=address)
        return instance


