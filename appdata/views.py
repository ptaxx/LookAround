from random import randint
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from .forms import (
    SignUpForm, 
    GameCreationForm, 
    ActivityCreationForm,
    VenueCreationForm,
    TeamCreationForm,
    )
from django.contrib import messages
from appdata.models import Activity, Game, Team, Area, CustomUser, Venue
from django.template import loader
from django.views.generic.edit import FormView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin


class GamePageView(View):
    def get(self, request, *args, **kwargs):
        game = Game.objects.get(id=kwargs.get('pk'))
        activities = game.activities.all()
        players = game.players.all()
        teams = Team.objects.filter(team_user__in=game.players.all()).distinct()  # search for teams, where at least 1 player is part of this game. So find all the teams that have players who are part of a specific game. And remove all dublicated teams.
        context = {'game': game, 'activities': activities, 'players': players, 'teams':teams}
        return render(request, 'gamepage.html', context)
    
class AreaPageView(View):
    def get(self, request, *args, **kwargs):
        area = Area.objects.get(id=kwargs.get('pk'))
        context = {'area': area}
        return render(request, 'areapage.html', context)
    

class VenuePageView(View):
    def get(self, request, *args, **kwargs):
        venue = Venue.objects.get(id=kwargs.get('pk'))
        context = {'venue': venue}
        return render(request, 'venuepage.html', context)
    
    
class ActivityView(View):
    def get(self, request, *args, **kwargs):
        activity = Activity.objects.get(id=kwargs.get('pk'))
        context = {'activity': activity}
        return render(request, 'activitypage.html', context)
    

class AreasPageView(View):
    def get(self, request, *args, **kwargs):
        areas = Area.objects.all()
        context = {'areas': areas}
        return render(request, 'areaspage.html', context)


class GamesPageView(View):
    def get(self, request, *args, **kwargs):
        games = Game.objects.all()
        context = {'games': games}
        return render(request, 'gamespage.html', context)
    

class IndexView(View):
    def get(self, request, *args, **kwargs):
        games = Game.objects.all()
        area = Area.objects.all()
        context = {'games': games, 'area': area,}
        return render(request, "index.html", context)

      
class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')  # Redirects to login if registration was successful
    
    def form_valid(self, form):
        messages.success(self.request, 'Registration was successful!')
        response = super().form_valid(form)
        return response
    

class UserPageViews(View):
    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.get(id=kwargs.get('pk'))
        # Find all teams where at least one player is part of
        teams = Team.objects.filter(
            team_user__in=user.game_set.values_list('players', flat=True)
            ).distinct()
        # Find all games where user is the player
        games = Game.objects.filter(players=user).distinct()
        context = {'user': user, 'teams': teams, 'games': games}
        return render(request, 'userpage.html', context)

    
class TeamPageViews(View):
    def get(self, request, *args, **kwargs):
        team = Team.objects.get(id=kwargs.get('pk'))
        teamplayers = team.team_user.all()
        context = {'team': team, 'teamplayers': teamplayers}
        return render(request, 'teampage.html', context)


class GameEntryView(FormView):
    form_class = GameCreationForm
    template_name = 'creategame.html'
    success_url = '/'
    def form_valid(self, form):
        self.game = Game.objects.create(
            area=form.cleaned_data.get('area'),
            starting_time=form.cleaned_data.get('starting_time'),
            finishing_time=form.cleaned_data.get('finishing_time'),
            availability=form.cleaned_data.get('availability'),
            )
        for player in form.cleaned_data['players']:
                self.game.players.add(player),
        return super(GameEntryView, self).form_valid(form)
    def get_success_url(self):
        return reverse('gamepage', kwargs={'pk': self.game.pk})
    
    
class ContactPage(View):
    def get(self, request):
        return render(request, 'contactpage.html')


class ActivityCreationFormView(FormView):
    template_name = 'createactivity.html'
    form_class = ActivityCreationForm
    success_url = '/'
    def form_valid(self, form):
        self.activity = Activity.objects.create(
            short_description=form.cleaned_data.get('short_description'),
            full_description=form.cleaned_data.get('full_description'),
            venue=form.cleaned_data.get('venue'),
            passcode=str(randint(10000,99999))
            )
        return super(ActivityCreationFormView, self).form_valid(form)
    def get_success_url(self):
        return reverse('activitypage', kwargs={'pk': self.activity.pk})
    
    
class VenueCreationFormView(FormView):
    template_name = 'createvenue.html'
    form_class = VenueCreationForm
    success_url = '/'
    def form_valid(self, form):
        self.venue = Venue.objects.create(
            name=form.cleaned_data.get('name'),
            area=form.cleaned_data.get('area'),
            opening_hour=form.cleaned_data.get('opening_hour'),
            closing_hour=form.cleaned_data.get('closing_hour'),
            description=form.cleaned_data.get('description'),
            contact=form.cleaned_data.get('contact'),
            picture=form.cleaned_data.get('picture'),
            tripadvisor_link=form.cleaned_data.get('tripadvisor_link'),
            )
        return super(VenueCreationFormView, self).form_valid(form)
    def get_success_url(self):
        return reverse('venuepage', kwargs={'pk': self.venue.pk})
    
    
class TeamCreationFormView(FormView):
    template_name = 'createteam.html'
    form_class = TeamCreationForm
    success_url = '/'
    def form_valid(self, form):
        self.team = Team.objects.create(
            name=form.cleaned_data.get('name'),
            moderator=form.cleaned_data.get('moderator'),
            )
        for player in form.cleaned_data['team_user']:
                self.team.team_user.add(player),
        return super(TeamCreationFormView, self).form_valid(form)
    def get_success_url(self):
        return reverse('teampage', kwargs={'pk': self.team.pk})


class JoinGameView(LoginRequiredMixin, View):
    def post(self, request, game_id):
        game = get_object_or_404(Game, id=game_id)

        if request.user in game.players.all():
            messages.warning(request, "You are already part of this game!")
        else:
            game.players.add(request.user)
            messages.success(request, "You have successfully joined the game")

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    
class LeaveGameView(LoginRequiredMixin, View):
    def post(self, request, game_id):
        game = get_object_or_404(Game, id=game_id)

        if request.user not in game.players.all():
            messages.warning(request, "You not a part of this game!")
        else:
            game.players.remove(request.user)
            messages.success(request, "You have successfully joined the game")

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    