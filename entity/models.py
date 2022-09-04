from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models


class Resource(models.Model):
    class Status(models.TextChoices):
        TCP = 'TCP', _('TCP')
        UDP = 'UDP', _('UDP')

    port = models.IntegerField(validators=[
            MaxValueValidator(65535),
            MinValueValidator(1)
        ])
    type = models.CharField(max_length=3, choices=Status.choices, default=Status.TCP)
    notes = models.CharField(max_length=255, default=None, blank=True, null=True)

    def __str__(self):
        return "{type}({port})".format(type=self.type, port=str(self.port))


class Address(models.Model):
    hostname = models.CharField(max_length=253, default=None, blank=True, null=True)
    ip_v4 = models.GenericIPAddressField(default=None, blank=True, null=True)
    ip_v6 = models.GenericIPAddressField(default=None, blank=True, null=True)
    resource = models.ManyToManyField(Resource)
    mac_address = models.CharField(max_length=17, default=None, blank=True, null=True, validators=[RegexValidator(
            regex='^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$',
            message='MAC Address must be valid',
            code='invalid_mac_address'
        )])
    mac_vendor = models.CharField(max_length=255, default=None, blank=True, null=True)

    def __str__(self):
        return self.ip_v4


class Entity(models.Model):
    class Status(models.TextChoices):
        UP = 'UP', _('Up')
        DOWN = 'DOWN', _('Down')

    name = models.CharField(max_length=253)
    notes = models.CharField(max_length=255, default=None, blank=True, null=True)
    address = models.ManyToManyField(Address)
    status = models.CharField(max_length=4, choices=Status.choices, default=Status.DOWN)
    os = models.CharField(max_length=255, default=None, blank=True, null=True)
    type = models.CharField(max_length=255, default=None, blank=True, null=True)
    hardware = models.CharField(max_length=255, default=None, blank=True, null=True)
    first_seen = models.DateTimeField(default=timezone.now, blank=True, verbose_name='first_seen')
    last_seen = models.DateTimeField(default=timezone.now, blank=True, verbose_name='last_seen')

    def __str__(self):
        return self.name





