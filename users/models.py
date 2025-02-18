from django.contrib.auth.models import User
from django.db import models
from django.forms import ValidationError

from accomodations.models import Property, Room, House


class TenantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tenant_profile')
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    rented_room = models.ForeignKey(Room, null=True, blank=True, on_delete=models.SET_NULL, related_name='tenants')
    rented_house = models.ForeignKey(House, null=True, blank=True, on_delete=models.SET_NULL, related_name='tenants')

    def clean(self):
        """Ensure a tenant can only rent either a room or a house, not both."""
        if self.rented_room and self.rented_house:
            raise ValidationError("A tenant can rent either a Room or a House, not both.")

    def save(self, *args, **kwargs):
        """Mark room or house as unavailable when assigned, and restore availability when changed."""
        
        # Fetch the existing TenantProfile from the database (if updating)
        if self.pk:
            existing_tenant = TenantProfile.objects.get(pk=self.pk)

            # If the tenant was previously renting a room and switched, make the old room available
            if existing_tenant.rented_room and existing_tenant.rented_room != self.rented_room:
                existing_tenant.rented_room.is_available = True
                existing_tenant.rented_room.save()

            # If the tenant was previously renting a house and switched, make the old house available
            if existing_tenant.rented_house and existing_tenant.rented_house != self.rented_house:
                existing_tenant.rented_house.is_available = True
                existing_tenant.rented_house.save()

        # Mark new rented room or house as unavailable
        if self.rented_room:
            self.rented_room.is_available = False
            self.rented_room.save()
        if self.rented_house:
            self.rented_house.is_available = False
            self.rented_house.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """When tenant profile is deleted, make the rented room or house available again."""
        if self.rented_room:
            self.rented_room.is_available = True
            self.rented_room.save()
        if self.rented_house:
            self.rented_house.is_available = True
            self.rented_house.save()

        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Tenant: {self.user.username}"


class PropertyManagerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='manager_profile')
    first_name = models.CharField(max_length=50, blank=True, null=True)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    managed_properties = models.ManyToManyField(Property, related_name='assigned_managers', blank=True)

    def __str__(self):
        return f"Manager: {self.user.first_name} {self.user.last_name}"