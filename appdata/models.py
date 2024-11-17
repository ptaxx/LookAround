from getpass import fallback_getpass

from django.contrib.auth.models import User
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
    team_user = models.ManyToManyField(User, related_name='member')

    def __str__(self):
        return self.name
    

class Area(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Venue(models.Model):
    name = models.CharField(max_length=32)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    opening_hour = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    closing_hour = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    description = models.TextField(max_length=200, blank=False)
    tripadvisor_link = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class Activity(models.Model):
    short_description = models.TextField()
    full_description = models.TextField()
    passcode = models.CharField(max_length=5)
    active = models.BooleanField(default=True)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)

    def __str__(self):
        return self.short_description


class Game(models.Model):
    starting_time = models.TimeField(auto_now_add=True)
    finishing_time = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    GAME_SIZE_CHOICES = [
        (9, 9),
        (16, 16),
    ]
    game_size = forms.MultipleChoiceField(choices=GAME_SIZE_CHOICES)
    availability = models.BooleanField(default=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    players = models.ManyToManyField(User)
    activities = models.ManyToManyField(Activity)

    def __str__(self):
        return self.starting_time

