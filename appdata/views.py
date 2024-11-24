from random import randint
from django.shortcuts import render, redirect
from django.views import View
from .forms import SignUpForm, GameCreationForm, ActivityCreationForm
from django.contrib import messages
from appdata.models import Activity, Game, Team, Area, CustomUser
from django.template import loader
from django.views.generic.edit import FormView


class GamePageView(View):
    def get(self, request, *args, **kwargs):
        game = Game.objects.get(id=kwargs.get('pk'))
        activities = game.activities.all()
        players = game.players.all()
        teams = Team.objects.filter(team_user__in=game.players.all()).distinct()  # search for teams, where at least 1 player is part of this game. So find all the teams that have players who are part of a specific game. And remove all dublicated teams.
        context = {"game": game, "activities": activities, "players": players, 'teams':teams}
        return render(request, "gamepage.html", context)
    
    
class ActivityView(View):
    def get(self, request, *args, **kwargs):
        activity = Activity.objects.get(id=kwargs.get('pk'))
        context = {"activity": activity}
        return render(request, "activitypage.html", context)
    

class GamesPageView(View):
    def get(self, request, *args, **kwargs):
        games = Game.objects.all()
        context = {"games": games}
        return render(request, "gamespage.html", context)
    

class IndexView(View):
    def get(self, request, *args, **kwargs):
        games = Game.objects.all()
        area = Area.objects.all()
        context = {"games": games, "area": area,}
        return render(request, "index.html", context)

      
def sign_up(request):
    if request.method == "POST":
        fm = SignUpForm(request.POST)
        if fm.is_valid():
            messages.success(request, 'Registration successful!')
            fm.save()
            return redirect("/")
    else:
        fm = SignUpForm()
    return render(request, 'registration/signup.html', {'form':fm})

class UserPageViews(View):
    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.get(id=kwargs.get('pk'))
        # Find all teams where at least one player is part of
        teams = Team.objects.filter(
            team_user__in=user.game_set.values_list('players', flat=True)
            ).distinct()
        # Find all games where user is the player
        games = Game.objects.filter(players=user).distinct()
        context = {"user": user, "teams": teams, "games": games}
        return render(request, "userpage.html", context)


def game_entry(request):
    if(request.method=="POST"):
        fm = GameCreationForm(request.POST)
        if fm.is_valid():
            fm.save()
            return redirect(f'/gamespage')
    else:
        fm = GameCreationForm()
    return render(request, 'creategame.html', {'form':fm})

def contactpage(request):
    return render(request, 'contactpage.html')


class ActivityCreationFormView(FormView):
    template_name = 'createactivity.html'
    form_class = ActivityCreationForm
    success_url = '/'
    def form_valid(self, form):
        Activity.objects.create(
            short_description=form.cleaned_data.get('short_description'),
            full_description=form.cleaned_data['full_description'],
            venue=form.cleaned_data['venue'],
            passcode=str(randint(10000,99999))
            )
        return super(ActivityCreationFormView, self).form_valid(form)
