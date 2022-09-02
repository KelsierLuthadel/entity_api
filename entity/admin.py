from django.contrib import admin

from entity.models import Address, Entity, Resource

admin.site.register(Resource)
admin.site.register(Address)
admin.site.register(Entity)
