# -*- coding: utf-8 -*-
import ast
import json
import os
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from App.models import *
from App.forms import *
from django.utils import timezone
from datetime import timedelta
from pywebpush import webpush
from App.download_manager import DownloadsManager

# --------------------------------------- GENERAL FUNCTIONS ------------------------------------------------------------


def createAvatars():
    try:
        for avatar_file in os.listdir("static/images/avatars"):
            if len(Avatar.objects.filter(src="/static/images/avatars/" + avatar_file)) == 0:
                Avatar.objects.create(name=avatar_file.split(
                    ".")[0], src="/static/images/avatars/" + avatar_file)
    except:
        print("No se encuentra la ruta static/images/avatars")

# ---------------------------------------------- APP -------------------------------------------------------------------


def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        context = {}
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"], password=form.cleaned_data["password"])

            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/")
            else:
                context["message"] = "Usuario o contraseña incorrectos"
                context["form"] = form
                return render(request, "app/login.html", context=context)
    else:
        form = LoginForm()

    return render(request, "app/login.html", {'form': form})


def log_out(request):
    logout(request)
    return HttpResponseRedirect("/login")


def sign_in(request):
    form = SignInForm(request.POST or None)
    context = {}

    if form.is_valid():
        if (form.cleaned_data["first_name"] != "" and form.cleaned_data["last_name"] != "" and form.cleaned_data["email_address"] != "" and form.cleaned_data["username"] != "" and form.cleaned_data["password"] != "" and form.cleaned_data["repassword"] != ""):
            if (form.cleaned_data["password"] != form.cleaned_data["repassword"]):
                context["form"] = form
                context["code_error"] = 1
                context["message"] = "Las contraseñas no coinciden"
                return render(request, "app/signin.html", context=context)
            else:
                try:
                    user = User.objects.create_user(username=form.cleaned_data["username"],
                                                    first_name=form.cleaned_data["first_name"],
                                                    last_name=form.cleaned_data["last_name"],
                                                    email=form.cleaned_data["email_address"],
                                                    password=form.cleaned_data["password"], is_staff=True)
                    user.save()

                    profile = Profile.objects.create(user=user, theme=Theme.objects.filter(
                        id=1).first(), avatar=Avatar.objects.first())
                    profile.save()

                    user = authenticate(username=form.cleaned_data["username"],
                                        password=form.cleaned_data["password"])

                    if user is not None:
                        login(request, user)
                        return HttpResponseRedirect("/")

                except Exception as e:
                    raise Exception(str(e))
                    context["form"] = form
                    context["code_error"] = 2
                    context["forbidden_username"] = 2
                    context["message"] = "El nombre de usuario no está disponible"
                    return render(request, "app/signin.html", context=context)
        else:
            context["form"] = form
            context["code_error"] = 3
            context["message"] = "Debes rellenar todos los campos"
            return render(request, "app/signin.html", context=context)

    context["form"] = form
    return render(request, "app/signin.html", context=context)


@login_required()
def home(request):
    profile = Profile.objects.get(user=request.user)
    form = uploadImageProfileForm(
        request.POST or None, request.FILES or None, instance=profile)

    one_month_ago = timezone.now() - timezone.timedelta(days=30)
    active_shows = Show.objects.filter(user=request.user, date_update__gte=one_month_ago).exclude(
        states__in=[1]).order_by("-date_update")

    next_episodes = []

    try:
        for show in active_shows:

            last_episode_season_seen = Episode.objects.filter(
                user=request.user, states__in=[1], show=show).order_by("season_number").last()
            last_episode_seen = Episode.objects.filter(user=request.user, states__in=[
                                                       1], show=show, season_number=last_episode_season_seen.season_number).order_by("episode_number").last()
            next_episode = Episode.objects.filter(user=request.user, show=show, season_number=last_episode_season_seen.season_number,
                                                  episode_number__gt=last_episode_seen.episode_number).order_by('episode_number')

            if len(next_episode) > 0:
                next_episode = next_episode.first()

            next_episodes.append({"id_show": next_episode.show.id_show, "name": show.name,
                                 "season_number": next_episode.season_number, "episode_number": next_episode.episode_number})
    except:
        print("Error en siguiente episodio")

    activitys = Activity.objects.all().order_by("-date_add")[:300]
    activitys_veo = []

    days = []
    for activity in activitys:
        if not activity.date_add.date() in days:
            date_activity = activity.date_add.date()

            f_start = datetime.combine(date_activity, datetime.min.time())
            f_fin = datetime.combine(date_activity, datetime.max.time())

            days.append(date_activity)
            activitys_veo.append({"year": f_start.year, "month": f_start.month, "day": f_start.day, "n_activitys": len(
                Activity.objects.filter(date_add__gte=f_start, date_add__lte=f_fin))})

    if form.is_valid():
        form.save()

    createAvatars()

    context = {
        "activitys_veo": activitys_veo,
        "profile": profile,
        "unread_recommendations": len(Recommendation.objects.filter(to_user=profile, read=False)),
        "form": form,
        "themes": Theme.objects.all(),
        "avatars": Avatar.objects.all(),
        "next_episodes": next_episodes,
        "activitys": Activity.objects.filter(user__in=Profile.objects.get(user=request.user).followings.all()).order_by("-date_add")[:10]
    }
    return render(request, "app/home.html", context=context)


def seeEpisode(request):

    id_show = request.POST["id_show"]
    season_number = request.POST["season_number"]
    episode_number = request.POST["episode_number"]

    episode_to_seen = Episode.objects.filter(show=Show.objects.get(
        id_show=id_show, user=request.user), season_number=season_number, episode_number=episode_number, user=request.user)

    if len(episode_to_seen) > 0:
        episode_to_seen = episode_to_seen.first()
        episode_to_seen.states.add(State.objects.get(id=1))
        result = "ok"
    else:
        result = "error"

    data = {
        'result': result,
    }

    return JsonResponse(data)


