from django import forms
from .models import CustomUser, Game
from django.contrib.auth.forms import UserCreationForm
from django.forms import DateTimeInput, ModelForm


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['isplayer', 'username', 'first_name', 'last_name', 'email', 'short_bio', 'userpic']
        labels = {'isplayer': 'Register as player', 'email': 'Email'}


class GameCreationForm(ModelForm):
    finishing_time = forms.DateTimeField(
        widget=forms.widgets.DateTimeInput(attrs={'type':'datetime-local'}),
    )
    class Meta:
        model = Game
        fields = [
            'area',
            'finishing_time',
            'players',
            'availability',
        ]
        labels ={
            'area': 'Area',
            'finishing_time': 'Finishing time (optional)',
            'players': 'Players',
            'avaialbility': 'Available to everyone',
        }
        widget = {'finishing_time': forms.TextInput(attrs={'type':'datetime-local'})}