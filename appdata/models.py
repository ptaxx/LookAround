from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django import forms
from django.db import models


class Area(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(null=True, blank=True)
    picture = models.ImageField(upload_to='static/area_pictures', null=True, blank=True)
    weather_id = models.CharField(max_length=10, default='588409')

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    short_bio = models.TextField(max_length=200, blank=True)
    isplayer = models.BooleanField(default=True)
    userpic = models.ImageField(
        default='static/images/default_userpic.png', 
        upload_to='static/profile_pictures',
        null=True, 
        blank=True
        )
    current_area = models.ForeignKey(Area, null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.username
  
   
class Team(models.Model):
    name = models.CharField(max_length=32)
    moderator = models.ForeignKey(CustomUser, related_name='moderator', on_delete=models.CASCADE)
    team_user = models.ManyToManyField(CustomUser, related_name='member', blank=True)

    def __str__(self):
        return self.name
    

class Venue(models.Model):
    name = models.CharField(max_length=32)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    opening_hour = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    closing_hour = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    description = models.TextField(max_length=200, blank=False)
    picture = models.ImageField(upload_to='static/venue_pictures', null=True, blank=True)
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
    starting_time = models.DateTimeField(auto_now=False, auto_now_add=False, default=datetime.now)
    finishing_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    availability = models.BooleanField(default=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    players = models.ManyToManyField(CustomUser)
    teams = models.ManyToManyField(Team)
    activities = models.ManyToManyField(Activity)

    def __str__(self):
        return f'{self.area}. {self.starting_time.strftime("%Y-%m-%d %H:%M")}'
    
    
class ActivityCheck(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f'{self.game}. {self.user}. {self.activity}'


class ScoreBoard(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    position = models.CharField(null=True, blank=True, max_length=32)

    def __str__(self):
        return f'{self.game}. {self.user}. {self.points}, {self.position}'