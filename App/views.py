# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from App.models import *
from App.forms import *

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

def addMovieToSee(request):
    movie = Movie.objects.create(id_movie=request.POST["id"], user=request.user, title=request.POST["title"], poster_path=request.POST["poster_path"])

    data = {
        'result': movie.id,
    }

    return JsonResponse(data)

def isMovieOnMyList(request):
    movie = Movie.objects.filter(id_movie=request.POST["id"], user=request.user)

    if len(movie) > 0:
        data = {
            'result': movie.first().id,
        }
    else:
        data = {
            'result': "null",
        }

    return JsonResponse(data)

def removeMovieToSee(request):
    Movie.objects.filter(id_movie=request.POST["id"], user=request.user).delete()

    data = {
        'result': "ok",
    }

    return JsonResponse(data)

def myMoviesToSee(request):
    movies = Movie.objects.filter(user=request.user, seen=False).order_by("date_add")
    results = []


    for movie in movies:
        results.append({"id": movie.id_movie, "poster_path": movie.poster_path})

    data = {
        'results': results
    }

    return JsonResponse(data)