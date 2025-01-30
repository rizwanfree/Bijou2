from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from accomodations.models import PropertyImage, RoomImage, Room, Property
# Create your views here.


def index(request):
    return render(request, 'main-web/index-2.html')


def about(request):
    return render(request, 'main-web/about.html')


def services(request):
    return render(request, 'main-web/index-2.html')


def gallery(request):
    property_images = PropertyImage.objects.select_related('property').all()
    return render(request, 'main-web/gallery.html', {"property_images": property_images})


def contact(request):
    return render(request, 'main-web/contacts.html')


def room_list(request):
    rooms = Room.objects.all()
    paginator = Paginator(rooms, 5)  # Show 5 rooms per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,  # Use `page_obj` instead of `rooms`
    }
    return render(request, 'main-web/room-list.html', context)


def room_details(request, slug):
    room = get_object_or_404(Room, slug=slug)  # Get room by slug
    context = {
        'room': room,
    }
    return render(request, "main-web/room.html", context)


def house_list(request):
    houses = Property.objects.all()
    paginator = Paginator(houses, 5)  # Show 5 houses per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Calculate price for 7 nights per house (if needed)
    for house in page_obj:
        house.price_for_seven_nights = house.price_per_night * 7

    context = {
        'houses': page_obj,  # Pass the paginated object to the template
    }
    return render(request, 'main-web/house-list.html', context)


