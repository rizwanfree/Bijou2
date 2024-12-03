from django.db import models


class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Amenity name (e.g., Wi-Fi, Pool)

    def __str__(self):
        return self.name

# Create your models here.
class Property(models.Model):
    name = models.CharField(max_length=255)  # Property name or title
    address = models.TextField()  # Full address
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    description = models.TextField(blank=True, null=True)  # Detailed description of the property
    image = models.ImageField(upload_to='property_images/', blank=True, null=True)  # Primary image
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)  # Average price per night
    amenities = models.ManyToManyField(Amenity, related_name='properties', blank=True)  # Many-to-many relationship
    rules = models.TextField(blank=True, null=True)  # House rules
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='rooms')  # Link to Property
    name = models.CharField(max_length=255)  # Room name or identifier
    capacity = models.PositiveIntegerField()  # Number of people the room can accommodate
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)  # Room-specific price
    description = models.TextField(blank=True, null=True)  # Detailed description of the room
    images = models.ImageField(upload_to='room_images/', blank=True, null=True)  # Primary image
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.property.name}"

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_images')
    image = models.ImageField(upload_to='property_images/')
    caption = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Image for {self.property.name}"

class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_images')
    image = models.ImageField(upload_to='room_images/')
    caption = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Image for {self.room.name}"