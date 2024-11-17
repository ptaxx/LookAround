from getpass import fallback_getpass

from django import forms
from django.db import models


class User(models.Model):
    username = models.CharField(max_length=32)
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    short_bio = models.TextField(max_length=200, blank=True)
    
    def __str__(self):
        return self.username
    

class BusinessClient(models.Model):
    username = models.CharField(max_length=32)
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.username
        

class Team(models.Model):
    name = models.CharField(max_length=32)
    moderator = models.ForeignKey(User, related_name='moderator', on_delete=models.CASCADE)
    member = models.ManyToManyField(User, related_name='member')

    def __str__(self):
        return self.name
    

class TeamUser(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)




class Area(models.Model):
    area_name = models.CharField(max_length=32)

    def __str__(self):
        return self.area_name


class Venue(models.Model):
    venue_name = models.CharField(max_length=32)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    venue_opening_hour = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    venue_closing_hour = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    description_of_the_venue = models.TextField(max_length=200, blank=False)
    venue_link_tripadvisor = models.URLField(max_length=200, blank=False)

    def __str__(self):
        return self.venue_name


class Activity(models.Model):
    short_description = models.TextField(max_length=140)
    full_description = models.TextField(max_length=1000)
    passcode = models.CharField(max_length=5)
    active = models.BooleanField(default=True)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)

    def __str__(self):
        return self.short_description


class Game(models.Model):
    starting_time = models.TimeField(auto_now=False, auto_now_add=False)
    finishing_time = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    GAME_SIZE_CHOICES = [
        ('9', 9),
        ('16', 16),
    ]
    game_size = forms.MultipleChoiceField(choices=GAME_SIZE_CHOICES)
    availability = models.BooleanField(default=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    players = models.ManyToManyField(User)
    activities = models.ManyToManyField(Activity)

    def __str__(self):
        return self.starting_time
    

class GameActivity(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)


class GameUser(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
