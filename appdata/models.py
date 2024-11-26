from django.contrib.auth.models import AbstractUser
from django import forms
from django.db import models


class Area(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(null=True, blank=True)
    picture = models.ImageField(upload_to='images', null=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    short_bio = models.TextField(max_length=200, blank=True)
    isplayer = models.BooleanField(default=True)
    userpic = models.ImageField(default='default_userpic.png', upload_to='profile_pictures')
    current_area = models.ForeignKey(Area, null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.username
  
   
class Team(models.Model):
    name = models.CharField(max_length=32)
    moderator = models.ForeignKey(CustomUser, related_name='moderator', on_delete=models.CASCADE)
    team_user = models.ManyToManyField(CustomUser, related_name='member')

    def __str__(self):
        return self.name
    

class Venue(models.Model):
    name = models.CharField(max_length=32)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    opening_hour = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    closing_hour = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    description = models.TextField(max_length=200, blank=False)
    picture = models.ImageField(upload_to='venue_pictures', null=True)
    contact = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
    tripadvisor_link = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class Activity(models.Model):
    short_description = models.TextField(max_length=80)
    full_description = models.TextField()
    passcode = models.CharField(max_length=5)
    active = models.BooleanField(default=True)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)

    def __str__(self):
        return self.short_description


class Game(models.Model):
    starting_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    finishing_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    GAME_SIZE_CHOICES = [
        (9, 9),
        (16, 16),
    ]
    game_size = forms.MultipleChoiceField(choices=GAME_SIZE_CHOICES)
    availability = models.BooleanField(default=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    players = models.ManyToManyField(CustomUser)
    activities = models.ManyToManyField(Activity)

    def __str__(self):
        return f'{self.starting_time.strftime("%Y-%m-%d %H:%M:%S")}, {self.area}'

