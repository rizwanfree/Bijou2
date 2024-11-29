from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'main-web/index-2.html')


def about(request):
    return render(request, 'main-web/about.html')


def services(request):
    return render(request, 'main-web/index-2.html')


def gallery(request):
    return render(request, 'main-web/gallery.html')


def contact(request):
    return render(request, 'main-web/contacts.html')


