from django.shortcuts import render
from django.views import generic

from web.models import Film 
from django.http import HttpResponse

# Create your views here.
def index(request):    
    films = Film.objects.all()
    context = {
        'films': films,
    }
    
    return render(request, 'web/index.html', context=context)

class FilmView(generic.DetailView):
    template_name = 'web/film.html'    
    model = Film