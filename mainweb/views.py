from django.shortcuts import render

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
    price_for_seven_nights = 0
    for room in rooms:
        price_for_seven_nights = room.price_per_night * 7
    
    context = {
        'rooms': rooms,
        'price_for_seven_nights': price_for_seven_nights,
    }
    return render(request, 'main-web/room-list.html', context)


def house_list(request):
    return render(request, 'main-web/room-list.html')


