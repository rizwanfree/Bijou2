from django.contrib import admin
from .models import TenantProfile, PropertyManagerProfile

@admin.register(TenantProfile)
class TenantProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address')

@admin.register(PropertyManagerProfile)
class PropertyManagerProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    filter_horizontal = ('managed_properties',)
