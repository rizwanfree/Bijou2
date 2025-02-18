from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.utils.text import slugify
import requests


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
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_rooms = models.IntegerField(default=1)
    description = models.TextField(blank=True, null=True)
    is_available = models.BooleanField(default=True)  # This is still needed to mark the house as available

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def check_availability(self, start_date, end_date):
        """Check if the house is available for the requested date range."""
        if not start_date or not end_date:
            return True  # If no dates are provided, consider it available

        overlapping_bookings = Booking.objects.filter(
            house=self,
            check_in__lt=end_date,  # Overlapping booking check
            check_out__gt=start_date
        )

        return not overlapping_bookings.exists()


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
    is_available = models.BooleanField(default=True)  # Ensuring new rooms start as available
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def check_availability(self, start_date, end_date):
        # Check if there are any bookings overlapping with the requested dates
        overlapping_bookings = Booking.objects.filter(
            room=self,
            check_in__lt=end_date,
            check_out__gt=start_date
        )
        return not overlapping_bookings.exists()

    def __str__(self):
        return f"Room: {self.name} - {self.property.name}"

class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='room_images/')
    caption = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"Image for {self.room.name}"
    


class Booking(models.Model):
    tenant = models.ForeignKey(User, on_delete=models.CASCADE)
    house = models.ForeignKey(House, null=True, blank=True, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, null=True, blank=True, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['check_in', 'check_out']),
        ]

    def clean(self):
        # Enforce that exactly one of house or room is set
        if (self.house and self.room) or (not self.house and not self.room):
            raise ValidationError("Booking must be for either a House or a Room (but not both).")
        if self.check_out <= self.check_in:
            raise ValidationError("Check-out date must be after check-in date.")
        # Check availability
        if self.house and not self.house.is_available(self.check_in, self.check_out):
            raise ValidationError("This house is not available for the selected dates.")
        if self.room and not self.room.is_available(self.check_in, self.check_out):
            raise ValidationError("This room is not available for the selected dates.")

    def __str__(self):
        if self.house:
            return f"Booking for House: {self.house.name} ({self.check_in} to {self.check_out})"
        else:
            return f"Booking for Room: {self.room.name} ({self.check_in} to {self.check_out})"
