from rest_framework import serializers

from .models import Interface, Entity, Resource


def find_id(validated_address):
    return len(list(filter(lambda found: 'id' in found, validated_address)))


# noinspection PyUnresolvedReferences
class ResourceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

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
        return rep

    def create(self, validated_data):
        instance = Resource.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        update_instance(instance, validated_data)
        instance.save()
        return instance


# noinspection PyUnresolvedReferences
class AddressSerializer(serializers.ModelSerializer):
    resource = ResourceSerializer(many=True)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Interface
        fields = (
            'id',
            'hostname',
            'ip_v4',
            'ip_v6',
            'mac_address',
            'mac_vendor',
            'resource',
            'frequency',
            'channel',
            'SSID',
            'BSSID'
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return rep

    def create(self, validated_data):
        validated_resource = validated_data.pop('resource')
        instance = Interface.objects.create(**validated_data)

        for resource in validated_resource:
            instance.resource.create(**resource)

        return instance

    def update(self, instance, validated_data):
        if 'resource' in validated_data:
            validated_resource = validated_data.pop('resource')
            if len(list(filter(lambda resource: 'id' in resource, validated_resource))):
                self.merge(validated_resource)
            else:
                self.replace(instance, validated_resource)

        update_instance(instance, validated_data)

        instance.save()
        return instance

    @staticmethod
    def merge(validated_resource):
        for item in validated_resource:
            pk = item.pop('id')
            resource_instance = Resource.objects.get(pk=pk)
            update_instance(resource_instance, item)
            resource_instance.save()

    @staticmethod
    def replace(instance, validated_resource):
        resources = instance.resource.all()
        resources.all().delete()
        for resource in validated_resource:
            instance.resource.create(**resource)


def update_instance(instance, validated_data):
    for key, value in validated_data.items():
        try:
            setattr(instance, key, value)
        except KeyError:  # validated_data may not contain all fields during HTTP PATCH
            pass


# noinspection PyUnresolvedReferences
class EntitySerializer(serializers.ModelSerializer):
    interface = AddressSerializer(many=True)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Entity
        fields = (
            'id',
            'name',
            'notes',
            'interface',
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
        validated_interface = validated_data.pop('interface')
        # create entity without address
        instance = Entity.objects.create(**validated_data)

        for interface in validated_interface:
            # extract resources from address
            validated_resource = interface.pop('resource')
            created_address = instance.interface.create(**interface)

            for resource in validated_resource:
                created_address.resource.create(**resource)

        return instance

    def update(self, instance, validated_data):
        if 'interface' in validated_data:
            validated_interface = validated_data.pop('interface')
            if not find_id(validated_interface):
                interfaces = instance.interface.all()
                for interface in interfaces:
                    interface.resource.all().delete()
                interfaces.all().delete()

                for interface in validated_interface:
                    # extract resources from address
                    validated_resource = interface.pop('resource')
                    created_interface = instance.interface.create(**interface)

                    for resource in validated_resource:
                        created_interface.resource.create(**resource)
            else:
                for interface in validated_interface:
                    if 'resource' in interface:
                        validated_resources = interface.pop('resource')
                        for resource in validated_resources:
                            pk = resource.pop('id')
                            resource_instance = Resource.objects.get(pk=pk)
                            update_instance(resource_instance, resource)
                            resource_instance.save()

                    pk = interface.pop('id')
                    address_instance = Interface.objects.get(pk=pk)
                    update_instance(address_instance, interface)
                    address_instance.save()

        update_instance(instance, validated_data)
        instance.save()
        return instance
