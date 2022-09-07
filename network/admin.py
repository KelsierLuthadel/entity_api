from django.contrib import admin

from network.models import Site, Network, Switch, WiFi, Machine, Interface, Resource, Bluetooth, Radio

admin.site.register(Site)
admin.site.register(Network)
admin.site.register(Switch)
admin.site.register(WiFi)
admin.site.register(Machine)
admin.site.register(Interface)
admin.site.register(Resource)
admin.site.register(Bluetooth)
admin.site.register(Radio)
