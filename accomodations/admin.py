from django.contrib import admin
from django.contrib.auth.models import User
from .models import Property, Room, HouseImage, RoomImage, Amenity, House, Booking

# Register your models here.


class BookingAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "tenant":
            # Only include users that have a TenantProfile
            kwargs["queryset"] = User.objects.filter(tenant_profile__isnull=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    

class PropertyAdmin(admin.ModelAdmin):
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "managers":
            # ✅ Only include users that have a PropertyManagerProfile
            kwargs["queryset"] = User.objects.filter(manager_profile__isnull=False)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

admin.site.register(Property, PropertyAdmin)
admin.site.register(Room)
admin.site.register(House)

admin.site.register(Booking, BookingAdmin)

admin.site.register(HouseImage)
admin.site.register(RoomImage)

admin.site.register(Amenity)