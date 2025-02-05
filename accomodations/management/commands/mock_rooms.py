import random
from django.core.management.base import BaseCommand
from accomodations.models import Room, Property, Facility
from django.utils.text import slugify

class Command(BaseCommand):
    help = "Populate the database with mock room data"

    def handle(self, *args, **kwargs):
        if not Property.objects.exists():
            self.stdout.write(self.style.ERROR("No properties found. Please add properties first."))
            return

        room_data = [
            {
                "name": "Deluxe Room",
                "capacity": 2,
                "number_of_bed": 1,
                "type_of_bed": "king",
                "price_per_night": 150.00,
                "description": "A luxurious room with a king-sized bed and modern amenities.",
            },
            {
                "name": "Ocean View Room",
                "capacity": 2,
                "number_of_bed": 1,
                "type_of_bed": "queen",
                "price_per_night": 180.00,
                "description": "Room with a breathtaking view of the ocean and a private balcony.",
            },
            {
                "name": "Economy Room",
                "capacity": 1,
                "number_of_bed": 1,
                "type_of_bed": "single",
                "price_per_night": 75.00,
                "description": "A budget-friendly room for solo travelers.",
            },
            {
                "name": "Executive Suite",
                "capacity": 3,
                "number_of_bed": 2,
                "type_of_bed": "double",
                "price_per_night": 220.00,
                "description": "A spacious suite with premium facilities and a lounge area.",
            },
            {
                "name": "Family Room",
                "capacity": 4,
                "number_of_bed": 2,
                "type_of_bed": "queen",
                "price_per_night": 250.00,
                "description": "Perfect for families, featuring two queen beds and ample space.",
            },
        ]

        facilities = list(Facility.objects.all())  # Fetch all facilities

        properties = list(Property.objects.all())

        for property in properties:
            for data in room_data:
                room, created = Room.objects.get_or_create(
                    property=property,
                    name=data["name"],
                    defaults={
                        "capacity": data["capacity"],
                        "number_of_bed": data["number_of_bed"],
                        "type_of_bed": data["type_of_bed"],
                        "price_per_night": data["price_per_night"],
                        "description": data["description"],
                        "slug": slugify(data["name"]),
                        "is_available": random.choice([True, False]),  # Randomly assign availability
                    }
                )

                if created:
                    selected_facilities = random.sample(facilities, min(3, len(facilities)))  # Assign up to 3 random facilities
                    room.facilities.set(selected_facilities)
                    self.stdout.write(self.style.SUCCESS(f"Added room: {room.name} to {property.name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Room {room.name} already exists in {property.name}"))

        self.stdout.write(self.style.SUCCESS("Room population complete!"))
