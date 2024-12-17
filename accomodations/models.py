from django.db import models
from django.contrib.auth.models import User


class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Property(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    description = models.TextField(blank=True, null=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    amenities = models.ManyToManyField('Amenity', related_name='properties', blank=True)
    rules = models.TextField(blank=True, null=True)
    managers = models.ManyToManyField(User, related_name='managed_properties_list', blank=True)  # Updated related_name
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')  # Link to Property
    image = models.ImageField(upload_to='img/property_images/')
    caption = models.CharField(max_length=255, blank=True, null=True)  # Optional caption

    def __str__(self):
        return f"Image for {self.property.name}"


class Room(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.property.name}"


class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='images')  # Link to Room
    image = models.ImageField(upload_to='room_images/')
    caption = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Image for {self.room.name}"