@login_required()
def movies(request):
    profile = Profile.objects.get(user=request.user)
    form = uploadImageProfileForm(
        request.POST or None, request.FILES or None, instance=profile)
    if form.is_valid():
        form.save()

    context = {
        "profile": profile,
        "unread_recommendations": len(Recommendation.objects.filter(to_user=profile, read=False)),
        "themes": Theme.objects.all(),
        "form": form,
        "avatars": Avatar.objects.all(),
    }
    return render(request, "app/movies.html", context=context)


@login_required()
def shows(request):
    profile = Profile.objects.get(user=request.user)
    form = uploadImageProfileForm(
        request.POST or None, request.FILES or None, instance=profile)
    if form.is_valid():
        form.save()

    context = {
        "profile": profile,
        "unread_recommendations": len(Recommendation.objects.filter(to_user=profile, read=False)),
        "themes": Theme.objects.all(),
        "form": form,
        "avatars": Avatar.objects.all(),
    }
    return render(request, "app/shows.html", context=context)

@login_required()
def social(request):
    profile = Profile.objects.get(user=request.user)
    recommentations = Recommendation.objects.filter(
        to_user=profile).order_by("-creation_date")[:30]
    unread_recommendations = len(
        Recommendation.objects.filter(to_user=profile, read=False))
    form = uploadImageProfileForm(
        request.POST or None, request.FILES or None, instance=profile)
    if form.is_valid():
        form.save()

    profiles = []
    for _profile in Profile.objects.all():
        if not request.user == _profile.user:
            if (_profile.user in Profile.objects.get(user=request.user).followings.all()):
                profiles.append({"exists": True, "profile": _profile})
            else:
                profiles.append({"exists": False, "profile": _profile})
    context = {
        "profile": profile,
        "recommendations": recommentations,
        "unread_recommendations": unread_recommendations,
        "themes": Theme.objects.all(),
        "form": form,
        "avatars": Avatar.objects.all(),
        "profilesJSON": profiles,
    }
    return render(request, "app/social.html", context=context)


