/**
 * Created by mlopez on 30/01/2019.
 */
$(document).ready(function(){
    // Más Populares
    TmdbRequestFilter('#shows_popularity', "https://api.themoviedb.org/3/discover/tv", {"languaje":"es-ES", "sort_by":"popularity.desc", "without_genres": "16", "include_null_first_air_dates":"false.desc", "page":"1"}, "Series Populares", "show");

    // Más Votadas
    TmdbRequestFilter('#shows_vote_count', "https://api.themoviedb.org/3/discover/tv", {"languaje":"es-ES", "sort_by":"vote_count.desc", "without_genres": "16", "include_null_first_air_dates":"false.desc", "page":"1"}, "Series mejor Votadas", "show");

});
