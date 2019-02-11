# -*- coding: utf-8 -*-
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

class Theme(models.Model):
    name = models.CharField(max_length=30)
    cssFile = models.CharField(max_length=40)

    bg_color = models.CharField(max_length=10)
    accent_color = models.CharField(max_length=10)

    def __str__(self):
        return str(self.name) + " (" + str(self.cssFile) + ".css)"

def path_image_upload(instance, filename):
    var = filename.split('.')
    var_length = len(var) - 1
    var_extension = var[var_length]
    return "static/images/profiles/" + instance.user.id + "." + var_extension

class Profile(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    theme = models.ForeignKey(Theme, blank=True, null=True)
    colorGenres = models.BooleanField(default=True)
    width_image = models.IntegerField(default=0)
    height_image = models.IntegerField(default=0)
    image = models.ImageField(upload_to=path_image_upload,
                              null=True, blank=True,
                              width_field="width_image",
                              height_field="height_image")

    def __str__(self):
        return str(self.user.first_name) + " " + str(self.user.last_name)

class State(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return str(self.id) + " - " + str(self.name)

class Movie(models.Model):
    id_movie = models.IntegerField()
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poster_path = models.CharField(max_length=50)
    date_add = models.DateTimeField(auto_now=False, auto_now_add=True)
    states = models.ManyToManyField(State, blank=True)

    def __str__(self):
        return str(self.title) + " (" + self.user.username + ") - States: " + str(self.states.all())

class Show(models.Model):
    id_show = models.IntegerField()
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poster_path = models.CharField(max_length=50)
    date_update = models.DateTimeField(default=datetime.now)
    states = models.ManyToManyField(State, blank=True)

    def __str__(self):
        return str(self.name) + " (" + self.user.username + ") - States: " + str(self.states.all())

    def getEpisodes(self):
        return Episode.objects.filter(show=self.id).all()

class Episode(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    id_episode = models.IntegerField()
    season_number = models.IntegerField()
    episode_number = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    states = models.ManyToManyField(State, blank=True)

    def __str__(self):
        return str(self.show.name) + " - S" + str(self.season_number) + "E" + str(self.episode_number) + " - States: " + str(self.states.all())