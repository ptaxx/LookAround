from .models import CustomUser, Game
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm


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