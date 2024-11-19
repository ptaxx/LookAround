from django.shortcuts import render
from django.views import View

from appdata.models import Activity, Game


class GamePageView(View):
    def get(self, request, *args, **kwargs):
        game = Game.objects.get(id=kwargs.get('pk'))
        activities = game.activities.all()
        players = game.players.all()
        context = {"game": game, "activities": activities, "players": players}
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