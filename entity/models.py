from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Resource(models.Model):
    class Type(models.TextChoices):
        TCP = 'TCP', _('TCP')
        UDP = 'UDP', _('UDP')

    port = models.IntegerField(validators=[
        MaxValueValidator(65535),
        MinValueValidator(1)
    ])
    type = models.CharField(max_length=3, choices=Type.choices, default=Type.TCP)
    notes = models.CharField(max_length=255, default=None, blank=True, null=True)

    def __str__(self):
        return "{type}({port})".format(type=self.type, port=str(self.port))


class Interface(models.Model):
    type = models.CharField(max_length=40, default=None, blank=True, null=True)
    hardware = models.CharField(max_length=40, default=None, blank=True, null=True)
    name = models.CharField(max_length=253, default=None, blank=True, null=True)
    ip_v4 = models.GenericIPAddressField(default=None, blank=True, null=True)
    ip_v6 = models.GenericIPAddressField(default=None, blank=True, null=True)
    physical_address = models.CharField(max_length=17, default=None, blank=True, null=True, validators=[RegexValidator(
        regex='^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$',
        message='MAC Address must be valid',
        code='invalid_mac_address'
    )])
    vendor = models.CharField(max_length=40, default=None, blank=True, null=True)
    notes = models.TextField(default=None, blank=True, null=True)
    resource = models.ManyToManyField(Resource, blank=True)

    def __str__(self):
        return self.name


class SSID(models.Model):
    class Type(models.TextChoices):
        WIFI_DEVICE = 'DEVICE', _('Device'),
        WIFI_BRIDGED = 'WIFI_BRIDGED', _('Wi-Fi Bridged'),
        WIFI_AP = 'WIFI_AP', _('Wi-Fi AP'),
        WIFI_AD_HOC = 'WIFI_AD_HOC', _('Wi-Fi AD Hoc'),

    type = models.CharField(max_length=40, choices=Type.choices,  default=None, blank=True, null=True)
    hardware = models.CharField(max_length=40, default=None, blank=True, null=True)
    name = models.CharField(max_length=253, default=None, blank=True, null=True)
    channel = models.IntegerField(default=None, null=True,
                                  validators=[
                                      MaxValueValidator(20),
                                      MinValueValidator(1)
                                  ])
    frequency = models.IntegerField(default=None, null=True,
                                    validators=[
                                        MaxValueValidator(65535),
                                        MinValueValidator(1)
                                    ])
    crypto = models.CharField(max_length=40, default=None, blank=True, null=True)
    BSSID = models.CharField(max_length=17, default=None, blank=True, null=True, validators=[RegexValidator(
        regex='^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$',
        message='MAC Address must be valid',
        code='invalid_mac_address'
    )])
    notes = models.TextField(default=None, blank=True, null=True)
    client = models.ManyToManyField(Interface, blank=True)
    first_seen = models.DateTimeField(default=timezone.now, blank=True, verbose_name='first_seen')
    last_seen = models.DateTimeField(default=timezone.now, blank=True, verbose_name='last_seen')

    def __str__(self):
        return self.name


class Entity(models.Model):
    class Status(models.TextChoices):
        UP = 'UP', _('Up')
        DOWN = 'DOWN', _('Down')

    name = models.CharField(max_length=253)
    type = models.CharField(max_length=40, default=None, blank=True, null=True)
    os = models.CharField(max_length=40, default=None, blank=True, null=True)
    hardware = models.CharField(max_length=40, default=None, blank=True, null=True)
    status = models.CharField(max_length=4, choices=Status.choices, default=Status.DOWN)
    notes = models.TextField(default=None, blank=True, null=True)
    interface = models.ManyToManyField(Interface, blank=True)
    first_seen = models.DateTimeField(default=timezone.now, blank=True, verbose_name='first_seen')
    last_seen = models.DateTimeField(default=timezone.now, blank=True, verbose_name='last_seen')

    def __str__(self):
        return self.name
