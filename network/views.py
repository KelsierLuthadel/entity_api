from rest_framework import permissions, viewsets

from network.models import Site, Network, Switch, WiFi, Machine, Interface, Resource, Bluetooth, Radio
from network.serializers import SiteSerializer, NetworkSerializer, SwitchSerializer, WiFiSerializer, MachineSerializer, \
    InterfaceSerializer, ResourceSerializer, BluetoothSerializer, RadioSerializer


class SiteView(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SiteSerializer


class NetworkView(viewsets.ModelViewSet):
    queryset = Network.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NetworkSerializer


class SwitchView(viewsets.ModelViewSet):
    queryset = Switch.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SwitchSerializer


class WiFiView(viewsets.ModelViewSet):
    queryset = WiFi.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WiFiSerializer


class MachineView(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MachineSerializer


class InterfaceView(viewsets.ModelViewSet):
    queryset = Interface.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InterfaceSerializer


class ResourceView(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ResourceSerializer


class BluetoothView(viewsets.ModelViewSet):
    queryset = Bluetooth.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BluetoothSerializer


class RadioView(viewsets.ModelViewSet):
    queryset = Radio.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RadioSerializer

