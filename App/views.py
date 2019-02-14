# -*- coding: utf-8 -*-
import ast
import os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from App.models import *
from App.forms import *
from django.utils import timezone


# --------------------------------------- GENERAL FUNCTIONS ------------------------------------------------------------
def createAvatars():
    try:
        for avatar_file in os.listdir("static/images/avatars/"):
            if len(Avatar.objects.filter(src="static/images/avatars/" + avatar_file)) == 0:
                Avatar.objects.create(name=avatar_file.split(".")[0], src="static/images/avatars/" + avatar_file)

    except:
        print("No se encuentra la ruta static/images/avatars")

# ---------------------------------------------- APP -------------------------------------------------------------------
def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        context = {}
        if form.is_valid():
            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])

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

                    profile = Profile.objects.create(user=user, theme=1)
                    profile.save()

                    user = authenticate(username=form.cleaned_data["username"],
                                        password=form.cleaned_data["password"])
                    if user is not None:
                        login(request, user)
                        return HttpResponseRedirect("/")

                except Exception:
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
    createAvatars()
    context = {
        "profile": Profile.objects.get(user=request.user),
        "themes": Theme.objects.all(),
        "avatars": Avatar.objects.all(),
    }
    return render(request, "app/home.html", context=context)

@login_required()
def movies(request):
    context = {
        "profile": Profile.objects.get(user=request.user),
        "themes": Theme.objects.all(),
        "avatars": Avatar.objects.all(),
    }
    return render(request, "app/movies.html", context=context)

@login_required()
def shows(request):
    context = {
        "profile": Profile.objects.get(user=request.user),
        "themes": Theme.objects.all(),
        "avatars": Avatar.objects.all(),
    }
    return render(request, "app/shows.html", context=context)

@login_required()
def social(request):
    profiles = []
    for profile in Profile.objects.all():
        if not request.user == profile.user:
            if(profile.user in Profile.objects.get(user=request.user).followings.all()):
                profiles.append({"exists": True, "profile": profile})
            else:
                profiles.append({"exists": False, "profile": profile})
    context = {
        "profile": Profile.objects.get(user=request.user),
        "themes": Theme.objects.all(),
        "avatars": Avatar.objects.all(),
        "profilesJSON": profiles,
    }
    return render(request, "app/social.html", context=context)

def changeAvatar(request):

    Profile.objects.filter(user=request.user).update(avatar=Avatar.objects.get(id=request.POST["id_avatar"]))

    data = {
        'result': "ok",
    }

    return JsonResponse(data)

def changeTheme(request, theme=None):
    Profile.objects.filter(user=request.user).update(theme=Theme.objects.get(id=theme))
    print(Theme.objects.get(id=theme))
    return HttpResponseRedirect("/")

@login_required()
def movie(request, id=None):
    context = {
        "profile": Profile.objects.get(user=request.user),
        "id": id,
        "themes": Theme.objects.all()
    }
    return render(request, "app/movie.html", context=context)

