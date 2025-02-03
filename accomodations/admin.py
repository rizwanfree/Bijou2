from django.contrib import admin

from .models import Property, Room, HouseImage, RoomImage, Amenity, Facility, House

# Register your models here.

admin.site.register(Property)
admin.site.register(Room)
admin.site.register(House)

admin.site.register(HouseImage)
admin.site.register(RoomImage)

admin.site.register(Amenity)
admin.site.register(Facility)