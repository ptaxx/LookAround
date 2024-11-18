from django.shortcuts import render
from django.views import View

from appdata.models import Activity


class GamePageView(View):
    def get(self, request, *args, **kwargs):
        activities = Activity.objects.all()
        context = {"activities": activities}
        return render(request, "game_page.html", context)
    
    
class ActivityView(View):
    def get(self, request, *args, **kwargs):
        activitie = Activity.objects.get(id=kwargs.get('pk'))
        context = {"activitie": activitie}
        return render(request, "activity_page.html", context)
    