@login_required()
def show(request, id=None):
    context = {
        "profile": Profile.objects.get(user=request.user),
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
    movie = Movie.objects.filter(id_movie=request.POST["id"], user=request.user)

    if len(movie) == 0:
        movie = Movie.objects.create(id_movie=request.POST["id"], user=request.user, title=request.POST["title"],
                                     poster_path=request.POST["poster_path"], vote_average=request.POST["vote_average"])
        movie.states.add(State.objects.get(id=2))

        Activity.objects.create(user=request.user, operation=Operation.objects.get(id=1), movie=movie)

    else:
        movie.first().states.add(State.objects.get(id=2))
        Activity.objects.create(user=request.user, operation=Operation.objects.get(id=1), movie=movie.first())

    data = {
        'result': request.POST["title"] + " añadida a la lista de pendientes",
    }

    return JsonResponse(data)

def isMovieOnMyList(request):
    movie = Movie.objects.filter(id_movie=request.POST["id"], user=request.user)

    if len(movie) > 0:
        states = []
        for state in movie.first().states.all():
            states.append({"id": state.id, "state": state.name})
        data = {
            'states': states
        }
    else:
        data = {
            'states': "null",
        }

    return JsonResponse(data)

def removeMovieToSee(request):
    movie = Movie.objects.filter(id_movie=request.POST["id"], user=request.user)

    movie_title = movie.first().title

    movie.first().states.remove(State.objects.get(id=2))

    if(len(movie.first().states.all()) == 0):
        movie.delete()

    data = {
        'result': movie_title + " eliminada de mi lista de pendientes",
    }

    return JsonResponse(data)

def setMovieToSeen(request):

    movie = Movie.objects.filter(id_movie=request.POST["id"], user=request.user)

    if len(movie) == 0:
        movie = Movie.objects.create(id_movie=request.POST["id"], user=request.user, title=request.POST["title"],
                                     poster_path=request.POST["poster_path"], vote_average=request.POST["vote_average"])
        movie.states.add(State.objects.get(id=1))
        Activity.objects.create(user=request.user, operation=Operation.objects.get(id=2), movie=movie)
    else:
        movie.first().states.add(State.objects.get(id=1))
        Activity.objects.create(user=request.user, operation=Operation.objects.get(id=2), movie=movie.first())

    data = {
        'result': request.POST["title"] + " añadida a vistas",
    }

    return JsonResponse(data)

def setMovieToNotSeen(request):

    movie = Movie.objects.filter(id_movie=request.POST["id"], user=request.user)

    movie_title = movie.first().title

    movie.first().states.remove(State.objects.get(id=1))

    if(len(movie.first().states.all()) == 0):
        movie.delete()

    data = {
        'result': movie_title + " eliminada de vistas",
    }

    return JsonResponse(data)

def myMoviesToSee(request):
    movies = Movie.objects.filter(user=request.user, states__in=[2]).order_by("date_add")
    results = []

    for movie in movies:
        results.append({"id": movie.id_movie, "poster_path": movie.poster_path})

    data = {
        'results': results
    }

    return JsonResponse(data)

def myMoviesSeen(request):
    movies = Movie.objects.filter(user=request.user, states__in=[1]).order_by("date_add")
    results = []

    for movie in movies:
        results.append({"id": movie.id_movie, "poster_path": movie.poster_path})

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
        Activity.objects.create(user=request.user, operation=Operation.objects.get(id=3), show=show)
    else:
        show.first().states.add(State.objects.get(id=2))
        Activity.objects.create(user=request.user, operation=Operation.objects.get(id=3), show=show.first())

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
            'states': states
        }
    else:
        data = {
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
        show.states.add(State.objects.get(id=1))

        seasons = ast.literal_eval(request.POST["seasons"])
        for season in seasons:
            for episode in season["episodes"]:
                episode = Episode.objects.create(show=show, id_episode=episode["id"], season_number=season["season_number"],
                                                 episode_number=episode["episode_number"], user=request.user)
                episode.states.add(State.objects.get(id=1))
        Activity.objects.create(user=request.user, operation=Operation.objects.get(id=4), show=show)
    else:
        show.first().states.add(State.objects.get(id=1))
        for episode in show.first().getEpisodes():
            episode.states.add(State.objects.get(id=1))
        Activity.objects.create(user=request.user, operation=Operation.objects.get(id=4), show=show.first())
    show.update(date_update=datetime.now())

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
    shows = Show.objects.filter(user=request.user, date_update__gte=one_month_ago).exclude(states__in=[1]).order_by("date_update")

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
    shows = Show.objects.filter(user=request.user, date_update__lte=one_month_ago).exclude(states__in=[1]).order_by("date_update")

    results = []

    for show in shows:
        results.append({"id": show.id_show, "poster_path": show.poster_path})

    data = {
        'results': results
    }

    return JsonResponse(data)

# Change Episode State
def changeEpisodeState(request): # Cambiar

    show = Show.objects.filter(id_show=request.POST["id_show"], user=request.user)

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
        Episode.objects.get(id_episode=request.POST["id_episode"], user=request.user).states.add(State.objects.get(id=1))

        Activity.objects.create(user=request.user, operation=Operation.objects.get(id=5), episode=Episode.objects.get(id_episode=request.POST["id_episode"], user=request.user))

        if len(Episode.objects.filter(show=Episode.objects.get(id_episode=request.POST["id_episode"]).show, user=request.user, states__in=[1])) == len(Episode.objects.filter(show=Episode.objects.get(id_episode=request.POST["id_episode"]).show, user=request.user)):
            show.first().states.add(State.objects.get(id=1))
            Activity.objects.create(user=request.user, operation=Operation.objects.get(id=4), show=show.first())
            show.update(date_update=datetime.now())
        else:
            show.first().states.remove(State.objects.get(id=1))

        show.update(date_update=datetime.now())
        result = "Episodio marcado como visto"
    else:
        Episode.objects.get(id_episode=request.POST["id_episode"], user=request.user).states.remove(State.objects.get(id=1))
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
    episodes = Episode.objects.filter(show=Show.objects.filter(id_show=request.POST["id_show"]).first(), season_number=request.POST["season_number"], user=request.user, states__in=[1])

    results = []

    for episode in episodes:
        results.append({"id": str(episode.show.id_show) + "_" + str(episode.season_number) + "_" + str(episode.episode_number)})

    data = {
        'results': results
    }

    return JsonResponse(data)

# List of Shows seen
def myShowsSeen(request):
    shows = Show.objects.filter(user=request.user, states__in=[1]).order_by("date_update")

    results = []

    for show in shows:
        results.append({"id": show.id_show, "poster_path": show.poster_path})

    data = {
        'results': results
    }

    return JsonResponse(data)

# ---------------------------------------- ACTIVITY --------------------------------------------------------------------
# All Activity
def allActivity(request):
    activitys = Activity.objects.all().order_by("-date_add")[:150]

    results = []

    for activity in activitys:
        if (activity.operation.id == 1):
            user_str = ""
            description = ""

            if (activity.user == request.user):
                description = "Has añadido <b>" + activity.movie.title + "</b> a tu lista de pendientes"
            else:
                user_str = activity.user.username,
                description = "ha añadido <b>" + activity.movie.title + "</b> a su lista de pendientes"

            results.append({"user": user_str,
                            "description": description,
                            "href": "/movie/" + str(activity.movie.id_movie),
                            "poster_path": "https://image.tmdb.org/t/p/w300" + activity.movie.poster_path,
                            "date": activity.date_add.strftime("%m-%d-%Y %H:%M:%S")})
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
                            "poster_path": "https://image.tmdb.org/t/p/w300" + activity.movie.poster_path,
                            "date": activity.date_add.strftime("%m-%d-%Y %H:%M:%S")})
        if (activity.operation.id == 3):
            user_str = ""
            description = ""

            if (activity.user == request.user):
                description = "Has añadido <b>" + activity.show.name + "</b> a tu lista de pendientes",
            else:
                user_str = activity.user.username,
                description = "ha añadido <b>" + activity.show.name + "</b> a su lista de pendientes",

            results.append({"user": user_str,
                            "description": description,
                            "href": "/show/" + str(activity.show.id_show),
                            "poster_path": "https://image.tmdb.org/t/p/w300" + activity.show.poster_path,
                            "date": activity.date_add.strftime("%m-%d-%Y %H:%M:%S")})
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
                            "poster_path": "https://image.tmdb.org/t/p/w300" + activity.show.poster_path,
                            "date": activity.date_add.strftime("%m-%d-%Y %H:%M:%S")})
        if (activity.operation.id == 5):
            user_str = ""
            description = ""

            if (activity.user == request.user):
                description = "Has visto el <b>E" + str(activity.episode.episode_number) + "xT" + str(
                    activity.episode.season_number) + "</b> de <b>" + activity.episode.show.name + "</b>",
            else:
                user_str = activity.user.username,
                description = "ha visto el <b>E" + str(activity.episode.episode_number) + "xS" + str(
                    activity.episode.season_number) + "</b> de <b>" + activity.episode.show.name + "</b>",

            results.append({"user": user_str,
                            "description": description,
                            "href": "/show/" + str(activity.episode.show.id_show),
                            "poster_path": "https://image.tmdb.org/t/p/w300" + activity.episode.show.poster_path,
                            "date": activity.date_add.strftime("%m-%d-%Y %H:%M:%S")})
        if (activity.operation.id == 6):
            user_str = ""
            description = ""

            if (activity.user == request.user):
                description = "Has seguido a <b>" + activity.follower.username + "</b>",
            else:
                user_str = activity.user.username,
                description = "ahora sigue a <b>" + activity.follower.username + "</b>",

            results.append({"user": user_str,
                            "description": description,
                            "href": "",
                            "poster_path": Profile.objects.get(user=activity.follower).avatar.src,
                            "date": activity.date_add.strftime("%m-%d-%Y %H:%M:%S")})

    data = {
        'results': results
    }

    return JsonResponse(data)

