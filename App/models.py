# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

class Theme(models.Model):
    name = models.CharField(max_length=30)
    cssFile = models.CharField(max_length=40)

    bg_color = models.CharField(max_length=10)
    accent_color = models.CharField(max_length=10)

    def __str__(self):
        return str(self.name) + " (" + str(self.cssFile) + ".css)"


class Profile(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    theme = models.ForeignKey(Theme, blank=True, null=True)
    colorGenres = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user.first_name) + " " + str(self.user.last_name)


class Movie(models.Model):
    id_movie = models.IntegerField()
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poster_path = models.CharField(max_length=50)
    date_add = models.DateTimeField(auto_now=False, auto_now_add=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title) + " (" + self.user.username +  ") - Vista: " + str(self.seen)