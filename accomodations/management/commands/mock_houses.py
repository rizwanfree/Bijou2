from django.core.management.base import BaseCommand
from accomodations.models import House, Property, Facility
from django.utils.text import slugify

class Command(BaseCommand):
    help = "Populate the database with mock house data"

    def handle(self, *args, **kwargs):
        houses_data = [
            {
                "property_name": "The Grand Plaza",
                "name": "Luxury Suite",
                "no_of_bathroom": 2,
                "number_of_rooms": 3,
                "price_per_night": 250.00,
                "description": "A high-end luxury suite with city views.",
                "facilities": ["Gym", "Pool", "Wi-Fi"]
            },
            {
                "property_name": "The Grand Plaza",
                "name": "Family Penthouse",
                "no_of_bathroom": 3,
                "number_of_rooms": 4,
                "price_per_night": 350.00,
                "description": "Spacious penthouse for families with top amenities.",
                "facilities": ["Wi-Fi", "Parking", "Laundry"]
            },
            {
                "property_name": "Ocean Breeze Resort",
                "name": "Beachfront Villa",
                "no_of_bathroom": 2,
                "number_of_rooms": 2,
                "price_per_night": 200.00,
                "description": "Villa with direct beach access and private pool.",
                "facilities": ["Pool", "AC", "Private Beach"]
            },
            {
                "property_name": "Mountain View Lodge",
                "name": "Cozy Cabin",
                "no_of_bathroom": 1,
                "number_of_rooms": 1,
                "price_per_night": 180.00,
                "description": "A peaceful wooden cabin with stunning mountain views.",
                "facilities": ["Fireplace", "Wi-Fi", "Balcony"]
            },
            {
                "property_name": "Sunset Apartments",
                "name": "Sunset Loft",
                "no_of_bathroom": 2,
                "number_of_rooms": 3,
                "price_per_night": 300.00,
                "description": "Modern loft with smart home features and rooftop access.",
                "facilities": ["Rooftop Access", "Parking", "Smart Home"]
            },
            {
                "property_name": "City Heights Tower",
                "name": "Executive Condo",
                "no_of_bathroom": 1,
                "number_of_rooms": 2,
                "price_per_night": 220.00,
                "description": "A high-rise executive condo with city skyline views.",
                "facilities": ["Gym", "Concierge", "Security"]
            }
        ]

        available_facilities = {facility.name: facility for facility in Facility.objects.all()}

        for data in houses_data:
            property_obj = Property.objects.filter(name=data["property_name"]).first()
            if not property_obj:
                self.stdout.write(self.style.WARNING(f"Property '{data['property_name']}' not found. Skipping..."))
                continue

            house, created = House.objects.get_or_create(
                property=property_obj,
                name=data["name"],
                defaults={
                    "no_of_bathroom": data["no_of_bathroom"],
                    "number_of_rooms": data["number_of_rooms"],
                    "price_per_night": data["price_per_night"],
                    "description": data["description"],
                    "slug": slugify(data["name"])
                }
            )

            facility_objects = [available_facilities[facility] for facility in data["facilities"] if facility in available_facilities]
            if facility_objects:
                house.facilities.set(facility_objects)

            house.save()

            self.stdout.write(self.style.SUCCESS(f"Added House: {house.name}"))

        self.stdout.write(self.style.SUCCESS("Mock houses added successfully!"))
