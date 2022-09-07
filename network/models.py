from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator, int_list_validator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Status(models.TextChoices):
    UP = 'UP', _('Up')
    DOWN = 'DOWN', _('Down')


class SSIDType(models.TextChoices):
    WIFI_DEVICE = 'DEVICE', _('Device'),
    WIFI_BRIDGED = 'WIFI_BRIDGED', _('Wi-Fi Bridged'),
    WIFI_AP = 'WIFI_AP', _('Wi-Fi AP'),
    WIFI_AD_HOC = 'WIFI_AD_HOC', _('Wi-Fi AD Hoc'),


class Protocol(models.TextChoices):
    TCP = 'TCP', _('TCP')
    UDP = 'UDP', _('UDP')


class Site(models.Model):
    name = models.CharField(max_length=253, default=None, blank=True, null=True)
    type = models.CharField(max_length=40, default=None, blank=True, null=True)
    notes = models.TextField(default=None, blank=True, null=True)


class Network(models.Model):
    name = models.CharField(max_length=253, default=None, blank=True, null=True)
    type = models.CharField(max_length=40, default=None, blank=True, null=True)
    os = models.CharField(max_length=40, default=None, blank=True, null=True)
    hardware = models.CharField(max_length=40, default=None, blank=True, null=True)
    status = models.CharField(max_length=4, choices=Status.choices, default=Status.DOWN)
    notes = models.TextField(default=None, blank=True, null=True)
    detected_by = models.CharField(max_length=40, default=None, blank=True, null=True)  # todo choices
    first_seen = models.DateTimeField(default=timezone.now, blank=True, verbose_name='first_seen')
    last_seen = models.DateTimeField(default=timezone.now, blank=True, verbose_name='last_seen')
    site_id = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='+', default=None, blank=True, null=True)

    def __str__(self):
        return self.name


class Switch(models.Model):
    name = models.CharField(max_length=253, default=None, blank=True, null=True)
    address = models.GenericIPAddressField(default=None, blank=True, null=True)
    mask = models.GenericIPAddressField(default=None, blank=True, null=True)
    gateway = models.GenericIPAddressField(default=None, blank=True, null=True)
    physical_address = models.CharField(max_length=17, default=None, blank=True, null=True, validators=[RegexValidator(
        regex='^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$',
        message='MAC Address must be valid',
        code='invalid_mac_address'
    )])
    vendor = models.CharField(max_length=40, default=None, blank=True, null=True)
    type = models.CharField(max_length=40, default=None, blank=True, null=True)
    os = models.CharField(max_length=40, default=None, blank=True, null=True)
    hardware = models.CharField(max_length=40, default=None, blank=True, null=True)
    status = models.CharField(max_length=4, choices=Status.choices, default=Status.DOWN)
    notes = models.TextField(default=None, blank=True, null=True)
    detected_by = models.CharField(max_length=40, default=None, blank=True, null=True)  # todo choices
    first_seen = models.DateTimeField(default=timezone.now, blank=True, verbose_name='first_seen')
    last_seen = models.DateTimeField(default=timezone.now, blank=True, verbose_name='last_seen')
    site_id = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='+',
                                default=None, blank=True, null=True)
    network_id = models.ForeignKey(Network, on_delete=models.CASCADE, related_name='+',
                                   default=None, blank=True, null=True)

    def __str__(self):
        return self.name


class WiFi(models.Model):
    name = models.CharField(max_length=253, default=None, blank=True, null=True)
    type = models.CharField(max_length=20, choices=SSIDType.choices, default=SSIDType.WIFI_DEVICE)
    address = models.GenericIPAddressField(default=None, blank=True, null=True)
    mask = models.GenericIPAddressField(default=None, blank=True, null=True)
    gateway = models.GenericIPAddressField(default=None, blank=True, null=True)
    status = models.CharField(max_length=4, choices=Status.choices, default=Status.DOWN)
    channels = models.CharField(validators=[int_list_validator], max_length=100)
    frequency = models.IntegerField(default=None, null=True,
                                    validators=[
                                        MaxValueValidator(65535),
                                        MinValueValidator(1)
                                    ])
    crypto = models.CharField(max_length=40, default=None, blank=True, null=True)
    SSID = models.CharField(max_length=17, default=None, blank=True, null=True, validators=[RegexValidator(
        regex='^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$',
        message='SSID Address must be valid',
        code='invalid_mac_address'
    )])
    BSSID = models.CharField(max_length=17, default=None, blank=True, null=True, validators=[RegexValidator(
        regex='^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$',
        message='BSSID Address must be valid',
        code='invalid_mac_address'
    )])
    vendor = models.CharField(max_length=40, default=None, blank=True, null=True)
    notes = models.TextField(default=None, blank=True, null=True)
    detected_by = models.CharField(max_length=40, default=None, blank=True, null=True)  # todo choices
    first_seen = models.DateTimeField(default=timezone.now, blank=True, verbose_name='first_seen')
    last_seen = models.DateTimeField(default=timezone.now, blank=True, verbose_name='last_seen')
    site_id = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='+',
                                default=None, blank=True, null=True)
    network_id = models.ForeignKey(Network, on_delete=models.CASCADE, related_name='+',
                                   default=None, blank=True, null=True)

    def __str__(self):
        return self.name


