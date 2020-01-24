# -*- coding: utf-8 -*-
import os
from datetime import datetime, timedelta

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

def path_image_upload(instance, filename):
    var = filename.split('.')
    var_length = len(var) - 1
    var_extension = var[var_length]

    try:
        image = "static/images/profiles/" + str(instance.user.id) + "_" + instance.user.username + "." + var_extension
        if(os.path.isfile(image)):
            os.remove(image)

    except Exception as e:
        print(str(e))


    return "static/images/profiles/" + str(instance.user.id) + "_" + instance.user.username + "." + var_extension

class Profile(models.Model):
    user = models.ForeignKey(User, related_name="user", blank=True, null=True)
    theme = models.ForeignKey(Theme, blank=True, null=True, on_delete=models.SET_NULL)
    colorGenres = models.BooleanField(default=True)
    celularDataSavings = models.BooleanField(default=True)
    width_image = models.IntegerField(default=0)
    height_image = models.IntegerField(default=0)
    followings = models.ManyToManyField(User, related_name="following", blank=True)
    avatar = models.ForeignKey(Avatar, blank=True, null=True, on_delete=models.SET_NULL)
    image = models.FileField(upload_to=path_image_upload, null=True, blank=True)

    def __str__(self):
        return str(self.user.first_name) + " " + str(self.user.last_name)

    def getMoviesSeen(self):
        return len(Movie.objects.filter(user=self.user, states__in=[1]).all())

    def getShowsSeen(self):
        return len(Show.objects.filter(user=self.user, states__in=[1]).all())

    def getEpisodesSeen(self):
        return len(Episode.objects.filter(user=self.user, states__in=[1]).all())

    def getLists(self):
        return List.objects.filter(user=self.user)

    def getFriends(self):
        friends = []
        for following in self.followings.all():
            friends.append(Profile.objects.get(user=following))
        return friends

    def getImage(self):
        image = "-"
        if self.image:
            image = self.image
        return image

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
        return str(self.id_movie) + " | " + str(self.title) + " (" + self.user.username + ") - States: " + str(self.states.all())

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

    def getUser(self):
        return self.user.username

    def getDescription(self):
        if (self.operation.id == 1):
            return "Ha añadido <b>" + self.movie.title + "</b> a su lista de pendientes"

        if (self.operation.id == 2):
            return "Ha visto <b>" + self.movie.title + "</b>"

        if (self.operation.id == 3):
            return "Ha añadido <b>" + self.show.name + "</b> a su lista de pendientes"

        if (self.operation.id == 4):
            return "Ha visto <b>" + self.show.name + "</b>"

        if (self.operation.id == 5):
            return "Ha visto el <b>E" + str(self.episode.episode_number) + "xT" + str(
                self.episode.season_number) + "</b> de <b>" + self.episode.show.name + "</b>"

        if (self.operation.id == 6):
            return "Ahora sigue a <b>" + self.follower.username + "</b>"

    def getPosterPath(self):
        if self.operation.id == 1 or self.operation_id == 2:
            return "https://image.tmdb.org/t/p/w200" + self.movie.poster_path

        if self.operation.id == 3 or self.operation.id == 4:
            return "https://image.tmdb.org/t/p/w200" + self.show.poster_path

        if self.operation.id == 5:
            return "https://image.tmdb.org/t/p/w200" + self.episode.show.poster_path

        if self.operation.id == 6:
            poster_path = ""
            if not Profile.objects.get(user=self.follower).avatar == None:
                poster_path = Profile.objects.get(user=self.follower).avatar.src
            return poster_path

    def getDate(self):
        return (self.date_add + timedelta(hours=1)).strftime("%d-%m-%Y %H:%M:%S")

    def getHref(self):
        if self.movie:
            return "/movie/" + str(self.movie.id_movie)
        elif self.show:
            return "/show/" + str(self.show.id_show)
        elif self.episode:
            return "/show/" + str(self.episode.show.id_show)

class List(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=10, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    movies = models.ManyToManyField(Movie, blank=True)
    shows = models.ManyToManyField(Show, blank=True)

    def __str__(self):
            return str(self.id) + " - " + str(self.user) + " | " + self.name

class Recommendation(models.Model):
    name = models.CharField(max_length=100)
    poster_path = models.CharField(max_length=50)
    id_media = models.IntegerField()
    from_user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="from_user")
    to_user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="to_user")
    types = (
        ('movie', 'Movie'),
        ('show', 'Show'),
    )
    type = models.CharField(choices=types, max_length=20)
    creation_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.from_user.user.username + " -> " + self.to_user.user.username + " | " + self.name
