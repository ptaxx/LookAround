from django import forms
from .models import CustomUser, Game, Activity
from django.contrib.auth.forms import UserCreationForm
from django.forms import DateTimeInput, ModelForm, TypedMultipleChoiceField


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
            'finishing_time',
            'players',
        ]
        labels ={
            'area': 'Area',
            'finishing_time': 'Finishing time (optional)',
            'players': 'Players',
            'availability': 'Available to everyone',
        }
        widgets = {
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
            'short_description': "Short Description (80 symbols max)",
            'full_description': 'Full description',
            'venue': 'Venue',
        }