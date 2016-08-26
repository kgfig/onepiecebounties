from django.shortcuts import render
from django.http import HttpResponse
from .models import Pirate

def index(request):
    pirates = Pirate.objects.all()
    return render(request, 'index.html', context={'pirates' : pirates})
