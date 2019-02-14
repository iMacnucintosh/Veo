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

class Avatar(models.Model):
    name = models.CharField(max_length=100)
    src = models.CharField(max_length=500)

    def __str__(self):
        return str(self.name) + " (" + str(self.src) + ")"

class Profile(models.Model):
    user = models.ForeignKey(User, related_name="user", blank=True, null=True)
    theme = models.ForeignKey(Theme, blank=True, null=True, on_delete=models.SET_NULL)
    colorGenres = models.BooleanField(default=True)
    width_image = models.IntegerField(default=0)
    height_image = models.IntegerField(default=0)
    followings = models.ManyToManyField(User, related_name="following", blank=True)
    avatar = models.ForeignKey(Avatar, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.user.first_name) + " " + str(self.user.last_name)

    def getMoviesSeen(self):
        return len(Movie.objects.filter(user=self.user, states__in=[1]).all())

    def getShowsSeen(self):
        return len(Show.objects.filter(user=self.user, states__in=[1]).all())

    def getEpisodesSeen(self):
        return len(Episode.objects.filter(user=self.user, states__in=[1]).all())

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
    vote_average = models.FloatField(default=0)
    states = models.ManyToManyField(State, blank=True)

    def __str__(self):
        return str(self.title) + " (" + self.user.username + ") - States: " + str(self.states.all())

class Show(models.Model):
    id_show = models.IntegerField()
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poster_path = models.CharField(max_length=50)
    date_update = models.DateTimeField(default=datetime.now)
    vote_average = models.FloatField(default=0)
    states = models.ManyToManyField(State, blank=True)

    def __str__(self):
        return str(self.name) + " (" + self.user.username + ") - States: " + str(self.states.all())

    def getEpisodes(self):
        return Episode.objects.filter(show=self.id).all()

    def getEpisodesSeen(self):
        return Episode.objects.filter(show=self.id, states__in=[1]).all()

class Episode(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    id_episode = models.IntegerField()
    season_number = models.IntegerField()
    episode_number = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    states = models.ManyToManyField(State, blank=True)

    def __str__(self):
        return str(self.show.name) + " - S" + str(self.season_number) + "E" + str(self.episode_number) + " - States: " + str(self.states.all())

class Operation(models.Model):
    operation_belongs_to_types = (
        ('movie', 'Movie'),
        ('show', 'Show'),
        ('episode', 'Episode'),
        ('follower', 'Follower'),
    )
    operation_belongs_to = models.CharField(choices=operation_belongs_to_types, max_length=30)

    type = models.ForeignKey(State, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.id) + " | " + str(self.operation_belongs_to) + " - " + str(self.type)

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_activity")
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE)

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True)
    show = models.ForeignKey(Show, on_delete=models.CASCADE, null=True, blank=True)
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, null=True, blank=True)
    follower = models.ForeignKey(User, related_name="new_follower", on_delete=models.CASCADE, null=True, blank=True)

    date_add = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        if not self.movie==None:
            return str(self.user.username) + " - " + str(self.operation.type.name) + " | " + str(self.movie.title)

        if not self.show==None:
            return str(self.user.username) + " - " + str(self.operation.type.name) + " | " + str(self.show.name)

        if not self.episode==None:
            return str(self.user.username) + " - " + str(self.operation.type.name) + " | " + str(self.episode.show.name) + " S" + str(self.episode.season_number) + "E" + str(self.episode.episode_number)

        if not self.follower==None:
            return str(self.user.username) + " | Follow | " + str(self.follower.username)