from django.shortcuts import render
from django.views import generic
from blog import models


def home(request):
    photos = models.Photo.objects.filter(pubstatus='SH')
    return render(request, 'home/index.html', context={'photos': photos})
