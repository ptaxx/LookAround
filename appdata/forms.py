from django import forms
from .models import CustomUser, Game, Activity, Venue, Team
from django.contrib.auth.forms import UserCreationForm
from django.forms import DateTimeInput, ModelForm


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['isplayer', 'username', 'first_name', 'last_name', 'email', 'short_bio', 'userpic']
        labels = {'isplayer': 'Register as player', 'email': 'Email'}


class GameCreationForm(ModelForm):
    class Meta:
        model = Game
        fields = [
            'area',
            'availability',
            'starting_time',
            'finishing_time',
            'players',
            'teams',
        ]
        labels ={
            'area': 'Area',
            'starting_time': 'Starting time',
            'finishing_time': 'Finishing time (optional)',
            'players': 'Players',
            'availability': 'Available to everyone',
            'teams': 'Add team',
        }
        widgets = {
            'starting_time': forms.widgets.DateTimeInput(attrs={'type':'datetime-local'}),
            'finishing_time': forms.widgets.DateTimeInput(attrs={'type':'datetime-local'}),
            }
     

class ActivityCreationForm(ModelForm):
    class Meta:
        model = Activity
        fields = [
            'short_description',
            'full_description',
            'venue',
        ]
        labels = {
            'short_description': 'Short Description (80 symbols max)',
            'full_description': 'Full description',
            'venue': 'Venue',
        }
        
        
class VenueCreationForm(ModelForm):
    class Meta:
        model = Venue
        fields = [
            'name',
            'area',
            'opening_hour',
            'closing_hour',
            'description',
            'contact',
            'picture',
            'tripadvisor_link',
        ]
        labels = {
            'name': 'Name of the venue',
            'area': 'Area',
            'opening_hour': 'Opening hour',
            'closing_hour': 'Closing hour',
            'description': 'Description of the Venue',
            'contact': 'Contact user',
            'picture': 'Picture of the Venue',
            'tripadvisor_link': 'TripAdvisor link'
        }
        widgets = {
            'opening_hour': forms.widgets.TimeInput(attrs={'type':'time'}),
            'closing_hour': forms.widgets.TimeInput(attrs={'type':'time'}),
            }
        enctype="multipart/form-data"
        
        
class TeamCreationForm(ModelForm):
    class Meta:
        model = Team
        fields = [
            'name',
            'moderator',
            'team_user',
        ]
        labels = {
            'name': 'Team name',
            'moderator': 'Team moderator',
            'team_user': 'Team members',
        }
        
        
class PasscodeForm(forms.Form):
    passcode = forms.CharField(
        label="Passcode", 
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )