from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    pirates = [
        {'name': 'Iron Mace Alvida'},
        {'name': 'Monkey D. Luffy'},
        ]
    return render(request, 'index.html', context={'pirates' : pirates})
