from rest_framework import serializers

from .models import Address, Entity, Resource


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = (
            'port',
            'type',
            'notes',
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return rep

    def create(self, validated_data):
        instance = Resource.objects.create(**validated_data)
        return instance


class AddressSerializer(serializers.ModelSerializer):
    resources = ResourceSerializer(many=True)

    class Meta:
        model = Address
        fields = (
            'hostname',
            'ip_v4',
            'ip_v6',
            'mac_address',
            'mac_vendor',
            'resources',
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return rep

    def create(self, validated_data):
        validated_resources = validated_data.pop('resources')
        instance = Address.objects.create(**validated_data)

        for resource in validated_resources:
            instance.resources.create(**resource)

        return instance


class EntitySerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=True)

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

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return rep

    def create(self, validated_data):
        # extract address
        validated_address = validated_data.pop('address')
        # create entity without address
        instance = Entity.objects.create(**validated_data)

        for address in validated_address:
            # extract resources from address
            validated_resource = address.pop('resources')
            created_address = instance.address.create(**address)

            for resource in validated_resource:
                created_address.resources.create(**resource)

        return instance
