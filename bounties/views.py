from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Pirate

# TODO: refactor. Tries to do too many things in one method
def index(request):
    pirates = Pirate.objects.all()
    keyword = request.GET.get('pirate-search-field')
    
    if keyword:
        results = Pirate.objects.filter(name__icontains=keyword)

        if results.count() == 1:
            return redirect('/onepiecebounties/%d/' % (results.first().id,))
        elif results.count() > 1:
            return render(request, 'list.html')
    
    return render(request, 'index.html', {'pirates' : pirates})

def get_pirate(request, pirate_id):
    pirates = Pirate.objects.all()
    pirate = Pirate.objects.get(id=pirate_id)
    return render(request, 'profile.html', {'pirate': pirate, 'pirates': pirates})
