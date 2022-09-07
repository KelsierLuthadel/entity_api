from rest_framework import serializers

from .models import Interface, Entity, Resource, SSID


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
def object_or_empty(validated_data, field):
    validated_resource = validated_data.pop(field) if field in validated_data else []
    return validated_resource


class InterfaceSerializer(serializers.ModelSerializer):
    resource = ResourceSerializer(many=True, required=False)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Interface
        fields = (
            'id',
            'type',
            'name',
            'hardware',
            'ip_v4',
            'ip_v6',
            'physical_address',
            'vendor',
            'notes',
            'resource',
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return rep

    def create(self, validated_data):
        validated_resource = object_or_empty(validated_data, 'resource')
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


class SSIDSerializer(serializers.ModelSerializer):
    client = InterfaceSerializer(many=True, required=False)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = SSID
        fields = (
            'id',
            'type',
            'hardware',
            'name',
            'channel',
            'frequency',
            'crypto',
            'BSSID',
            'notes',
            'client',
            'first_seen',
            'last_seen',
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return rep

    def create(self, validated_data):
        validated_interface = object_or_empty(validated_data, 'client')
        instance = SSID.objects.create(**validated_data)

        for interface in validated_interface:
            validated_resource = object_or_empty(interface, 'resource')
            created_address = instance.client.create(**interface)

            for resource in validated_resource:
                created_address.resource.create(**resource)

        return instance

    def update(self, instance, validated_data):
        if 'client' in validated_data:
            validated_interface = validated_data.pop('client')
            if not find_id(validated_interface):
                interfaces = instance.client.all()
                for interface in interfaces:
                    interface.resource.all().delete()
                interfaces.all().delete()

                for found in validated_interface:
                    # extract resources from address
                    if 'resource' in found:
                        validated_resource = found.pop('resource')
                        created_interface = instance.client.create(**found)

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


# noinspection PyUnresolvedReferences
class EntitySerializer(serializers.ModelSerializer):
    interface = InterfaceSerializer(many=True, required=False)
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
        validated_interface = object_or_empty(validated_data, 'interface')
        instance = Entity.objects.create(**validated_data)

        for interface in validated_interface:
            validated_resource = object_or_empty(interface, 'resource')
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
