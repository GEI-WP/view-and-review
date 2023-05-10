from typing import Any, Dict
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden, QueryDict
from django.views.generic.edit import DeleteView, UpdateView
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods 
from django.contrib.auth.models import User
from django.views import generic

from web.models import Rating, Reputation
from web.forms import RegisterForm, RatingForm, ReputationForm

from . import api

# Create your views here.


class IndexView(generic.TemplateView):
    template_name = "web/index.html"
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        context['popular'] = api.popular(number=20)
        context['latest'] = api.latest(number=20)
        context['top_films'] = api.top_most_rated(number=20)
        context['top_batfilms'] = api.top_most_rated_includes(includes="Batman")
        
        return context

class FilmView(generic.TemplateView):
    template_name = 'web/film.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = {}
        # Can raise 404
        film = api.film(kwargs['pk'])           
        context['film'] = film
        context['RATING_CHOICES'] = Rating.RATING_CHOICES
        context['form'] = RatingForm(initial={'film': film['id']})
        context['ratings'] = Rating.objects.filter(film=film['id'])
        if self.request.user.is_authenticated:
            user_rating = Rating.objects.filter(user=self.request.user, film=film['id']).first()
            if user_rating:
                context['form'] = RatingForm(instance=user_rating)
                context['user_rating'] = user_rating

        # Gets the form prefilled with the user's past choices
        return context

class LogoutView(generic.TemplateView):
    template_name = 'registration/logout.html'


class ProfileView(generic.TemplateView):
    template_name = 'auth/profile_settings.html'
    

def RegisterView(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration succesful " + str(user))
            return redirect('/')
        messages.error(
            request, "Unsuccesful registration. Invalid information.")
    return render(request=request, template_name='registration/register.html', context={"form": form})

@login_required
@require_http_methods(['POST', 'DELETE', 'PUT'])
def reputation(request):     
    if request.method == 'POST':   
        form = ReputationForm(request.POST)
        if form.is_valid():
            form.save()
    if request.method == 'PUT':   
        data = QueryDict(request.body)
        new_value = data.get('value') == 'true'
        Reputation.objects.filter(user=data.get('user'), rating=data.get('rating')).update(value=new_value)
    if request.method == 'DELETE':
        data = QueryDict(request.body)
        Reputation.objects.filter(user=data.get('user'), rating=data.get('rating')).delete()
    return HttpResponse()
            
@login_required
def userUpdateView(request, pk):
    user = get_object_or_404(User, pk=pk)

    if user != request.user:
        return HttpResponseForbidden("Cannot update other's account")

    username = QueryDict(request.body).get('username')

    db_user = User.objects.filter(username=username)
    if db_user.exists():
        return HttpResponseForbidden("A user already has that username!")
    
    user.username = username
    user.save()
    return HttpResponse()

class UserDeleteView(DeleteView):
    model = User
    
    def form_valid(self, form):
        self.object = self.get_object()
        if self.object == self.request.user:
            self.object.delete()
            return HttpResponseRedirect('/')
        else:
            return HttpResponseForbidden("Cannot delete other's account")


@login_required
@require_http_methods(['GET', 'POST'])
def ratingDelete(request, film_id):
    object = Rating.objects.filter(film=film_id, user=request.user).first()
    if request.method == 'GET':
        return render(request=request, template_name='web/rating_confirm_delete.html', context={'object': object})
        
    # POST request logic
    object.delete()
    return HttpResponseRedirect(reverse('film', args=(film_id)))    

@login_required
@require_http_methods(['POST'])
def rate(request, film_id):
    form = RatingForm(request.POST)
    if form.is_valid():
        # Process the data in form.cleaned_data
        rating = form.save(commit=False)
        rating.user = User.objects.get(username=request.user)
        old_rating = Rating.objects.filter(user=rating.user)
        if old_rating.exists():
            old_rating.update(score=rating.score, review=rating.review, review_title=rating.review_title)
        else:
            rating.save()
        return HttpResponseRedirect(reverse('film', args=(film_id,)))
    else:
        messages.error(request, "Unsuccesful review. Invalid information: " + str(form.errors))
    