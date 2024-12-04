from django.contrib.auth.models import User
from django.db import models

from django.contrib.auth.models import AbstractUser
from accomodations.models import Property

class TenantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tenant_profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)  # Tenant's address

    def __str__(self):
        return f"Tenant: {self.user.username}"
    



class PropertyManagerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='manager_profile')
    managed_properties = models.ManyToManyField(Property, related_name='assigned_managers', blank=True)

    def __str__(self):
        return f"Manager: {self.user.username}"
    

