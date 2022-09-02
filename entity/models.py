from django.utils.translation import gettext_lazy as _
from django.db import models


class Resource(models.Model):
    class Status(models.TextChoices):
        TCP = 'TCP', _('TCP')
        UDP = 'UDP', _('UDP')

    port = models.IntegerField()
    type = models.CharField(max_length=3, choices=Status.choices, default=Status.TCP)
    notes = models.CharField(max_length=255, default=None, blank=True, null=True)

    def __str__(self):
        return "{type}({port})".format(type=self.type, port=str(self.port))


class Address(models.Model):
    hostname = models.CharField(max_length=253, default=None, blank=True, null=True)
    ip_v4 = models.GenericIPAddressField(default=None, blank=True, null=True)
    ip_v6 = models.GenericIPAddressField(default=None, blank=True, null=True)
    resources = models.ManyToManyField(Resource)
    mac_address = models.CharField(max_length=17, default=None, blank=True, null=True)
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
    first_seen = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='date found')
    last_seen = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='date seen')

    def __str__(self):
        return self.name





