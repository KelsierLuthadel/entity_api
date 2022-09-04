from rest_framework import serializers

from .models import Address, Entity, Resource


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = (
            'id',
            'port',
            'type',
            'notes',
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep.id = instance.pk
        return rep

    def create(self, validated_data):
        instance = Resource.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        update_instance(instance, validated_data)
        instance.save()
        return instance


class AddressSerializer(serializers.ModelSerializer):
    resource = ResourceSerializer(many=True)

    class Meta:
        model = Address
        fields = (
            'id',
            'hostname',
            'ip_v4',
            'ip_v6',
            'mac_address',
            'mac_vendor',
            'resource',
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep.id = instance.pk
        return rep

    def create(self, validated_data):
        validated_resource = validated_data.pop('resource')
        instance = Address.objects.create(**validated_data)

        for resource in validated_resource:
            instance.resource.create(**resource)

        return instance

    def update(self, instance, validated_data):
        resources = instance.resource.all()
        resources.all().delete()

        validated_resource = validated_data.pop('resource')

        for resource in validated_resource:
            instance.resource.create(**resource)

        update_instance(instance, validated_data)
        instance.save()
        return instance


def update_instance(instance, validated_data):
    for key, value in validated_data.items():
        try:
            setattr(instance, key, value)
        except KeyError:  # validated_data may not contain all fields during HTTP PATCH
            pass


class EntitySerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=True)

    class Meta:
        model = Entity
        fields = (
            'id',
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
        rep.id = instance.pk
        return rep

    def create(self, validated_data):
        # extract address
        validated_address = validated_data.pop('address')
        # create entity without address
        instance = Entity.objects.create(**validated_data)

        for address in validated_address:
            # extract resources from address
            validated_resource = address.pop('resource')
            created_address = instance.address.create(**address)

            for resource in validated_resource:
                created_address.resource.create(**resource)

        return instance

    def update(self, instance, validated_data):
        addresses = instance.address.all()

        for address in addresses:
            address.resource.all().delete()
        addresses.all().delete()

        validated_address = validated_data.pop('address')

        for address in validated_address:
            # extract resources from address
            validated_resource = address.pop('resource')
            created_address = instance.address.create(**address)

            for resource in validated_resource:
                created_address.resource.create(**resource)

        update_instance(instance, validated_data)
        instance.save()
        return instance
