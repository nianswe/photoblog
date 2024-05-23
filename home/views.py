from django.shortcuts import render
from django.views import generic
from blog import models

# Create your views here.


def photo_home(request):
    photos = models.Photo.objects.all()
    return render(request, 'home/index.html', context={'photos': photos})


