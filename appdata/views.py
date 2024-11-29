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
from .utils import get_weather_data


class GamePageView(View):
    def get(self, request, *args, **kwargs):
        game = Game.objects.get(id=kwargs.get('pk'))
        activities = game.activities.all()
        players = game.players.all()
        teams = Team.objects.filter(team_user__in=game.players.all()).distinct()
        area_id = game.area.weather_id
        weather_data = get_weather_data(area_id)
        context = {
            'game': game, 
            'activities': activities, 
            'players': players, 
            'teams':teams,
            'weather_data': weather_data,
            }
        return render(request, 'gamepage.html', context)
    
class AreaPageView(View):
    def get(self, request, *args, **kwargs):
        area = Area.objects.get(id=kwargs.get('pk'))
        venues = Venue.objects.filter(area=area)
        area_id = area.weather_id
        weather_data = get_weather_data(area_id)
        context = {
            'area': area, 
            'weather_data': weather_data,
            'venues': venues
            }
        return render(request, 'areapage.html', context)
    

class VenuePageView(View):
    def get(self, request, *args, **kwargs):
        venue = Venue.objects.get(id=kwargs.get('pk'))
        context = {'venue': venue}
        return render(request, 'venuepage.html', context)
    
    
class ActivityView(View):
    def get(self, request, *args, **kwargs):
        activity = Activity.objects.get(id=kwargs.get('pk'))
        form = PasscodeForm()
        activitycheck = ActivityCheck.objects.filter(
            activity=activity,
            user = request.user
            )
        for entry in activitycheck:
            if entry.is_active:
                user_has_activity = True
            else:
                user_has_activity = False
        context = {
            'activity': activity, 
            'form': form,
            'activitycheck': activitycheck,
            'user_has_activity': user_has_activity,
            }
        return render(request, 'activitypage.html', context)
    def post(self, request, *args, **kwargs):
        activity = Activity.objects.get(id=kwargs.get('pk'))
        activitycheck = ActivityCheck.objects.filter(
            activity=activity,
            user = request.user
            )
        for entry in activitycheck:
            if entry.is_active:
                user_has_activity = True
            else:
                user_has_activity = False
        form = PasscodeForm(request.POST)
        if form.is_valid():
            passcode = form.cleaned_data['passcode']
            if passcode == activity.passcode:
                messages.success(request, 'The passcode is correct! Task complete!')
                activity_checks = ActivityCheck.objects.filter(
                    activity=activity, 
                    user=request.user
                    )
                for entry in activity_checks:
                    entry.is_active = False
                    entry.save()
                games = Game.objects.filter(activities=activity)
                for game in games:
                    scoreboards = ScoreBoard.objects.filter(
                        game=game,
                        user=request.user
                    )
                    for scoreboard in scoreboards:
                        if scoreboard.points < 9:
                            scoreboard.points += 1
                            scoreboard.save()
                            if scoreboard.points == 9:
                                scoreboards = ScoreBoard.objects.filter(game=game)
                                positions = [entry.position for entry in scoreboards]
                                if '3rd place' in positions:
                                    scoreboard.position = 'Finished'
                                    scoreboard.save()
                                elif '2nd place' in positions:
                                    scoreboard.position = '3rd place'
                                    scoreboard.save()
                                elif '1st place' in positions:
                                    scoreboard.position = '2nd place'
                                    scoreboard.save()
                                else:
                                    scoreboard.position = '1st place'
                                    scoreboard.save()
            else:
                messages.error(request, 'Incorrect passcode. Please try again.')
        context = {
            'activity': activity, 
            'form': form,
            'activitycheck': activitycheck,
            'user_has_activity': user_has_activity,
            }
        return render(request, 'activitypage.html', context)
    

class AreasPageView(View):
    def get(self, request, *args, **kwargs):
        areas = Area.objects.all()
        context = {'areas': areas}
        return render(request, 'areaspage.html', context)


class TeamsPageView(View):
    def get(self, request, *args, **kwargs):
        teams = Team.objects.all()
        context = {'teams': teams}
        return render(request, 'teamspage.html', context)

class GamesPageView(View):
    def get(self, request, *args, **kwargs):
        games = Game.objects.all()
        context = {'games': games}
        return render(request, 'gamespage.html', context)
    

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
        context = {'games': games, 'area': area, 'weather_data': weather_data}
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
        games = Game.objects.filter(teams=team)
        teamplayers = team.team_user.all()
        context = {'team': team, 
                   'teamplayers': teamplayers,
                   'games': games,
                   }
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
            self.game.players.add(player)
        for team in form.cleaned_data['teams']:
                self.game.teams.add(team)
        
        venues = Venue.objects.filter(area=form.cleaned_data.get('area'))
        if len(venues) < 9:
            for x in venues:
                activities = Activity.objects.filter(venue=x)
                if activities.exists():
                    activity = choice(activities)
                    self.game.activities.add(activity)
        if len(venues) >= 9:
            venues = list(venues)
            selected_venues = sample(venues, 9)
            for x in selected_venues:
                activities = Activity.objects.filter(venue=x)
                if activities.exists():
                    activity = choice(activities)
                    self.game.activities.add(activity)
                    
        activities = self.game.activities.all()
        players = set(self.game.players.all())
        teams = self.game.teams.all()
        for team in teams:
            for user in team.team_user.all():
                players.add(user)
            players.add(team.moderator)
        for activity in activities:
            for player in players:
                ActivityCheck.objects.create(
                    game=self.game,
                    user=player,
                    activity=activity,
                )
        for player in players:
            ScoreBoard.objects.create(
                game=self.game,
                user=player,
            )  
                           
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
       

    