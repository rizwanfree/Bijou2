from django.shortcuts import render

from accomodations.models import PropertyImage, RoomImage
# Create your views here.


def index(request):
    return render(request, 'main-web/index-2.html')


def about(request):
    return render(request, 'main-web/about.html')


def services(request):
    return render(request, 'main-web/index-2.html')


def gallery(request):
    property_images = PropertyImage.objects.all()
    
    return render(request, 'main-web/gallery.html', {"property_images": property_images})


def contact(request):
    return render(request, 'main-web/contacts.html')


def room_list(request):
    return render(request, 'main-web/room-list.html')


