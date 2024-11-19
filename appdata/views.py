from django.shortcuts import render
from django.views import View

from appdata.models import Activity, Game, Team


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
        activitie = Activity.objects.get(id=kwargs.get('pk'))
        context = {"activitie": activitie}
        return render(request, "activitypage.html", context)
    

class GamesPageView(View):
    def get(self, request, *args, **kwargs):
        games = Game.objects.all()
        context = {"games": games}
        return render(request, "gamespage.html", context)