# My Followings Activity
def myFollowingsActivity(request):
    activitys = Activity.objects.filter(user__in=Profile.objects.get(user=request.user).followings.all()).order_by("-date_add")[:150]

    results = []

    for activity in activitys:
        if (activity.operation.id == 1):
            user_str = ""
            description = ""

            if (activity.user == request.user):
                description = "Has añadido <b>" + activity.movie.title + "</b> a tu lista de pendientes"
            else:
                user_str = activity.user.username,
                description = "ha añadido <b>" + activity.movie.title + "</b> a su lista de pendientes"

            results.append({"user": user_str,
                            "description": description,
                            "href": "/movie/" + str(activity.movie.id_movie),
                            "poster_path": "https://image.tmdb.org/t/p/w300" + activity.movie.poster_path,
                            "date": activity.date_add.strftime("%m-%d-%Y %H:%M:%S")})
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
                            "poster_path": "https://image.tmdb.org/t/p/w300" + activity.movie.poster_path,
                            "date": activity.date_add.strftime("%m-%d-%Y %H:%M:%S")})
        if (activity.operation.id == 3):
            user_str = ""
            description = ""

            if (activity.user == request.user):
                description = "Has añadido <b>" + activity.show.name + "</b> a tu lista de pendientes",
            else:
                user_str = activity.user.username,
                description = "ha añadido <b>" + activity.show.name + "</b> a su lista de pendientes",

            results.append({"user": user_str,
                            "description": description,
                            "href": "/show/" + str(activity.show.id_show),
                            "poster_path": "https://image.tmdb.org/t/p/w300" + activity.show.poster_path,
                            "date": activity.date_add.strftime("%m-%d-%Y %H:%M:%S")})
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
                            "poster_path": "https://image.tmdb.org/t/p/w300" + activity.show.poster_path,
                            "date": activity.date_add.strftime("%m-%d-%Y %H:%M:%S")})
        if (activity.operation.id == 5):
            user_str = ""
            description = ""

            if (activity.user == request.user):
                description = "Has visto el <b>E" + str(activity.episode.episode_number) + "xT" + str(
                    activity.episode.season_number) + "</b> de <b>" + activity.episode.show.name + "</b>",
            else:
                user_str = activity.user.username,
                description = "ha visto el <b>E" + str(activity.episode.episode_number) + "xS" + str(
                    activity.episode.season_number) + "</b> de <b>" + activity.episode.show.name + "</b>",

            results.append({"user": user_str,
                            "description": description,
                            "href": "/show/" + str(activity.episode.show.id_show),
                            "poster_path": "https://image.tmdb.org/t/p/w300" + activity.episode.show.poster_path,
                            "date": activity.date_add.strftime("%m-%d-%Y %H:%M:%S")})
        if (activity.operation.id == 6):
            user_str = ""
            description = ""

            if (activity.user == request.user):
                description = "Has seguido a <b>" + activity.follower.username + "</b>",
            else:
                user_str = activity.user.username,
                description = "ahora sigue a <b>" + activity.follower.username + "</b>",

            results.append({"user": user_str,
                            "description": description,
                            "href": "",
                            "poster_path": Profile.objects.get(user=activity.follower).avatar.src,
                            "date": activity.date_add.strftime("%m-%d-%Y %H:%M:%S")})

    data = {
        'results': results
    }

    return JsonResponse(data)

# --------------------------------------- FOLLOWERS --------------------------------------------------------------------
def followUser(request):

    Profile.objects.get(user=request.user).followings.add(User.objects.get(id=request.POST["id_user"]))

    Activity.objects.create(user=request.user, operation=Operation.objects.get(id=6), follower=User.objects.get(id=request.POST["id_user"]))

    data = {
        'result': "ok",
    }

    return JsonResponse(data)

def unFollowUser(request):

    Profile.objects.get(user=request.user).followings.remove(User.objects.get(id=request.POST["id_user"]))

    data = {
        'result': "ok",
    }

    return JsonResponse(data)


# ---------------------------------------- SEARCH ----------------------------------------------------------------------
@login_required()
def search(request, query=None):
    context = {
        "profile": Profile.objects.get(user=request.user),
        "themes": Theme.objects.all(),
        "avatars": Avatar.objects.all(),
        "query": query
    }
    return render(request, "app/search.html", context=context)

