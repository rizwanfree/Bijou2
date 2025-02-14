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
    houses = House.objects.all()
    if request.method == "POST":
        start_date = request.POST.get('checkIn')
        end_date = request.POST.get('checkOut')

        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                if end_date <= start_date:
                    return HttpResponseBadRequest("Check-out date must be after check-in date.")
            except ValueError:
                return HttpResponseBadRequest("Invalid date format. Please use YYYY-MM-DD.")
        else:
            start_date = None
            end_date = None

        # Attach availability info for each house
        for house in houses:
            house.is_available_for_dates = house.check_availability(start_date, end_date) if start_date and end_date else None

        # Paginate all houses
        paginator = Paginator(houses, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)


        context = {
            'page_obj': page_obj,
            'start_date': start_date,
            'end_date': end_date
        }

        return render(request, 'main-web/house-list.html', context)

    # Paginate all houses
    paginator = Paginator(houses, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
    'page_obj': page_obj,
    }
    return render(request, 'main-web/house-list.html', context)

def house_details(request, slug):
    house = get_object_or_404(House, slug=slug)  # Fetch by slug

    check_in = request.GET.get('checkIn')
    check_out = request.GET.get('checkOut')

    property = house.property    

    price_per_night = house.price_per_night  # Assuming `price` field exists
    total_price = price_per_night  # Default price for 1 night

    if check_in and check_out:
        try:
            check_in = datetime.strptime(check_in, "%Y-%m-%d")
            check_out = datetime.strptime(check_out, "%Y-%m-%d")
            nights = (check_out - check_in).days
            if nights > 0:
                total_price = price_per_night * nights
        except ValueError:
            pass  # Handle invalid date format gracefully

    context = {
        'house': house,
        'checkin': check_in,
        'checkout': check_out,
        'total_price': total_price,
        'property': property,
        
    }

    return render(request, 'main-web/house-details.html', context)



def payment_methods(request, id):
    house = get_object_or_404(House, id=id)
    payment_methods = PaymentMethod.objects.all()
    image = HouseImage.objects.filter(house=house).first()  # Get first image if exists

    # Get dates from request
    checkin = request.GET.get('checkIn')
    checkout = request.GET.get('checkOut')

    # Default values if no dates are provided
    if checkin and checkout:
        checkin_date = datetime.strptime(checkin, "%Y-%m-%d").date()
        checkout_date = datetime.strptime(checkout, "%Y-%m-%d").date()
        total_nights = (checkout_date - checkin_date).days
    else:
        checkin_date = None
        checkout_date = None
        total_nights = 1  # Default to 1 night if no dates

    # Calculate price
    total_price = house.price_per_night * total_nights

    print(checkin_date, checkout_date)
    return render(request, 'main-web/payment-methods.html', {
        'house': house,
        'house_image': image,
        'payment_methods': payment_methods,
        'checkin_date': checkin_date,
        'checkout_date': checkout_date,
        'total_nights': total_nights,
        'total_price': total_price,
    })



