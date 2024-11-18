from django.shortcuts import render
from django.views import View

from appdata.models import Activity

class GamePageView(View):
    def get(self, request, *args, **kwargs):
        activities = Activity.objects.all()
        context = {"activities": activities}
        return render(request, "game_page.html", context)