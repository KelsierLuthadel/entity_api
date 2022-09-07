from rest_framework import serializers

from .models import Site, Network, Switch, WiFi, Machine, Interface, Resource, Bluetooth, Radio


def find(key, metadata):
    return len(list(filter(lambda found: key in found, metadata)))


def object_or_empty(validated_data, field):
    validated_resource = validated_data.pop(field) if field in validated_data else []
    return validated_resource


def update_instance(instance, validated_data):
    for key, value in validated_data.items():
        try:
            setattr(instance, key, value)
        except KeyError:  # validated_data may not contain all fields during HTTP PATCH
            pass


class SiteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Site
        fields = (
            'id',
            'name',
            'type',
            'notes',
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return rep

    def create(self, validated_data):
        instance = Site.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        update_instance(instance, validated_data)
        instance.save()
        return instance


class NetworkSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    site_id = serializers.PrimaryKeyRelatedField(queryset=Site.objects.all())

    class Meta:
        model = Network
        fields = (
            'id',
            'name',
            'type',
            'os',
            'hardware',
            'status',
            'notes',
            'detected_by',
            'first_seen',
            'last_seen',
            'site_id',
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return rep

    def create(self, validated_data):
        instance = Network.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        update_instance(instance, validated_data)
        instance.save()
        return instance


class SwitchSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    site_id = serializers.PrimaryKeyRelatedField(queryset=Site.objects.all())
    network_id = serializers.PrimaryKeyRelatedField(queryset=Network.objects.all())

    class Meta:
        model = Switch
        fields = (
            'id',
            'name',
            'address',
            'mask',
            'gateway',
            'physical_address',
            'vendor',
            'type',
            'os',
            'hardware',
            'status',
            'notes',
            'detected_by',
            'first_seen',
            'last_seen',
            'site_id',
            'network_id',
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return rep

    def create(self, validated_data):
        instance = Switch.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        update_instance(instance, validated_data)
        instance.save()
        return instance


class WiFiSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    site_id = serializers.PrimaryKeyRelatedField(queryset=Site.objects.all())
    network_id = serializers.PrimaryKeyRelatedField(queryset=Network.objects.all())

    class Meta:
        model = WiFi
        fields = (
            'id',
            'name',
            'type',
            'address',
            'mask',
            'gateway',
            'status',
            'channels',
            'frequency',
            'crypto',
            'SSID',
            'BSSID',
            'vendor',
            'notes',
            'detected_by',
            'first_seen',
            'last_seen',
            'site_id',
            'network_id',
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return rep

    def create(self, validated_data):
        instance = WiFi.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        update_instance(instance, validated_data)
        instance.save()
        return instance


class MachineSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    site_id = serializers.PrimaryKeyRelatedField(queryset=Site.objects.all())

    class Meta:
        model = Machine
        fields = (
            'id',
            'name',
            'type',
            'os',
            'hardware',
            'status',
            'notes',
            'detected_by',
            'first_seen',
            'last_seen',
            'site_id',
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return rep

    def create(self, validated_data):
        instance = Machine.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        update_instance(instance, validated_data)
        instance.save()
        return instance


class InterfaceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    site_id = serializers.PrimaryKeyRelatedField(queryset=Site.objects.all())
    machine_id = serializers.PrimaryKeyRelatedField(queryset=Machine.objects.all())

    class Meta:
        model = Interface
        fields = (
            'id',
            'name',
            'type',
            'ip_v4',
            'ip_v6',
            'status',
            'hardware',
            'physical_address',
            'vendor',
            'notes',
            'site_id',
            'machine_id',
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return rep

    def create(self, validated_data):
        instance = Interface.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        update_instance(instance, validated_data)
        instance.save()
        return instance


class ResourceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    site_id = serializers.PrimaryKeyRelatedField(queryset=Site.objects.all())
    interface_id = serializers.PrimaryKeyRelatedField(queryset=Interface.objects.all())

    class Meta:
        model = Resource
        fields = (
            'id',
            'name',
            'protocol',
            'port',
            'notes',
            'first_seen',
            'last_seen',
            'site_id',
            'interface_id',
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


class BluetoothSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    site_id = serializers.PrimaryKeyRelatedField(queryset=Site.objects.all())
    machine_id = serializers.PrimaryKeyRelatedField(queryset=Machine.objects.all())

    class Meta:
        model = Bluetooth
        fields = (
            'id',
            'name',
            'type',
            'status',
            'hardware',
            'physical_address',
            'vendor',
            'notes',
            'site_id',
            'machine_id',
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return rep

    def create(self, validated_data):
        instance = Bluetooth.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        update_instance(instance, validated_data)
        instance.save()
        return instance


class RadioSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    site_id = serializers.PrimaryKeyRelatedField(queryset=Site.objects.all())
    machine_id = serializers.PrimaryKeyRelatedField(queryset=Machine.objects.all())

    class Meta:
        model = Radio
        fields = (
            'id',
            'name',
            'type',
            'status',
            'hardware',
            'physical_address',
            'vendor',
            'notes',
            'site_id',
            'machine_id',
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return rep

    def create(self, validated_data):
        instance = Radio.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        update_instance(instance, validated_data)
        instance.save()
        return instance
