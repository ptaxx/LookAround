from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from appdata.views import (
    ActivityView,
    AreaPageView,
    AreasPageView,
    GamePageView,
    GamesPageView,
    IndexView,
    JoinGameView,
    TeamPageViews,
    UserPageViews,
    SignUpView,
    GameEntryView,
    ContactPage,
    ActivityCreationFormView,
    VenuePageView,
    VenueCreationFormView,
    TeamCreationFormView,
    TeamsPageView,
    LeaveGameView,
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("areapage/<int:pk>/", AreaPageView.as_view(), name="areapage"),
    path("venuepage/<int:pk>/", VenuePageView.as_view(), name="venuepage"),
    path("gamespage/", GamesPageView.as_view(), name="gamespage"),
    path("areaspage/", AreasPageView.as_view(), name="areaspage"),
    path("gamepage/<int:pk>/", GamePageView.as_view(), name="gamepage"),
    path("activitypage/<int:pk>/", ActivityView.as_view(), name="activitypage"),
    path(
        "login/",
        LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("userpage/<int:pk>/", UserPageViews.as_view(), name="userpage"),
    path("teampage/<int:pk>/", TeamPageViews.as_view(), name="teampage"),
    path("createactivity/", ActivityCreationFormView.as_view(), name="createactivity"),
    path("creategame/", GameEntryView.as_view(), name="creategame"),
    path("contactpage/", ContactPage.as_view(), name="contact"),
    path("createvenue/", VenueCreationFormView.as_view(), name="createvenue"),
    path("createteam/", TeamCreationFormView.as_view(), name="createteam"),
    path("join/<int:game_id>/", JoinGameView.as_view(), name="join_game"),
    path("teamspage/", TeamsPageView.as_view(), name="teamspage"),
    path("leave/<int:game_id>/", LeaveGameView.as_view(), name="leave_game"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
