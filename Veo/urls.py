"""Veo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  re_path(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  re_path(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  re_path(r'^blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, re_path

from App.views import (
    addMovieToSee,
    addShowToSee,
    addToList,
    changeAvatar,
    changeCelularSavings,
    changeEpisodeState,
    changeGenreColors,
    changeTheme,
    deleteFromList,
    download,
    download_torrent,
    followUser,
    home,
    isMovieOnMyList,
    isShowOnMyList,
    log_in,
    log_out,
    movie,
    movies,
    myActiveShows,
    myActivity,
    myFollowingsActivity,
    myFollowingsRecientActivity,
    myForgottenShows,
    myMoviesSeen,
    myMoviesToSee,
    myShowsPending,
    myShowsSeen,
    newList,
    notification,
    profile,
    readRecommendations,
    registerEndpoint,
    removeList,
    removeMovieToSee,
    removeShowToSee,
    save_qtorrent_settings,
    search,
    seeEpisode,
    setMovieToNotSeen,
    setMovieToSeen,
    setShowToNotSeen,
    setShowToSeen,
    shareWithFriends,
    show,
    shows,
    sign_in,
    social,
    syncronizeEpisodes,
    unFollowUser,
    unRegisterEndpoint,
    updateMediaPoster,
)


urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
    # ------------------------------------- APP --------------------------------------------------
    re_path(r"^login/$", log_in),
    re_path(r"^logout/$", log_out),
    re_path(r"^signin/$", sign_in),
    # HomePage
    re_path(r"^$", home),
    re_path(r"^seeEpisode/$", seeEpisode),
    # Movies
    re_path(r"^movies/$", movies),
    # Shows
    re_path(r"^shows/$", shows),
    # Social
    re_path(r"^social/$", social),
    re_path(r"^readRecommendations/$", readRecommendations),
    # Change Theme
    re_path(r"^changeTheme/(?P<theme>\d+)/$", changeTheme),
    # Change Celular Data Savings
    re_path(r"^changeCelularSavings/$", changeCelularSavings),
    # Movie
    re_path(r"^movie/(?P<id>\d+)/$", movie),
    # Is Movie on my List
    re_path(r"^isMovieOnMyList/$", isMovieOnMyList),
    # Show
    re_path(r"^show/(?P<id>\d+)/$", show),
    # Change Genre Colors
    re_path(r"^changeGenreColors/$", changeGenreColors),
    # ------------------------------------ MOVIE -------------------------------------------------
    # Add Movie to see
    re_path(r"^addMovieToSee/$", addMovieToSee),
    # Remove Movie to see
    re_path(r"^removeMovieToSee/$", removeMovieToSee),
    # Set Movie like seen
    re_path(r"^setMovieToSeen/$", setMovieToSeen),
    # Set Movie like not seen
    re_path(r"^setMovieToNotSeen/$", setMovieToNotSeen),
    # List of my Movies to see
    re_path(r"^myMoviesToSee/$", myMoviesToSee),
    # List of my Movies seen
    re_path(r"^myMoviesSeen/$", myMoviesSeen),
    # ----------------------------------- SHOW --------------------------------------------------
    # Add Show to see
    re_path(r"^addShowToSee/$", addShowToSee),
    # Is Show on my List
    re_path(r"^isShowOnMyList/$", isShowOnMyList),
    # Remove Show to see
    re_path(r"^removeShowToSee/$", removeShowToSee),
    # Set Show like seen
    re_path(r"^setShowToSeen/$", setShowToSeen),
    # Set Show like not seen
    re_path(r"^setShowToNotSeen/$", setShowToNotSeen),
    # List of active Shows
    re_path(r"^myActiveShows/$", myActiveShows),
    # List of Forgotten Shows
    re_path(r"^myForgottenShows/$", myForgottenShows),
    # Change State of episode
    re_path(r"^changeEpisodeState/$", changeEpisodeState),
    # Syncronize Episodes
    re_path(r"^syncronizeEpisodes/$", syncronizeEpisodes),
    # List of Seen Shows
    re_path(r"^myShowsSeen/$", myShowsSeen),
    # List of Pending Shows
    re_path(r"^myShowsPending/$", myShowsPending),
    # ------------------------------------ MEDIA -------------------------------------------------
    # Downloads
    re_path(r"^download/(?P<name>[\w\s]+)$", download),
    # Download torrent with qbittorrent
    re_path(r"^download_torrent/$", download_torrent),
    # ------------------------------------ MEDIA -------------------------------------------------
    # Update old poster_path of media after launch an error
    re_path(r"^updateMediaPoster/$", updateMediaPoster),
    # ----------------------------------- ACTIVITY -----------------------------------------------
    # List of All Activity
    re_path(r"^myActivity/$", myActivity),
    # List of My Following Activity
    re_path(r"^myFollowingsActivity/$", myFollowingsActivity),
    # List of My Following Recient Activity
    re_path(r"^myFollowingsRecientActivity/$", myFollowingsRecientActivity),
    # ---------------------------------- FOLLOWES ------------------------------------------------
    # Follow User
    re_path(r"^followUser/$", followUser),
    # UnFollow User
    re_path(r"^unFollowUser/$", unFollowUser),
    # Change Avatar
    re_path(r"^changeAvatar/$", changeAvatar),
    # ---------------------------------- SEARCH --------------------------------------------------
    # Search by query
    re_path(r"^search/(?P<query>\w+)/$", search),
    # --------------------------------- PROFILE --------------------------------------------------
    re_path(r"^profile/(?P<id>\d+)/$", profile),
    re_path(r"^newList/$", newList),
    re_path(r"^removeList/$", removeList),
    re_path(r"^addToList/$", addToList),
    re_path(r"^deleteFromList/$", deleteFromList),
    re_path(r"^list/(?P<id>\d+)/$", list),
    re_path(r"^shareWithFriends/$", shareWithFriends),
    re_path(r"^save_qtorrent_settings/$", save_qtorrent_settings),
    # --------------------------------- NOTIFICATIONS --------------------------------------------
    re_path("notification/", notification),
    re_path("registerEndpoint/", registerEndpoint),
    re_path("unRegisterEndpoint/", unRegisterEndpoint),
    re_path("webpush/", include("webpush.urls")),
]