class Machine(models.Model):
    name = models.CharField(max_length=253, default=None, blank=True, null=True)
    type = models.CharField(max_length=40, default=None, blank=True, null=True)
    os = models.CharField(max_length=40, default=None, blank=True, null=True)
    hardware = models.CharField(max_length=40, default=None, blank=True, null=True)
    status = models.CharField(max_length=4, choices=Status.choices, default=Status.DOWN)
    notes = models.TextField(default=None, blank=True, null=True)
    detected_by = models.CharField(max_length=40, default=None, blank=True, null=True)  # todo choices
    first_seen = models.DateTimeField(default=timezone.now, blank=True, verbose_name='first_seen')
    last_seen = models.DateTimeField(default=timezone.now, blank=True, verbose_name='last_seen')
    site_id = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='+',
                                default=None, blank=True, null=True)

    def __str__(self):
        return self.name


class Interface(models.Model):
    name = models.CharField(max_length=253, default=None, blank=True, null=True)
    type = models.CharField(max_length=40, default=None, blank=True, null=True)
    ip_v4 = models.GenericIPAddressField(default=None, blank=True, null=True)
    ip_v6 = models.GenericIPAddressField(default=None, blank=True, null=True)
    status = models.CharField(max_length=4, choices=Status.choices, default=Status.DOWN)
    hardware = models.CharField(max_length=40, default=None, blank=True, null=True)
    physical_address = models.CharField(max_length=17, default=None, blank=True, null=True, validators=[RegexValidator(
        regex='^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$',
        message='MAC Address must be valid',
        code='invalid_mac_address'
    )])
    vendor = models.CharField(max_length=40, default=None, blank=True, null=True)
    notes = models.TextField(default=None, blank=True, null=True)
    first_seen = models.DateTimeField(default=timezone.now, blank=True, verbose_name='first_seen')
    last_seen = models.DateTimeField(default=timezone.now, blank=True, verbose_name='last_seen')
    site_id = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='+',
                                default=None, blank=True, null=True)
    machine_id = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='+',
                                   default=None, blank=True, null=True)

    def __str__(self):
        return self.name


class Resource(models.Model):
    name = models.CharField(max_length=253, default=None, blank=True, null=True)
    protocol = models.CharField(max_length=4, choices=Protocol.choices, default=Protocol.TCP)
    port = models.IntegerField(validators=[
        MaxValueValidator(65535),
        MinValueValidator(1)
    ])
    notes = models.CharField(max_length=255, default=None, blank=True, null=True)
    first_seen = models.DateTimeField(default=timezone.now, blank=True, verbose_name='first_seen')
    last_seen = models.DateTimeField(default=timezone.now, blank=True, verbose_name='last_seen')
    site_id = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='+',
                                default=None, blank=True, null=True)
    interface_id = models.ForeignKey(Interface, on_delete=models.CASCADE, related_name='+',
                                     default=None, blank=True, null=True)

    def __str__(self):
        return self.name


class Bluetooth(models.Model):
    name = models.CharField(max_length=253, default=None, blank=True, null=True)
    type = models.CharField(max_length=40, default=None, blank=True, null=True)
    hardware = models.CharField(max_length=40, default=None, blank=True, null=True)
    status = models.CharField(max_length=4, choices=Status.choices, default=Status.DOWN)
    physical_address = models.CharField(max_length=17, default=None, blank=True, null=True, validators=[RegexValidator(
        regex='^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$',
        message='MAC Address must be valid',
        code='invalid_mac_address'
    )])
    vendor = models.CharField(max_length=40, default=None, blank=True, null=True)
    notes = models.TextField(default=None, blank=True, null=True)
    first_seen = models.DateTimeField(default=timezone.now, blank=True, verbose_name='first_seen')
    last_seen = models.DateTimeField(default=timezone.now, blank=True, verbose_name='last_seen')
    site_id = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='+',
                                default=None, blank=True, null=True)
    machine_id = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='+',
                                   default=None, blank=True, null=True)

    def __str__(self):
        return self.name


class Radio(models.Model):
    name = models.CharField(max_length=253, default=None, blank=True, null=True)
    type = models.CharField(max_length=40, default=None, blank=True, null=True)
    hardware = models.CharField(max_length=40, default=None, blank=True, null=True)
    status = models.CharField(max_length=4, choices=Status.choices, default=Status.DOWN)
    physical_address = models.CharField(max_length=17, default=None, blank=True, null=True, validators=[RegexValidator(
        regex='^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$',
        message='MAC Address must be valid',
        code='invalid_mac_address'
    )])
    vendor = models.CharField(max_length=40, default=None, blank=True, null=True)
    notes = models.TextField(default=None, blank=True, null=True)
    first_seen = models.DateTimeField(default=timezone.now, blank=True, verbose_name='first_seen')
    last_seen = models.DateTimeField(default=timezone.now, blank=True, verbose_name='last_seen')
    site_id = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='+',
                                default=None, blank=True, null=True)
    machine_id = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='+',
                                   default=None, blank=True, null=True)
