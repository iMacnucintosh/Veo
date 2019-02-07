/**
 * Created by mlopez on 30/01/2019.
 */
$(document).ready(function(){
    // Más Populares
    TmdbRequestFilter('#movies_popularity', "https://api.themoviedb.org/3/discover/movie", {"languaje":"es-ES", "sort_by":"popularity.desc", "without_genres": "16", "include_null_first_air_dates":"false.desc", "page":"1"}, "Peliculas Populares","movie");

    // Más Votadas
    TmdbRequestFilter('#movies_vote_count', "https://api.themoviedb.org/3/discover/movie", {"languaje":"es-ES", "sort_by":"vote_count.desc", "without_genres": "16", "include_null_first_air_dates":"false.desc", "page":"1"}, "Peliculas mejor Votadas","movie");

    // En Cines
    TmdbRequestFilter('#movies_theatres', "https://api.themoviedb.org/3/movie/now_playing", {"language":"es-ES", "page":"1"}, "Peliculas En Cartelera de Cines", "movie");

});