def readRecommendations(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    Recommendation.objects.filter(
        to_user=profile, read=False).update(read=True)

    data = {
        'result': "ok",
    }

    return JsonResponse(data)


def changeAvatar(request):

    profile = Profile.objects.filter(user=request.user).first()
    Profile.objects.filter(user=request.user).update(
        avatar=Avatar.objects.get(id=request.POST["id_avatar"]))
    image = "/home/veo/Veo/" + str(profile.image)
    Profile.objects.filter(user=request.user).update(image="")

    try:
        if (os.path.isfile(image)):
            os.remove(image)

    except Exception as e:
        print(str(e))

    data = {
        'result': "ok",
    }

    return JsonResponse(data)


def changeCelularSavings(request):

    status = request.POST["status"]

    if status == "true":
        state = True
    else:
        state = False

    Profile.objects.filter(user=request.user).update(celularDataSavings=state)

    data = {
        'result': "ok",
    }

    return JsonResponse(data)


def changeTheme(request, theme=None):
    Profile.objects.filter(user=request.user).update(
        theme=Theme.objects.get(id=theme))
    print(Theme.objects.get(id=theme))
    return HttpResponseRedirect("/")


def movie(request, id=None):
    if request.user.is_anonymous:
        profile = None
    else:
        profile = Profile.objects.get(user=request.user)

    context = {
        "profile": profile,
        "unread_recommendations": len(Recommendation.objects.filter(to_user=profile, read=False)),
        "id": id,
        "themes": Theme.objects.all()
    }
    return render(request, "app/movie.html", context=context)


def show(request, id=None):
    if request.user.is_anonymous:
        profile = None
    else:
        profile = Profile.objects.get(user=request.user)

    context = {
        "profile": profile,
        "unread_recommendations": len(Recommendation.objects.filter(to_user=profile, read=False)),
        "id": id,
        "themes": Theme.objects.all()
    }
    return render(request, "app/show.html", context=context)


def changeGenreColors(request):
    status = request.POST["status"]

    if status == "true":
        Profile.objects.filter(user=request.user).update(colorGenres=True)
    else:
        Profile.objects.filter(user=request.user).update(colorGenres=False)

    data = {
        'result': status,
    }

    return JsonResponse(data)

# ------------------------------------- MOVIE --------------------------------------------------------------------------


def addMovieToSee(request):
    movie = Movie.objects.filter(
        id_movie=request.POST["id"], user=request.user)

    if len(movie) == 0:
        movie = Movie.objects.create(id_movie=request.POST["id"], user=request.user, title=request.POST["title"],
                                     poster_path=request.POST["poster_path"], vote_average=request.POST["vote_average"])
        movie.states.add(State.objects.get(id=2))

        Activity.objects.create(
            user=request.user, operation=Operation.objects.get(id=1), movie=movie)

    else:
        movie.first().states.add(State.objects.get(id=2))
        Activity.objects.create(
            user=request.user, operation=Operation.objects.get(id=1), movie=movie.first())

    data = {
        'result': request.POST["title"] + " añadida a la lista de pendientes",
    }

    return JsonResponse(data)


def isMovieOnMyList(request):
    movie = Movie.objects.filter(
        id_movie=request.POST["id"], user=request.user)

    if len(movie) > 0:
        states = []
        for state in movie.first().states.all():
            states.append({"id": state.id, "state": state.name})
        data = {
            'id': request.POST["id"],
            'states': states
        }
    else:
        data = {
            'id': request.POST["id"],
            'states': "null",
        }

    return JsonResponse(data)


def removeMovieToSee(request):
    movie = Movie.objects.filter(
        id_movie=request.POST["id"], user=request.user)

    movie_title = movie.first().title

    movie.first().states.remove(State.objects.get(id=2))

    if (len(movie.first().states.all()) == 0):
        movie.delete()

    data = {
        'result': movie_title + " eliminada de mi lista de pendientes",
    }

    return JsonResponse(data)


def setMovieToSeen(request):

    movie = Movie.objects.filter(
        id_movie=request.POST["id"], user=request.user)

    if len(movie) == 0:
        movie = Movie.objects.create(id_movie=request.POST["id"], user=request.user, title=request.POST["title"],
                                     poster_path=request.POST["poster_path"], vote_average=request.POST["vote_average"])
        movie.states.clear()
        movie.states.remove(State.objects.get(id=2))
        movie.states.add(State.objects.get(id=1))
        Activity.objects.create(
            user=request.user, operation=Operation.objects.get(id=2), movie=movie)
    else:
        movie.first().states.remove(State.objects.get(id=2))
        movie.first().states.add(State.objects.get(id=1))
        Activity.objects.create(
            user=request.user, operation=Operation.objects.get(id=2), movie=movie.first())

    data = {
        'result': request.POST["title"] + " añadida a vistas",
    }

    return JsonResponse(data)


def setMovieToNotSeen(request):

    movie = Movie.objects.filter(
        id_movie=request.POST["id"], user=request.user)

    movie_title = movie.first().title

    movie.first().states.remove(State.objects.get(id=1))

    if (len(movie.first().states.all()) == 0):
        movie.delete()

    data = {
        'result': movie_title + " eliminada de vistas",
    }

    return JsonResponse(data)


def myMoviesToSee(request):
    movies = Movie.objects.filter(user=request.user, states__in=[
                                  2]).order_by("-date_add")
    results = []

    for movie in movies:
        results.append(
            {"id": movie.id_movie, "poster_path": movie.poster_path})

    data = {
        'results': results
    }

    return JsonResponse(data)


def myMoviesSeen(request):
    movies = Movie.objects.filter(user=request.user, states__in=[
                                  1]).order_by("-date_add")
    results = []

    for movie in movies:
        results.append(
            {"id": movie.id_movie, "poster_path": movie.poster_path})

    data = {
        'results': results
    }

    return JsonResponse(data)


# ------------------------------------- SHOW ---------------------------------------------------------------------------
def addShowToSee(request):

    show = Show.objects.filter(id_show=request.POST["id"], user=request.user)

    if len(show) == 0:
        show = Show.objects.create(id_show=request.POST["id"], user=request.user, name=request.POST["name"],
                                   poster_path=request.POST["poster_path"], vote_average=request.POST["vote_average"])
        show.states.add(State.objects.get(id=2))

        seasons = ast.literal_eval(request.POST["seasons"])
        for season in seasons:
            for episode in season["episodes"]:
                Episode.objects.create(show=show, id_episode=episode["id"], season_number=season["season_number"],
                                       episode_number=episode["episode_number"], user=request.user)
        Activity.objects.create(
            user=request.user, operation=Operation.objects.get(id=3), show=show)
    else:
        show.first().states.add(State.objects.get(id=2))
        Activity.objects.create(
            user=request.user, operation=Operation.objects.get(id=3), show=show.first())

    data = {
        'result': request.POST["name"] + " añadida a la lista de pendientes",
    }

    return JsonResponse(data)


def isShowOnMyList(request):
    show = Show.objects.filter(id_show=request.POST["id"], user=request.user)

    if len(show) > 0:
        states = []
        for state in show.first().states.all():
            states.append({"id": state.id, "state": state.name})
        data = {
            'id': request.POST["id"],
            'states': states
        }
    else:
        data = {
            'id': request.POST["id"],
            'states': "null",
        }

    return JsonResponse(data)


def removeShowToSee(request):
    show = Show.objects.filter(id_show=request.POST["id"], user=request.user)

    show_title = show.first().name

    show.first().states.remove(State.objects.get(id=2))

    if len(show.first().states.all()) == 0 and len(show.first().getEpisodesSeen()) == 0:
        show.delete()

    data = {
        'result': show_title + " eliminada de mi lista de pendientes",
    }

    return JsonResponse(data)


def setShowToSeen(request):

    show = Show.objects.filter(id_show=request.POST["id"], user=request.user)

    if len(show) == 0:
        show = Show.objects.create(id_show=request.POST["id"], user=request.user, name=request.POST["name"],
                                   poster_path=request.POST["poster_path"], vote_average=request.POST["vote_average"])
        show.states.remove(State.objects.get(id=2))
        show.states.add(State.objects.get(id=1))

        seasons = ast.literal_eval(request.POST["seasons"])
        for season in seasons:
            for episode in season["episodes"]:
                episode = Episode.objects.create(show=show, id_episode=episode["id"], season_number=season["season_number"],
                                                 episode_number=episode["episode_number"], user=request.user)
                episode.states.add(State.objects.get(id=1))

        Show.objects.filter(id=request.POST["id"]).update(
            date_update=datetime.now())
        Activity.objects.create(
            user=request.user, operation=Operation.objects.get(id=4), show=show)
    else:
        show.first().states.remove(State.objects.get(id=2))
        show.first().states.add(State.objects.get(id=1))
        for episode in show.first().getEpisodes():
            episode.states.add(State.objects.get(id=1))

        show.update(date_update=datetime.now())
        Activity.objects.create(
            user=request.user, operation=Operation.objects.get(id=4), show=show.first())

    data = {
        'result': request.POST["name"] + " añadida a vistas",
    }

    return JsonResponse(data)


def setShowToNotSeen(request):

    show = Show.objects.filter(id_show=request.POST["id"], user=request.user)

    show_name = show.first().name

    show.first().states.remove(State.objects.get(id=1))

    for episode in show.first().getEpisodes():
        episode.states.remove(State.objects.get(id=1))

    if len(show.first().states.all()) == 0 and len(show.first().getEpisodesSeen()) == 0:
        show.delete()

    data = {
        'result': show_name + " eliminada de vistas",
    }

    return JsonResponse(data)

# List of Shows in active


def myActiveShows(request):
    one_month_ago = timezone.now() - timezone.timedelta(days=30)
    shows = Show.objects.filter(user=request.user, date_update__gte=one_month_ago).exclude(
        states__in=[1]).order_by("-date_update")

    results = []

    for show in shows:
        results.append({"id": show.id_show, "poster_path": show.poster_path})

    data = {
        'results': results
    }

    return JsonResponse(data)

# List of Shows in active


def myForgottenShows(request):
    one_month_ago = timezone.now() - timezone.timedelta(days=30)
    shows = Show.objects.filter(user=request.user, date_update__lte=one_month_ago).exclude(
        states__in=[1]).order_by("-date_update")

    results = []

    for show in shows:
        results.append({"id": show.id_show, "poster_path": show.poster_path})

    data = {
        'results': results
    }

    return JsonResponse(data)

# Change Episode State


def changeEpisodeState(request):  # Cambiar

    show = Show.objects.filter(
        id_show=request.POST["id_show"], user=request.user)

    if len(show) == 0:
        show = Show.objects.create(id_show=request.POST["id_show"], user=request.user, name=request.POST["name"],
                                   poster_path=request.POST["poster_path"])

        seasons = ast.literal_eval(request.POST["seasons"])

        for season in seasons:
            for episode in season["episodes"]:
                Episode.objects.create(show=show, id_episode=episode["id"], season_number=season["season_number"],
                                       episode_number=episode["episode_number"], user=request.user)

        show = Show.objects.filter(id=show.id)

    result = ""
    if request.POST["state"] == "1":

        _show = Show.objects.filter(
            id_show=request.POST["id_show"], user=request.user).first()

        if len(Episode.objects.filter(id_episode=request.POST["id_episode"], user=request.user)) == 0:
            seasons = ast.literal_eval(request.POST["seasons"])

            for season in seasons:
                for episode in season["episodes"]:
                    if len(Episode.objects.filter(id_episode=episode["id"], user=request.user)) == 0:
                        Episode.objects.create(show=_show, id_episode=episode["id"], season_number=season["season_number"],
                                               episode_number=episode["episode_number"], user=request.user)

        Episode.objects.get(id_episode=request.POST["id_episode"], user=request.user).states.add(
            State.objects.get(id=1))

        Activity.objects.create(user=request.user, operation=Operation.objects.get(
            id=5), episode=Episode.objects.get(id_episode=request.POST["id_episode"], user=request.user))

        if len(Episode.objects.filter(show=Episode.objects.get(id_episode=request.POST["id_episode"], user=request.user).show, user=request.user, states__in=[1])) == len(Episode.objects.filter(show=Episode.objects.get(id_episode=request.POST["id_episode"], user=request.user).show, user=request.user)):
            show.first().states.add(State.objects.get(id=1))
            Activity.objects.create(
                user=request.user, operation=Operation.objects.get(id=4), show=show.first())
            show.update(date_update=datetime.now())
        else:
            show.first().states.remove(State.objects.get(id=1))

        show.update(date_update=datetime.now())
        result = "Episodio marcado como visto"
    else:
        Episode.objects.get(id_episode=request.POST["id_episode"], user=request.user).states.remove(
            State.objects.get(id=1))
        show.first().states.remove(State.objects.get(id=1))
        result = "Episodio marcado como no visto"

    if len(show.first().states.all()) == 0 and len(show.first().getEpisodesSeen()) == 0:
        show.delete()

    data = {
        'results': result
    }

    return JsonResponse(data)

# Syncronize episodes Seen


def syncronizeEpisodes(request):

    episodes = Episode.objects.filter(show=Show.objects.filter(id_show=request.POST["id_show"], user=request.user).first(
    ), season_number=request.POST["season_number"], user=request.user, states__in=[1])

    results = []

    for episode in episodes:
        results.append({"id": str(episode.show.id_show) + "_" +
                       str(episode.season_number) + "_" + str(episode.episode_number)})

    data = {
        'results': results
    }

    return JsonResponse(data)

# List of Shows seen


def myShowsSeen(request):
    shows = Show.objects.filter(user=request.user, states__in=[
                                1]).order_by("-date_update")

    results = []

    for show in shows:
        results.append({"id": show.id_show, "poster_path": show.poster_path})

    data = {
        'results': results
    }

    return JsonResponse(data)

# List of Shows pending


def myShowsPending(request):
    shows = Show.objects.filter(user=request.user, states__in=[
                                2]).order_by("-date_update")

    results = []

    for show in shows:
        results.append({"id": show.id_show, "poster_path": show.poster_path})

    data = {
        'results': results
    }

    return JsonResponse(data)

# ---------------------------------------- ACTIVITY --------------------------------------------------------------------
# All Activity


def myActivity(request):
    activitys = Activity.objects.filter(
        user=request.user).order_by("-date_add")[:50]

    results = []

    for activity in activitys:
        if (activity.operation.id == 1):
            user_str = ""
            description = ""

            if (activity.user == request.user):
                description = "Has añadido <b>" + \
                    activity.movie.title + "</b> a tu lista de pendientes"
            else:
                user_str = activity.user.username,
                description = "ha añadido <b>" + activity.movie.title + \
                    "</b> a su lista de pendientes"

            results.append({"user": user_str,
                            "description": description,
                            "href": "/movie/" + str(activity.movie.id_movie),
                            "poster_path": "https://image.tmdb.org/t/p/w200" + activity.movie.poster_path,
                            "date": (activity.date_add + timedelta(hours=1)).strftime("%d-%m-%Y %H:%M:%S")})
        if (activity.operation.id == 2):
            user_str = ""
            description = ""

            if (activity.user == request.user):
                description = "Has visto <b>" + activity.movie.title + "</b>",
            else:
                user_str = activity.user.username,
                description = "ha visto <b>" + activity.movie.title + "</b>",

            results.append({"user": user_str,
                            "description": description,
                            "href": "/movie/" + str(activity.movie.id_movie),
                            "poster_path": "https://image.tmdb.org/t/p/w200" + activity.movie.poster_path,
                            "date": (activity.date_add + timedelta(hours=1)).strftime("%d-%m-%Y %H:%M:%S")})
        if (activity.operation.id == 3):
            user_str = ""
            description = ""

            if (activity.user == request.user):
                description = "Has añadido <b>" + activity.show.name + \
                    "</b> a tu lista de pendientes",
            else:
                user_str = activity.user.username,
                description = "ha añadido <b>" + activity.show.name + \
                    "</b> a su lista de pendientes",

            results.append({"user": user_str,
                            "description": description,
                            "href": "/show/" + str(activity.show.id_show),
                            "poster_path": "https://image.tmdb.org/t/p/w200" + activity.show.poster_path,
                            "date": (activity.date_add + timedelta(hours=1)).strftime("%d-%m-%Y %H:%M:%S")})
        if (activity.operation.id == 4):
            user_str = ""
            description = ""

            if (activity.user == request.user):
                description = "Has visto <b>" + activity.show.name + "</b>",
            else:
                user_str = activity.user.username,
                description = "ha visto <b>" + activity.show.name + "</b>",

            results.append({"user": user_str,
                            "description": description,
                            "href": "/show/" + str(activity.show.id_show),
                            "poster_path": "https://image.tmdb.org/t/p/w200" + activity.show.poster_path,
                            "date": (activity.date_add + timedelta(hours=1)).strftime("%d-%m-%Y %H:%M:%S")})
        if (activity.operation.id == 5):
            user_str = ""
            description = ""

            if (activity.user == request.user):
                description = "Has visto el <b>E" + str(activity.episode.episode_number) + "xT" + str(
                    activity.episode.season_number) + "</b> de <b>" + activity.episode.show.name + "</b>",
            else:
                user_str = activity.user.username,
                description = "ha visto el <b>E" + str(activity.episode.episode_number) + "xT" + str(
                    activity.episode.season_number) + "</b> de <b>" + activity.episode.show.name + "</b>",

            results.append({"user": user_str,
                            "description": description,
                            "href": "/show/" + str(activity.episode.show.id_show),
                            "poster_path": "https://image.tmdb.org/t/p/w200" + activity.episode.show.poster_path,
                            "date": (activity.date_add + timedelta(hours=1)).strftime("%d-%m-%Y %H:%M:%S")})
        if (activity.operation.id == 6):
            user_str = ""
            description = ""

            if (activity.user == request.user):
                description = "Has seguido a <b>" + activity.follower.username + "</b>",
            else:
                user_str = activity.user.username,
                description = "ahora sigue a <b>" + activity.follower.username + "</b>",

            poster_path = ""
            if not Profile.objects.get(user=activity.follower).avatar == None:
                poster_path = Profile.objects.get(
                    user=activity.follower).avatar.src

            results.append({"user": user_str,
                            "description": description,
                            "href": "",
                            "poster_path": poster_path,
                            "date": (activity.date_add + timedelta(hours=1)).strftime("%d-%m-%Y %H:%M:%S")})

    data = {
        'results': results
    }

    return JsonResponse(data)

# My Followings Activity


def myFollowingsActivity(request):
    activitys = Activity.objects.filter(user__in=Profile.objects.get(
        user=request.user).followings.all()).order_by("-date_add")[:50]

    results = []

    for activity in activitys:
        if (activity.operation.id == 1):
            user_str = ""
            user_id = ""
            description = ""

            if (activity.user == request.user):
                description = "Has añadido <b>" + \
                    activity.movie.title + "</b> a tu lista de pendientes"
            else:
                user_str = activity.user.username
                user_id = activity.user.id
                description = "ha añadido <b>" + activity.movie.title + \
                    "</b> a su lista de pendientes"

            results.append({"user": user_str,
                            "user_id": user_id,
                            "description": description,
                            "href": "/movie/" + str(activity.movie.id_movie),
                            "poster_path": "https://image.tmdb.org/t/p/w200" + activity.movie.poster_path,
                            "date": (activity.date_add + timedelta(hours=1)).strftime("%d-%m-%Y %H:%M:%S")})
        if (activity.operation.id == 2):
            user_str = ""
            user_id = ""
            description = ""

            if (activity.user == request.user):
                description = "Has visto <b>" + activity.movie.title + "</b>",
            else:
                user_str = activity.user.username
                user_id = activity.user.id
                description = "ha visto <b>" + activity.movie.title + "</b>",

            results.append({"user": user_str,
                            "user_id": user_id,
                            "description": description,
                            "href": "/movie/" + str(activity.movie.id_movie),
                            "poster_path": "https://image.tmdb.org/t/p/w200" + activity.movie.poster_path,
                            "date": (activity.date_add + timedelta(hours=1)).strftime("%d-%m-%Y %H:%M:%S")})
        if (activity.operation.id == 3):
            user_str = ""
            user_id = ""
            description = ""

            if (activity.user == request.user):
                description = "Has añadido <b>" + activity.show.name + \
                    "</b> a tu lista de pendientes",
            else:
                user_str = activity.user.username
                user_id = activity.user.id
                description = "ha añadido <b>" + activity.show.name + \
                    "</b> a su lista de pendientes",

            results.append({"user": user_str,
                            "user_id": user_id,
                            "description": description,
                            "href": "/show/" + str(activity.show.id_show),
                            "poster_path": "https://image.tmdb.org/t/p/w200" + activity.show.poster_path,
                            "date": (activity.date_add + timedelta(hours=1)).strftime("%d-%m-%Y %H:%M:%S")})
        if (activity.operation.id == 4):
            user_str = ""
            user_id = ""
            description = ""

            if (activity.user == request.user):
                description = "Has visto <b>" + activity.show.name + "</b>",
            else:
                user_str = activity.user.username
                user_id = activity.user.id
                description = "ha visto <b>" + activity.show.name + "</b>",

            results.append({"user": user_str,
                            "user_id": user_id,
                            "description": description,
                            "href": "/show/" + str(activity.show.id_show),
                            "poster_path": "https://image.tmdb.org/t/p/w200" + activity.show.poster_path,
                            "date": (activity.date_add + timedelta(hours=1)).strftime("%d-%m-%Y %H:%M:%S")})
        if (activity.operation.id == 5):
            user_str = ""
            user_id = ""
            description = ""

            if (activity.user == request.user):
                description = "Has visto el <b>E" + str(activity.episode.episode_number) + "xT" + str(
                    activity.episode.season_number) + "</b> de <b>" + activity.episode.show.name + "</b>",
            else:
                user_str = activity.user.username
                user_id = activity.user.id
                description = "ha visto el <b>E" + str(activity.episode.episode_number) + "xT" + str(
                    activity.episode.season_number) + "</b> de <b>" + activity.episode.show.name + "</b>",

            results.append({"user": user_str,
                            "user_id": user_id,
                            "description": description,
                            "href": "/show/" + str(activity.episode.show.id_show),
                            "poster_path": "https://image.tmdb.org/t/p/w200" + activity.episode.show.poster_path,
                            "date": (activity.date_add + timedelta(hours=1)).strftime("%d-%m-%Y %H:%M:%S")})
        if (activity.operation.id == 6):
            user_str = ""
            user_id = ""
            description = ""

            if (activity.user == request.user):
                description = "Has seguido a <b>" + activity.follower.username + "</b>",
            else:
                user_str = activity.user.username
                user_id = activity.user.id
                description = "ahora sigue a <b>" + activity.follower.username + "</b>",

            poster_path = ""
            if not Profile.objects.get(user=activity.follower).avatar == None:
                poster_path = Profile.objects.get(
                    user=activity.follower).avatar.src

            results.append({"user": user_str,
                            "user_id": user_id,
                            "description": description,
                            "href": "",
                            "poster_path": poster_path,
                            "date": (activity.date_add + timedelta(hours=1)).strftime("%d-%m-%Y %H:%M:%S")})

    data = {
        'results': results
    }

    return JsonResponse(data)

# My Followings Recient Activity


def myFollowingsRecientActivity(request):
    activitys = Activity.objects.filter(Q(user__in=Profile.objects.get(
        user=request.user).followings.all()) | Q(user=request.user)).order_by("-date_add")[:10]

    results = []

    for activity in activitys:
        if (activity.operation.id == 1):
            user_str = ""
            user_id = ""
            description = ""

            if (activity.user == request.user):
                description = "Has añadido <b>" + \
                    activity.movie.title + "</b> a tu lista de pendientes"
            else:
                user_str = activity.user.username
                user_id = activity.user.id
                description = "ha añadido <b>" + activity.movie.title + \
                    "</b> a su lista de pendientes"

            results.append({"user": user_str,
                            "user_id": user_id,
                            "description": description,
                            "href": "/movie/" + str(activity.movie.id_movie),
                            "poster_path": "https://image.tmdb.org/t/p/w200" + activity.movie.poster_path,
                            "date": (activity.date_add + timedelta(hours=1)).strftime("%d-%m-%Y %H:%M:%S")})
        if (activity.operation.id == 2):
            user_str = ""
            user_id = ""
            description = ""

            if (activity.user == request.user):
                description = "Has visto <b>" + activity.movie.title + "</b>",
            else:
                user_str = activity.user.username
                user_id = activity.user.id
                description = "ha visto <b>" + activity.movie.title + "</b>",

            results.append({"user": user_str,
                            "user_id": user_id,
                            "description": description,
                            "href": "/movie/" + str(activity.movie.id_movie),
                            "poster_path": "https://image.tmdb.org/t/p/w200" + activity.movie.poster_path,
                            "date": (activity.date_add + timedelta(hours=1)).strftime("%d-%m-%Y %H:%M:%S")})
        if (activity.operation.id == 3):
            user_str = ""
            user_id = ""
            description = ""

            if (activity.user == request.user):
                description = "Has añadido <b>" + activity.show.name + \
                    "</b> a tu lista de pendientes",
            else:
                user_str = activity.user.username
                user_id = activity.user.id
                description = "ha añadido <b>" + activity.show.name + \
                    "</b> a su lista de pendientes",

            results.append({"user": user_str,
                            "user_id": user_id,
                            "description": description,
                            "href": "/show/" + str(activity.show.id_show),
                            "poster_path": "https://image.tmdb.org/t/p/w200" + activity.show.poster_path,
                            "date": (activity.date_add + timedelta(hours=1)).strftime("%d-%m-%Y %H:%M:%S")})
        if (activity.operation.id == 4):
            user_str = ""
            user_id = ""
            description = ""

            if (activity.user == request.user):
                description = "Has visto <b>" + activity.show.name + "</b>",
            else:
                user_str = activity.user.username
                user_id = activity.user.id
                description = "ha visto <b>" + activity.show.name + "</b>",

            results.append({"user": user_str,
                            "user_id": user_id,
                            "description": description,
                            "href": "/show/" + str(activity.show.id_show),
                            "poster_path": "https://image.tmdb.org/t/p/w200" + activity.show.poster_path,
                            "date": (activity.date_add + timedelta(hours=1)).strftime("%d-%m-%Y %H:%M:%S")})
        if (activity.operation.id == 5):
            user_str = ""
            user_id = ""
            description = ""

            if (activity.user == request.user):
                description = "Has visto el <b>E" + str(activity.episode.episode_number) + "xT" + str(
                    activity.episode.season_number) + "</b> de <b>" + activity.episode.show.name + "</b>",
            else:
                user_str = activity.user.username
                user_id = activity.user.id
                description = "ha visto el <b>E" + str(activity.episode.episode_number) + "xT" + str(
                    activity.episode.season_number) + "</b> de <b>" + activity.episode.show.name + "</b>",

            results.append({"user": user_str,
                            "user_id": user_id,
                            "description": description,
                            "href": "/show/" + str(activity.episode.show.id_show),
                            "poster_path": "https://image.tmdb.org/t/p/w200" + activity.episode.show.poster_path,
                            "date": (activity.date_add + timedelta(hours=1)).strftime("%d-%m-%Y %H:%M:%S")})
        if (activity.operation.id == 6):
            user_str = ""
            user_id = ""
            description = ""

            if (activity.user == request.user):
                description = "Has seguido a <b>" + activity.follower.username + "</b>",
            else:
                user_str = activity.user.username
                user_id = activity.user.id
                description = "ahora sigue a <b>" + activity.follower.username + "</b>",

            poster_path = ""
            if not Profile.objects.get(user=activity.follower).avatar == None:
                poster_path = Profile.objects.get(
                    user=activity.follower).avatar.src

            results.append({"user": user_str,
                            "user_id": user_id,
                            "description": description,
                            "href": "",
                            "poster_path": poster_path,
                            "date": (activity.date_add + timedelta(hours=1)).strftime("%d-%m-%Y %H:%M:%S")})

    data = {
        'results': results
    }

    return JsonResponse(data)

# ----------------------------------------- DOWNLOADS ------------------------------------------------------------------
@login_required()
def download(request, name):
    profile = Profile.objects.get(user=request.user)
    form = uploadImageProfileForm(
        request.POST or None, request.FILES or None, instance=profile)
    if form.is_valid():
        form.save()

    downloads_manager = DownloadsManager()

    torrents_find = downloads_manager.search_torrents_tpb(name)

    context = {
        "profile": profile,
        "unread_recommendations": len(Recommendation.objects.filter(to_user=profile, read=False)),
        "themes": Theme.objects.all(),
        "form": form,
        "avatars": Avatar.objects.all(),
        "name": name,
        "torrents_find": torrents_find
    }
    return render(request, "app/download.html", context=context)


def download_torrent(request):
    results = {}

    torrent_href = request.POST["href"]
    torrent_hash = request.POST["hash"]

    downloads_manager = DownloadsManager()
    status = downloads_manager.download_torrent(torrent_href, torrent_hash)

    data = {
        'status': status
    }

    return JsonResponse(data)


# ----------------------------------------- MEDIA ----------------------------------------------------------------------
def updateMediaPoster(request):
    results = {}

    media_id = request.POST["media_id"]
    type = request.POST["type"]
    poster_path = request.POST["poster_path"]

    results["media_id"] = media_id
    results["type"] = type
    results["poster_path"] = poster_path

    if type == "movie":
        Movie.objects.filter(id_movie=media_id, user=request.user).update(
            poster_path=poster_path)
    elif type == "show":
        Show.objects.filter(id_show=media_id, user=request.user).update(
            poster_path=poster_path)

    data = {
        'results': results
    }

    return JsonResponse(data)

# --------------------------------------- FOLLOWERS --------------------------------------------------------------------


def followUser(request):

    Profile.objects.get(user=request.user).followings.add(
        User.objects.get(id=request.POST["id_user"]))

    Activity.objects.create(user=request.user, operation=Operation.objects.get(
        id=6), follower=User.objects.get(id=request.POST["id_user"]))

    data = {
        'result': "ok",
    }

    return JsonResponse(data)


def unFollowUser(request):

    Profile.objects.get(user=request.user).followings.remove(
        User.objects.get(id=request.POST["id_user"]))

    data = {
        'result': "ok",
    }

    return JsonResponse(data)

# ---------------------------------------- SEARCH ----------------------------------------------------------------------


@login_required()
def search(request, query=None):
    form = uploadImageProfileForm(
        request.POST or None, request.FILES or None, instance=Profile.objects.get(user=request.user))
    if form.is_valid():
        form.save()
    context = {
        "profile": Profile.objects.get(user=request.user),
        "unread_recommendations": len(Recommendation.objects.filter(to_user=Profile.objects.get(user=request.user), read=False)),
        "themes": Theme.objects.all(),
        "avatars": Avatar.objects.all(),
        "query": query,
        "form": form,
    }
    return render(request, "app/search.html", context=context)

# ---------------------------------------- PROFILE ---------------------------------------------------------------------


@login_required()
def profile(request, id=None):
    user = User.objects.get(id=id)
    activitys = Activity.objects.filter(user=user).order_by("-date_add")
    activitys_dir = []

    days = []
    for activity in activitys:
        if not activity.date_add.date() in days:
            date_activity = activity.date_add.date()

            f_start = datetime.combine(date_activity, datetime.min.time())
            f_fin = datetime.combine(date_activity, datetime.max.time())

            days.append(date_activity)
            activitys_dir.append({"year": f_start.year, "month": f_start.month, "day": f_start.day, "n_activitys": len(
                Activity.objects.filter(user=user, date_add__gte=f_start, date_add__lte=f_fin))})

    user_lists = List.objects.filter(user=user)

    form = uploadImageProfileForm(
        request.POST or None, request.FILES or None, instance=Profile.objects.get(user=user))
    if form.is_valid():
        form.save()

    context = {
        "activitys": activitys,
        "activitys_summary": activitys[:40],
        "activitys_dir": activitys_dir,
        "user_lists": user_lists,
        "profile_visited": Profile.objects.get(user=user),
        "profile": Profile.objects.get(user=request.user),
        "unread_recommendations": len(Recommendation.objects.filter(to_user=Profile.objects.get(user=request.user), read=False)),
        "themes": Theme.objects.all(),
        "form": form,
        "avatars": Avatar.objects.all(),
    }

    return render(request, "app/profile.html", context=context)

# Create a new List for user


def newList(request):
    user = User.objects.get(id=request.POST["id_user"])

    newList = List.objects.create(
        user=user, name=request.POST["name"], color=request.POST["color"])

    if newList:
        result = newList.id
    else:
        result = -1

    data = {
        'result': result
    }

    return JsonResponse(data)

# Delete a list for user


def removeList(request):

    # Delete all movies and shows from this list with only List status
    list = List.objects.get(id=request.POST["id_list"])

    for movie in list.movies.all():
        if len(movie.states.all()) == 1:
            state = movie.states.all().first()
            if state == State.objects.get(id=3):
                Movie.objects.filter(id=movie.id).delete()

    for show in list.shows.all():
        if len(show.states.all()) == 1:
            state = show.states.all().first()
            if state == State.objects.get(id=3):
                Show.objects.filter(id=show.id).delete()
                print("\n\n\n")
                print("Serie Eliminada")
                print("\n\n\n")

    List.objects.filter(id=request.POST["id_list"]).delete()

    data = {
        'result': 'ok'
    }

    return JsonResponse(data)

# Añade una pelicula o serie a una de tus listas


def addToList(request):
    type = request.POST["type"]
    list = List.objects.get(id=request.POST["id_list"])

    # Case Movie:
    if type == "1":
        movie = Movie.objects.filter(
            id_movie=request.POST["id"], user=request.user)

        if len(movie) == 0:
            movie = Movie.objects.create(id_movie=request.POST["id"], user=request.user, title=request.POST["title"],
                                         poster_path=request.POST["poster_path"], vote_average=request.POST["vote_average"])
            movie.states.add(State.objects.get(id=3))
            list.movies.add(movie)
        else:
            movie.first().states.add(State.objects.get(id=3))
            list.movies.add(movie.first())

        data = {
            'result': request.POST["title"] + " añadida a tu lista " + list.name,
        }
    else:  # Case Show
        show = Show.objects.filter(
            id_show=request.POST["id"], user=request.user)

        if len(show) == 0:
            show = Show.objects.create(id_show=request.POST["id"], user=request.user, name=request.POST["name"],
                                       poster_path=request.POST["poster_path"],
                                       vote_average=request.POST["vote_average"])
            show.states.add(State.objects.get(id=3))

            seasons = ast.literal_eval(request.POST["seasons"])
            for season in seasons:
                for episode in season["episodes"]:
                    Episode.objects.create(show=show, id_episode=episode["id"], season_number=season["season_number"],
                                           episode_number=episode["episode_number"], user=request.user)
            list.shows.add(show)
        else:
            show.first().states.add(State.objects.get(id=3))
            list.shows.add(show.first())

        data = {
            'result': request.POST["name"] + " añadida a tu lista " + list.name,
        }

    return JsonResponse(data)

# Añade una pelicula o serie a una de tus listas


def deleteFromList(request):
    type = request.POST["type"]
    list = List.objects.get(id=request.POST["id_list"])
    id_media = request.POST["id_media"]

    # Case Movie:
    if type == "1":
        movie = Movie.objects.filter(id_movie=id_media, user=request.user)
        title = movie.first().title

        if len(movie.first().states.all()) > 1:
            movie.first().status.remove(State.objects.get(id=3))
            list.movies.remove(movie.first())
        else:
            list.movies.remove(movie.first())
            movie.delete()

        data = {
            'result': title + " eliminada de " + list.name,
        }
    else:  # Case Show
        show = Show.objects.filter(id_show=id_media, user=request.user)
        title = show.first().name

        if len(show.first().states.all()) > 1:
            show.first().status.remove(State.objects.get(id=3))
            list.shows.remove(show.first())
        else:
            list.shows.remove(show.first())
            show.delete()

        data = {
            'result': title + " eliminada de " + list.name,
        }

    return JsonResponse(data)


@login_required()
def list(request, id=None):
    list = List.objects.get(id=id)

    form = uploadImageProfileForm(
        request.POST or None, request.FILES or None, instance=Profile.objects.get(user=request.user))
    if form.is_valid():
        form.save()

    context = {
        "profile": Profile.objects.get(user=request.user),
        "unread_recommendations": len(Recommendation.objects.filter(to_user=Profile.objects.get(user=request.user), read=False)),
        "profile_list": Profile.objects.get(user=list.user),
        "list": list,
        "form": form,
    }

    return render(request, "app/list.html", context=context)


# Guarda la configuración de conexión de qbittorrent
def save_qtorrent_settings(request):

    Profile.objects.filter(user=request.user).update(
        qip=request.POST["qip"],
        qport=request.POST["qport"],
        quser=request.POST["quser"],
        qpassword=request.POST["qpassword"],
    )

    data = {
        'status': 'ok'
    }

    return JsonResponse(data)

# ----------------------------------------- NOTIFICATIONS --------------------------------------------------------------


def notification(request):
    data = {"title": "Veo",
            "body": "hola",
            "icon": "https://image.tmdb.org/t/p/w200/3iFm6Kz7iYoFaEcj4fLyZHAmTQA.jpg"}

    profile = Profile.objects.get(
        user=User.objects.get(username="iMacnucintosh"))

    webpush(json.loads(profile.endpoint),
            json.dumps(data),
            vapid_private_key="UP56WTB9F-H-NVOz2qbOBwDk-1txARUaCk7olQWdXdk",
            vapid_claims={"sub": "mailto:manuellopezmallorquin@syltec.es"})


def shareWithFriends(request):
    profile_from = Profile.objects.get(user=request.user)
    friends_selected = ast.literal_eval(request.POST["friends_selected"])

    for friend in friends_selected:
        to_user = Profile.objects.get(id=friend)
        Recommendation.objects.create(name=request.POST["title"], poster_path=request.POST["poster_path"],
                                      id_media=request.POST["id"], from_user=profile_from, to_user=to_user, type=request.POST["type"])

        if to_user.endpoint != "":
            if request.POST["type"] == "show":
                type = "serie"
            else:
                type = "película"

            data = {
                "title": "Veo",
                "body": profile_from.user.username + " te ha recomendado la " + type + " " + request.POST["title"],
                "icon": "https://image.tmdb.org/t/p/w200" + request.POST["poster_path"]
            }

            webpush(json.loads(to_user.endpoint),
                    json.dumps(data),
                    vapid_private_key="UP56WTB9F-H-NVOz2qbOBwDk-1txARUaCk7olQWdXdk",
                    vapid_claims={"sub": "mailto:manuellopezmallorquin@syltec.es"})

    return JsonResponse({"response": "ok"})

# Register the Endpoint for this user


def registerEndpoint(request):
    endpoint = request.POST["endpoint"]
    Profile.objects.filter(user=request.user).update(endpoint=endpoint)
    return JsonResponse({"response": "ok"})

# UnRegister the Endpoint for this user


def unRegisterEndpoint(request):
    Profile.objects.filter(user=request.user).update(endpoint="")
    return JsonResponse({"response": "ok"})
