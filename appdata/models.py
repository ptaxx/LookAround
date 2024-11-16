from django import forms
from django.db import models


class User(models.Model):
    username = models.CharField(max_length=32)
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    short_bio = models.TextField(max_length=200, blank=True)
    user_pic = models.ImageField(upload_to='userpics', null=True)

    def __str__(self):
        return self.username
        

class Team(models.Model):
    name = models.CharField(max_length=32)
    moderator = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

area_choices = ("Trysil")

class Area(models.Model):
    area_name = models.CharField(max_length=20, choices=area_choices, default="Trysil")

    def __str__(self):
        return self.area_name




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
    GAME_SIZE_CHOICES = (
        ('9', 9)
        ('16', 16)
    )
    game_size = forms.MultipleChoiceField(choices=GAME_SIZE_CHOICES)
    availability = models.BooleanField(default=True)
    area = models.ForeignKey(Area)
    players = models.ManyToManyField(User, Null=True, on_delete=models.SET_NULL)
    activities = models.ManyToManyField(Activity, on_delete=models.CASCADE)

    def __str__(self):
        return self.starting_time