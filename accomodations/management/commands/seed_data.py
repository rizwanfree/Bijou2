import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from accomodations.models import Amenity, Facility, Property, House, Room

class Command(BaseCommand):
    help = "Seeds the database with mock data (6 houses, 6 rooms total)"

    def handle(self, *args, **kwargs):
        # Create Amenity Data
        amenities = ["WiFi", "Air Conditioning", "Heating", "TV", "Parking", "Swimming Pool"]
        for name in amenities:
            Amenity.objects.get_or_create(name=name)

        # Create Facility Data
        facilities = ["Security", "Power Backup", "CCTV", "Laundry", "Garden", "Elevator"]
        for name in facilities:
            Facility.objects.get_or_create(name=name)

        # Ensure an admin user exists
        admin_user, _ = User.objects.get_or_create(username="admin", defaults={"is_staff": True, "is_superuser": True})

        # Create a single Property
        property_obj, _ = Property.objects.get_or_create(
            name="Sunset Villa",
            defaults={
                "address": "123 Beachside Ave",
                "city": "Miami",
                "state": "FL",
                "zip_code": "33101",
                "description": "A luxurious villa with ocean views.",
                "slug": slugify("Sunset Villa"),
            },
        )
        property_obj.managers.add(admin_user)
        property_obj.amenities.set(Amenity.objects.all())

        # Create 6 Houses
        houses = []
        for i in range(6):
            house_name = f"House {i+1}"
            house, _ = House.objects.get_or_create(
                property=property_obj,
                name=house_name,
                slug=slugify(house_name),
                no_of_bathroom=random.randint(1, 3),
                price_per_night=random.uniform(80, 300),
                number_of_rooms=random.randint(1, 5),
                is_available=True,
            )
            house.facilities.set(Facility.objects.order_by('?')[:3])  # Random 3 facilities
            houses.append(house)

        # Create 6 Rooms
        bed_types = ["single", "double", "queen", "king"]
        for i in range(6):
            room_name = f"Room {i+1}"
            room, _ = Room.objects.get_or_create(
                property=property_obj,
                name=room_name,
                slug=slugify(room_name),
                capacity=random.randint(1, 4),
                number_of_bed=random.randint(1, 2),
                type_of_bed=random.choice(bed_types),
                price_per_night=random.uniform(40, 250),
                is_available=True,
            )
            room.facilities.set(Facility.objects.order_by('?')[:2])  # Random 2 facilities

        self.stdout.write(self.style.SUCCESS("6 houses and 6 rooms inserted successfully!"))
