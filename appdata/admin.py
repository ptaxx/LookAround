from django.contrib import admin
from .models import CustomUser, Team, Area, Venue, Activity, Game, ScoreBoard, ActivityCheck


admin.site.register(CustomUser)

admin.site.register(Team)

admin.site.register(Area)

admin.site.register(Venue)

admin.site.register(Activity)

admin.site.register(Game)

admin.site.register(ActivityCheck)

admin.site.register(ScoreBoard)



