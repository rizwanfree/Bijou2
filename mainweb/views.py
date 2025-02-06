from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from accomodations.models import HouseImage, RoomImage, Room, House
from finances.models import PaymentMethod
from django.views.decorators.clickjacking import xframe_options_exempt

# Create your views here.

def index(request):
    return render(request, 'main-web/index-2.html')

def about(request):
    return render(request, 'main-web/about.html')

def contact(request):
    return render(request, 'main-web/contact-us.html')



def room_list(request):
    """List all available rooms with pagination."""
    rooms = Room.objects.filter(is_available=True)  # Only show available rooms
    paginator = Paginator(rooms, 5)  # Show 5 rooms per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

        # Calculate price for 7 nights per room
    for room in page_obj:
        room.price_for_seven_nights = room.price_per_night * 7

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'main-web/room-list.html', context)

def room_details(request, slug):
    """Show details for a specific room."""
    room = get_object_or_404(Room, slug=slug)
    property_obj = room.property
    
    context = {
        'room': room,
        'property': property_obj
    }
    return render(request, "main-web/room.html", context)

def house_list(request):
    """List all available houses with pagination."""
    houses = House.objects.filter(is_available=True)  # Only show available houses
    paginator = Paginator(houses, 5)  # Show 5 houses per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Calculate price for 7 nights per house
    for house in page_obj:
        house.price_for_seven_nights = house.price_per_night * 7

    context = {
        'page_obj': page_obj,  # Pass paginated object
    }
    return render(request, 'main-web/house-list.html', context)


def house_details(request, slug):
    """Show details for a specific house with map location."""
    house = get_object_or_404(House, slug=slug)
    property_obj = house.property  # Get the associated property

    context = {
        'house': house,
        'property': property_obj,  # Pass property data including lat/lng
    }
    return render(request, "main-web/house-details.html", context)


def payment_methods(request):
    payment_methods = PaymentMethod.objects.all()
    return render(request, 'main-web/payment-methods.html', {'payment_methods': payment_methods})

@xframe_options_exempt
def payment_methods_iframe(request):
    payment_methods = PaymentMethod.objects.all()
    return render(request, 'main-web/payment-methods-iframe.html', {'payment_methods': payment_methods})