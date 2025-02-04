from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import requests


class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Facility(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Property(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    amenities = models.ManyToManyField('Amenity', related_name='properties', blank=True)
    rules = models.TextField(blank=True, null=True)
    managers = models.ManyToManyField(User, related_name='managed_properties', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)  

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        # If latitude and longitude are not set, fetch them using geocoding API
        if not self.latitude or not self.longitude:
            self.set_coordinates()

        super().save(*args, **kwargs)

    def set_coordinates(self):
        """Fetch coordinates using OpenStreetMap (Nominatim) API"""
        address_string = f"{self.address}, {self.city}, {self.state}, {self.zip_code}"
        url = f"https://nominatim.openstreetmap.org/search?q={address_string}&format=json"
        
        try:
            response = requests.get(url, headers={'User-Agent': 'Django-App'})
            response.raise_for_status()
            data = response.json()
            
            if data:
                self.latitude = float(data[0]['lat'])
                self.longitude = float(data[0]['lon'])
        except Exception as e:
            print("Error fetching coordinates:", e)

    def __str__(self):
        return self.name

class House(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='houses')
    name = models.CharField(max_length=255)
    no_of_bathroom = models.IntegerField(default=1)
    slug = models.SlugField(unique=True, blank=True)
    facilities = models.ManyToManyField('Facility', related_name='houses', blank=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_rooms = models.IntegerField(default=1)
    description = models.TextField(blank=True, null=True)
    is_available = models.BooleanField(default=True)  # Ensuring new houses start as available

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"House: {self.name} - {self.property.name}"

class HouseImage(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='images')  # Renamed from `property`
    image = models.ImageField(upload_to='house_images/')
    caption = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"Image for {self.house.name}"

class Room(models.Model):
    TYPE_OF_BED = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('queen', 'Queen'),
        ('king', 'King'),
    ]
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    capacity = models.PositiveIntegerField(default=1)
    number_of_bed = models.PositiveIntegerField(default=1)
    type_of_bed = models.CharField(choices=TYPE_OF_BED, max_length=50, default='single')
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    facilities = models.ManyToManyField('Facility', related_name='rooms', blank=True)
    is_available = models.BooleanField(default=True)  # Ensuring new rooms start as available
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Room: {self.name} - {self.property.name}"

class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='room_images/')
    caption = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"Image for {self.room.name}"
