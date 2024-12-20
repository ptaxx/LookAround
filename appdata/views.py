from datetime import datetime
from random import randint, choice, sample
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from .forms import (
    SignUpForm,
    GameCreationForm,
    ActivityCreationForm,
    VenueCreationForm,
    TeamCreationForm,
    PasscodeForm,
)
from django.contrib import messages
from appdata.models import (
    Activity,
    Game,
    Team,
    Area,
    CustomUser,
    Venue,
    ActivityCheck,
    ScoreBoard,
)
from django.template import loader
from django.views.generic.edit import FormView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import (
    get_weather_data, 
    countdown_timer, 
    user_activity_check, 
    get_location, 
    compare_location,
)
from django.utils import timezone


class GamePageView(View):
    def get(self, request, *args, **kwargs):
        game = Game.objects.get(id=kwargs.get("pk"))
        activities = game.activities.all()
        players = game.players.all()
        scoreboards = ScoreBoard.objects.filter(game=game).order_by("-points")
        teams = Team.objects.filter(team_user__in=game.players.all()).distinct()
        area_id = game.area.weather_id
        weather_data = get_weather_data(area_id)
        time_data = countdown_timer(game.starting_time)
        activity_checks = []
        user = request.user
        if user in players:
            activity_checks = ActivityCheck.objects.filter(
                game=game,
                user=user,
            )
        else:
            activity_checks = [None] * 9
        combined = zip(activities, activity_checks)
        context = {
            "game": game,
            "activities": activities,
            "players": players,
            "teams": teams,
            "weather_data": weather_data,
            "scoreboards": scoreboards,
            "time_data": time_data,
            "activity_checks": activity_checks,
            "combined": combined
        }
        return render(request, "gamepage.html", context)


class AreaPageView(View):
    def get(self, request, *args, **kwargs):
        area = Area.objects.get(id=kwargs.get("pk"))
        venues = Venue.objects.filter(area=area)
        area_id = area.weather_id
        weather_data = get_weather_data(area_id)
        context = {"area": area, "weather_data": weather_data, "venues": venues}
        return render(request, "areapage.html", context)

    def post(self, request, *args, **kwargs):
        area = Area.objects.get(id=kwargs.get("pk"))
        venues = Venue.objects.filter(area=area)
        area_id = area.weather_id
        weather_data = get_weather_data(area_id)
        context = {"area": area, "weather_data": weather_data, "venues": venues}
        if "set_area" in request.POST:
            area = Area.objects.get(id=kwargs.get("pk"))
            profile = request.user
            profile.current_area = area
            profile.save()
            return render(request, "areapage.html", context)


class VenuePageView(View):
    def get(self, request, *args, **kwargs):
        venue = Venue.objects.get(id=kwargs.get("pk"))
        context = {"venue": venue}
        return render(request, "venuepage.html", context)


class ActivityView(View):
    def get(self, request, *args, **kwargs):
        activity = Activity.objects.get(id=kwargs.get("pk"))
        form = PasscodeForm()
        user = request.user
        user_has_activity = user_activity_check(user, activity)
        context = {
            "activity": activity,
            "form": form,
            "user_has_activity": user_has_activity,
        }
        return render(request, "activitypage.html", context)

    def post(self, request, *args, **kwargs):
        activity = Activity.objects.get(id=kwargs.get("pk"))
        user = request.user
        user_has_activity = user_activity_check(user, activity)
        form = PasscodeForm(request.POST)
        if form.is_valid():
            passcode = form.cleaned_data["passcode"]
            if passcode == activity.passcode:
                self.update_scoreboard(request)
                return redirect(request.path)
            else:
                messages.error(request, "Incorrect passcode. Please try again.")
        if "compare_locations" in request.POST:
            latitude = activity.latitude
            longitude = activity.longitude
            if compare_location(latitude, longitude):
                if user_has_activity:
                    self.update_scoreboard(request)
                    return redirect(request.path)
            else:
                messages.error(request, "You are not at the location. Please try again.")
        context = {
            "activity": activity,
            "form": form,
            "user_has_activity": user_has_activity,
        }
        return render(request, "activitypage.html", context)
    
    def update_scoreboard(self, request, *args, **kwargs):
        activity_id = self.kwargs.get("pk")
        activity = Activity.objects.get(id=activity_id)
        user = request.user
        messages.success(request, "Task complete!")
        activity_checks = ActivityCheck.objects.filter(
            activity=activity, user=request.user
        )
        for entry in activity_checks:
            entry.is_active = False
            entry.save()
            games = Game.objects.filter(activities=activity)
        for game in games:
            scoreboards = ScoreBoard.objects.filter(
                game=game, user=request.user
        )
            for scoreboard in scoreboards:
                if scoreboard.points < 9:
                    scoreboard.points += 1
                    scoreboard.save()
                    if scoreboard.points == 9:
                        scoreboards = ScoreBoard.objects.filter(game=game)
                        positions = [entry.position for entry in scoreboards]
                        if "3rd place" in positions:
                            scoreboard.position = "Finished"
                            scoreboard.save()
                        elif "2nd place" in positions:
                            scoreboard.position = "3rd place"
                            scoreboard.save()
                        elif "1st place" in positions:
                            scoreboard.position = "2nd place"
                            scoreboard.save()
                        else:
                            scoreboard.position = "1st place"
                            scoreboard.save()
                
            

class AreasPageView(View):
    def get(self, request, *args, **kwargs):
        areas = Area.objects.all()
        context = {"areas": areas}
        return render(request, "areaspage.html", context)


class TeamsPageView(View):
    def get(self, request, *args, **kwargs):
        teams = Team.objects.all()
        context = {"teams": teams}
        return render(request, "teamspage.html", context)


