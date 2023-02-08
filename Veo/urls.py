"""Veo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from App.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # ------------------------------------- APP ------------------------------------------------------------------------
    url(r'^login/$', log_in),
    url(r'^logout/$', log_out),
    url(r'^signin/$', sign_in),

    # HomePage
    url(r'^$', home),
    url(r'^seeEpisode/$', seeEpisode),

    # Movies
    url(r'^movies/$', movies),

    # Shows
    url(r'^shows/$', shows),

    # Social
    url(r'^social/$', social),
    url(r'^readRecommendations/$', readRecommendations),

    # Change Theme
    url(r'^changeTheme/(?P<theme>\d+)/$', changeTheme),

    # Change Celular Data Savings
    url(r'^changeCelularSavings/$', changeCelularSavings),

    # Movie
    url(r'^movie/(?P<id>\d+)/$', movie),

    # Is Movie on my List
    url(r'^isMovieOnMyList/$', isMovieOnMyList),

    # Show
    url(r'^show/(?P<id>\d+)/$', show),

    # Change Genre Colors
    url(r'^changeGenreColors/$', changeGenreColors),

    # ------------------------------------ MOVIE -----------------------------------------------------------------------

    # Add Movie to see
    url(r'^addMovieToSee/$', addMovieToSee),

    # Remove Movie to see
    url(r'^removeMovieToSee/$', removeMovieToSee),

    # Set Movie like seen
    url(r'^setMovieToSeen/$', setMovieToSeen),

    # Set Movie like not seen
    url(r'^setMovieToNotSeen/$', setMovieToNotSeen),

    # List of my Movies to see
    url(r'^myMoviesToSee/$', myMoviesToSee),

    # List of my Movies seen
    url(r'^myMoviesSeen/$', myMoviesSeen),

    # ----------------------------------- SHOW -------------------------------------------------------------------------

    # Add Show to see
    url(r'^addShowToSee/$', addShowToSee),

    # Is Show on my List
    url(r'^isShowOnMyList/$', isShowOnMyList),

    # Remove Show to see
    url(r'^removeShowToSee/$', removeShowToSee),

    # Set Show like seen
    url(r'^setShowToSeen/$', setShowToSeen),

    # Set Show like not seen
    url(r'^setShowToNotSeen/$', setShowToNotSeen),

    # List of active Shows
    url(r'^myActiveShows/$', myActiveShows),

    # List of Forgotten Shows
    url(r'^myForgottenShows/$', myForgottenShows),

    # Change State of episode
    url(r'^changeEpisodeState/$', changeEpisodeState),

    # Syncronize Episodes
    url(r'^syncronizeEpisodes/$', syncronizeEpisodes),

    # List of Seen Shows
    url(r'^myShowsSeen/$', myShowsSeen),

    # List of Pending Shows
    url(r'^myShowsPending/$', myShowsPending),

    # ------------------------------------ MEDIA -----------------------------------------------------------------------
    # Downloads
    url(r'^download/(?P<name>[\w\s]+)$', download),

    # Download torrent with qbittorrent
    url(r'^download_torrent/$', download_torrent),

    # ------------------------------------ MEDIA -----------------------------------------------------------------------
    # Update old poster_path of media after launch an error
    url(r'^updateMediaPoster/$', updateMediaPoster),

    # ----------------------------------- ACTIVITY ---------------------------------------------------------------------
    # List of All Activity
    url(r'^myActivity/$', myActivity),

    # List of My Following Activity
    url(r'^myFollowingsActivity/$', myFollowingsActivity),

    # List of My Following Recient Activity
    url(r'^myFollowingsRecientActivity/$', myFollowingsRecientActivity),

    # ---------------------------------- FOLLOWES ----------------------------------------------------------------------
    # Follow User
    url(r'^followUser/$', followUser),

    # UnFollow User
    url(r'^unFollowUser/$', unFollowUser),

    # Change Avatar
    url(r'^changeAvatar/$', changeAvatar),

    # ---------------------------------- SEARCH ------------------------------------------------------------------------
    # Search by query
    url(r'^search/(?P<query>\w+)/$', search),

    # --------------------------------- PROFILE ------------------------------------------------------------------------
    url(r'^profile/(?P<id>\d+)/$', profile),
    url(r'^newList/$', newList),
    url(r'^removeList/$', removeList),
    url(r'^addToList/$', addToList),
    url(r'^deleteFromList/$', deleteFromList),
    url(r'^list/(?P<id>\d+)/$', list),
    url(r'^shareWithFriends/$', shareWithFriends),
    url(r'^save_qtorrent_settings/$', save_qtorrent_settings),

    # --------------------------------- NOTIFICATIONS ------------------------------------------------------------------
    url('notification/', notification),
    url('registerEndpoint/', registerEndpoint),
    url('unRegisterEndpoint/', unRegisterEndpoint),
    url('webpush/', include('webpush.urls')),
]
