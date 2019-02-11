# -*- coding: utf-8 -*-
import ast
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from App.models import *
from App.forms import *
from django.utils import timezone

# --------------- APP --------------
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
    context = {
        "profile": Profile.objects.get(user=request.user),
        "themes": Theme.objects.all()
    }
    return render(request, "app/home.html", context=context)

@login_required()
def movies(request):
    context = {
        "profile": Profile.objects.get(user=request.user),
        "themes": Theme.objects.all()
    }
    return render(request, "app/movies.html", context=context)

@login_required()
def shows(request):
    context = {
        "profile": Profile.objects.get(user=request.user),
        "themes": Theme.objects.all()
    }
    return render(request, "app/shows.html", context=context)

@login_required()
def social(request):
    context = {
        "profile": Profile.objects.get(user=request.user),
        "themes": Theme.objects.all()
    }
    return render(request, "app/social.html", context=context)

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
                                     poster_path=request.POST["poster_path"])
        movie.states.add(State.objects.get(id=2))
    else:
        movie.first().states.add(State.objects.get(id=2))

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

def myMoviesToSee(request):
    movies = Movie.objects.filter(user=request.user, states__in=[2]).order_by("date_add")
    results = []

    for movie in movies:
        results.append({"id": movie.id_movie, "poster_path": movie.poster_path})

    data = {
        'results': results
    }

    return JsonResponse(data)

def setMovieToSeen(request):

    movie = Movie.objects.filter(id_movie=request.POST["id"], user=request.user)

    if len(movie) == 0:
        movie = Movie.objects.create(id_movie=request.POST["id"], user=request.user, title=request.POST["title"],
                                     poster_path=request.POST["poster_path"])
        movie.states.add(State.objects.get(id=1))
    else:
        movie.first().states.add(State.objects.get(id=1))

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


# ------------------------------------- SHOW ---------------------------------------------------------------------------
def addShowToSee(request):

    show = Show.objects.filter(id_show=request.POST["id"], user=request.user)

    if len(show) == 0:
        show = Show.objects.create(id_show=request.POST["id"], user=request.user, name=request.POST["name"],
                                   poster_path=request.POST["poster_path"])
        show.states.add(State.objects.get(id=2))

        seasons = ast.literal_eval(request.POST["seasons"])
        for season in seasons:
            for episode in season["episodes"]:
                Episode.objects.create(show=show, id_episode=episode["id"], season_number=season["season_number"],
                                       episode_number=episode["episode_number"], user=request.user)
    else:
        show.first().states.add(State.objects.get(id=2))


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

    if(len(show.first().states.all()) == 0):
        show.delete()

    data = {
        'result': show_title + " eliminada de mi lista de pendientes",
    }

    return JsonResponse(data)

def setShowToSeen(request):

    show = Show.objects.filter(id_show=request.POST["id"], user=request.user)

    if len(show) == 0:
        show = Show.objects.create(id_show=request.POST["id"], user=request.user, name=request.POST["name"],
                                   poster_path=request.POST["poster_path"])
        show.states.add(State.objects.get(id=1))

        seasons = ast.literal_eval(request.POST["seasons"])
        for season in seasons:
            for episode in season["episodes"]:
                episode = Episode.objects.create(show=show, id_episode=episode["id"], season_number=season["season_number"],
                                       episode_number=episode["episode_number"], user=request.user)
                episode.states.add(State.objects.get(id=1))
    else:
        show.first().states.add(State.objects.get(id=1))
        for episode in show.first().getEpisodes():
            episode.states.add(State.objects.get(id=1))

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

    if(len(show.first().states.all()) == 0):
        show.delete()

    data = {
        'result': show_name + " eliminada de vistas",
    }

    return JsonResponse(data)

# List of Shows in active
def myActiveShows(request):
    one_month_ago = timezone.now() - timezone.timedelta(days=30)
    shows = Show.objects.filter(user=request.user, date_update__gte=one_month_ago).order_by("date_update")

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
    shows = Show.objects.filter(user=request.user, date_update__lte=one_month_ago).order_by("date_update")

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
        show = Show.objects.create(id_show=request.POST["id"], user=request.user, name=request.POST["name"],
                                   poster_path=request.POST["poster_path"])

        seasons = ast.literal_eval(request.POST["seasons"])
        for season in seasons:
            for episode in season["episodes"]:
                Episode.objects.create(show=show, id_episode=episode["id"], season_number=season["season_number"],
                                       episode_number=episode["episode_number"], user=request.user)

    result = ""
    if request.POST["state"] == "1":

        Episode.objects.get(id_episode=request.POST["id_episode"], user=request.user).states.add(State.objects.get(id=1))
        if len(Episode.objects.filter(show=Episode.objects.get(id_episode=request.POST["id_episode"]).show, user=request.user, states__in=[1])) == len(Episode.objects.filter(show=Episode.objects.get(id_episode=request.POST["id_episode"]).show, user=request.user)):
            show.first().states.add(State.objects.get(id=1))
        else:
            show.first().states.remove(State.objects.get(id=1))
        result = "Episodio marcado como visto"
    else:
        Episode.objects.get(id_episode=request.POST["id_episode"], user=request.user).states.remove(State.objects.get(id=1))
        show.first().states.remove(State.objects.get(id=1))
        result = "Episodio marcado como no visto"

    if len(show.first().states.all()) == 0:
        show.delete()

    data = {
        'results': result
    }

    return JsonResponse(data)

# Syncronize episodes Seen
def syncronizeEpisodes(request):
    episodes = Episode.objects.filter(show=Show.objects.get(id_show=request.POST["id_show"]), season_number=request.POST["season_number"], user=request.user, states__in=[1])

    results = []

    for episode in episodes:
        results.append({"id": str(episode.show.id_show) + "_" + str(episode.season_number) + "_" + str(episode.episode_number)})

    data = {
        'results': results
    }

    return JsonResponse(data)