class GamesPageView(View):
    def get(self, request, *args, **kwargs):
        games = Game.objects.all()
        context = {"games": games}
        return render(request, "gamespage.html", context)


class IndexView(View):
    def get(self, request, *args, **kwargs):
        games = Game.objects.all()
        area = Area.objects.all()
        user = request.user
        if user.is_authenticated and user.current_area:
            area_id = user.current_area.weather_id
        else:
            area_id = Area.objects.first().weather_id
        weather_data = get_weather_data(area_id)
        context = {"games": games, "area": area, "weather_data": weather_data}
        return render(request, "index.html", context)


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        messages.success(self.request, "Registration was successful!")
        response = super().form_valid(form)
        return response


class UserPageViews(View):
    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.get(id=kwargs.get("pk"))
        teams = Team.objects.filter(
            team_user__in=user.game_set.values_list("players", flat=True)
        ).distinct()
        games = Game.objects.filter(players=user).distinct()
        context = {"user": user, "teams": teams, "games": games}
        return render(request, "userpage.html", context)


class TeamPageViews(View):
    def get(self, request, *args, **kwargs):
        team = Team.objects.get(id=kwargs.get("pk"))
        games = Game.objects.filter(teams=team)
        teamplayers = team.team_user.all()
        context = {
            "team": team,
            "teamplayers": teamplayers,
            "games": games,
        }
        return render(request, "teampage.html", context)


class GameEntryView(FormView):
    form_class = GameCreationForm
    template_name = "creategame.html"
    success_url = "/"

    def form_valid(self, form):
        game = Game.objects.create(
            area=form.cleaned_data.get("area"),
            starting_time=form.cleaned_data.get("starting_time"),
            availability=form.cleaned_data.get("availability"),
        )
        venues = Venue.objects.filter(area=form.cleaned_data.get("area"))
        if len(venues) < 9:
            for x in venues:
                activities = Activity.objects.filter(venue=x)
                if activities.exists():
                    activity = choice(activities)
                    game.activities.add(activity)
        if len(venues) >= 9:
            venues = list(venues)
            selected_venues = sample(venues, 9)
            for x in selected_venues:
                activities = Activity.objects.filter(venue=x)
                if activities.exists():
                    activity = choice(activities)
                    game.activities.add(activity)

        activities = game.activities.all()
        self.game = game

        return super(GameEntryView, self).form_valid(form)

    def get_success_url(self):
        return reverse("gamepage", kwargs={"pk": self.game.pk})


class ContactPage(View):
    def get(self, request):
        return render(request, "contactpage.html")


class ActivityCreationFormView(FormView):
    template_name = "createactivity.html"
    form_class = ActivityCreationForm
    success_url = "/"

    def form_valid(self, form):
        your_location = get_location()
        lat = your_location.get("lat")
        lon = your_location.get("lon")
        self.activity = Activity.objects.create(
            short_description=form.cleaned_data.get("short_description"),
            full_description=form.cleaned_data.get("full_description"),
            venue=form.cleaned_data.get("venue"),
            passcode=str(randint(10000, 99999)),
            latitude=lat,
            longitude=lon,
        )
        return super(ActivityCreationFormView, self).form_valid(form)

    def get_success_url(self):
        return reverse("activitypage", kwargs={"pk": self.activity.pk})


class VenueCreationFormView(FormView):
    template_name = "createvenue.html"
    form_class = VenueCreationForm
    success_url = "/"

    def form_valid(self, form):
        self.venue = Venue.objects.create(
            name=form.cleaned_data.get("name"),
            area=form.cleaned_data.get("area"),
            opening_hour=form.cleaned_data.get("opening_hour"),
            closing_hour=form.cleaned_data.get("closing_hour"),
            description=form.cleaned_data.get("description"),
            contact=form.cleaned_data.get("contact"),
            picture=form.cleaned_data.get("picture"),
            tripadvisor_link=form.cleaned_data.get("tripadvisor_link"),
        )
        return super(VenueCreationFormView, self).form_valid(form)

    def get_success_url(self):
        return reverse("venuepage", kwargs={"pk": self.venue.pk})


class TeamCreationFormView(FormView):
    template_name = "createteam.html"
    form_class = TeamCreationForm
    success_url = "/"

    def form_valid(self, form):
        self.team = Team.objects.create(
            name=form.cleaned_data.get("name"),
            moderator=form.cleaned_data.get("moderator"),
        )
        for player in form.cleaned_data["team_user"]:
            self.team.team_user.add(player),
        return super(TeamCreationFormView, self).form_valid(form)

    def get_success_url(self):
        return reverse("teampage", kwargs={"pk": self.team.pk})


class JoinGameView(LoginRequiredMixin, View):
    def post(self, request, game_id):
        game = get_object_or_404(Game, id=game_id)

        if request.user in game.players.all():
            messages.warning(request, "You are already part of this game!")
        else:
            game.players.add(request.user)
            ScoreBoard.objects.create(
                game=game,
                user=request.user,
            )
            activities = game.activities.all()
            for activity in activities:
                ActivityCheck.objects.create(
                    game=game, activity=activity, user=request.user
                )
            messages.success(request, "You have successfully joined the game")

        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


class LeaveGameView(LoginRequiredMixin, View):
    def post(self, request, game_id):
        game = get_object_or_404(Game, id=game_id)

        if request.user not in game.players.all():
            messages.warning(request, "You not a part of this game!")
        else:
            game.players.remove(request.user)
            ScoreBoard.objects.filter(
                game=game,
                user=request.user,
            ).delete()
            ActivityCheck.objects.filter(
                game=game,
                user=request.user,
            ).delete()
            messages.success(request, "You have successfully joined the game")

        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
