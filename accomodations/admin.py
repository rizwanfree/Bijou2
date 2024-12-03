from django.contrib import admin

from .models import Property, Room, PropertyImage, RoomImage, Amenity

# Register your models here.

admin.site.register(Property)
admin.site.register(Room)

admin.site.register(PropertyImage)
admin.site.register(RoomImage)

admin.site.register(Amenity)