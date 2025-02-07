from datetime import datetime
from pyexpat.errors import messages
from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from accomodations.models import HouseImage, RoomImage, Room, House
from finances.models import PaymentMethod
from django.views.decorators.clickjacking import xframe_options_exempt
from django.core.exceptions import ValidationError

# Create your views here.

def index(request):
    return render(request, 'main-web/index-2.html')

def about(request):
    return render(request, 'main-web/about.html')

def contact(request):
    return render(request, 'main-web/contact-us.html')



def room_list(request):
    """List all rooms and show if they are available for selected dates."""
    start_date = request.GET.get('checkIn')
    end_date = request.GET.get('checkOut')

    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            if end_date <= start_date:
                return HttpResponseBadRequest("Check-out date must be after check-in date.")
            total_nights = (end_date - start_date).days
        except ValueError:
            return HttpResponseBadRequest("Invalid date format. Please use YYYY-MM-DD.")
    else:
        start_date = None
        end_date = None
        total_nights = 1  # Default to 1 night if no dates are selected

    # Show all rooms, don't filter them out
    rooms = Room.objects.all()

    # Attach availability info for each room
    for room in rooms:
        room.is_available_for_dates = room.check_availability(start_date, end_date) if start_date and end_date else None

    # Paginate all rooms
    paginator = Paginator(rooms, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Calculate price for total nights per room
    for room in page_obj:
        room.price_for_total_nights = room.price_per_night * total_nights

    context = {
        'page_obj': page_obj,
        'start_date': start_date,
        'end_date': end_date,
        'total_nights': total_nights,
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
    """List all houses and show if they are available for selected dates."""
    start_date = request.GET.get('checkIn')
    end_date = request.GET.get('checkOut')

    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            if end_date <= start_date:
                return HttpResponseBadRequest("Check-out date must be after check-in date.")
            total_nights = (end_date - start_date).days
        except ValueError:
            return HttpResponseBadRequest("Invalid date format. Please use YYYY-MM-DD.")
    else:
        start_date = None
        end_date = None
        total_nights = 1  # Default to 1 night if no dates are selected

    # Show all houses, don't filter them out
    houses = House.objects.all()

    # Attach availability info for each house
    for house in houses:
        house.is_available_for_dates = house.check_availability(start_date, end_date) if start_date and end_date else None

    # Paginate all houses
    paginator = Paginator(houses, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Calculate price for total nights per house
    for house in page_obj:
        house.price_for_total_nights = house.price_per_night * total_nights

    context = {
        'page_obj': page_obj,
        'start_date': start_date,
        'end_date': end_date,
        'total_nights': total_nights,
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