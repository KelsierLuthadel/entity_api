from django.contrib import admin

from entity.models import Interface, Entity, Resource, SSID

admin.site.register(SSID)
admin.site.register(Resource)
admin.site.register(Interface)
admin.site.register(Entity)
