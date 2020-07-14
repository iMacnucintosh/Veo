/**
 * Created by mlopez on 30/01/2019.
 */
function resizePosters(){
    var width_poster_list = (window.innerWidth - 20)
    var poster_cols = 0;

    if (window.innerWidth <= 600) {
        poster_cols = 3;
    } else if (window.innerWidth > 600 && window.innerWidth <= 992){
        poster_cols = 4;
    }else {
        poster_cols = 6;
    }

    $('.poster-item.list').css("height", ((width_poster_list/poster_cols)/0.666666666666) + "px");
}

var escalaBackdrop = 1;
var aumentando = true;

// Función que da zoom en el tiempo a la imagen de fondo de peli o serie
function zoomBackdrop(){

    if(window.innerWidth < 1000){
        if(aumentando){
            escalaBackdrop += 0.00014;
            if(escalaBackdrop >= 1.4){
                aumentando = false;
            }
        }else{
            escalaBackdrop -= 0.00014;
            if(escalaBackdrop <= 1){
                aumentando = true;
            }
        }
        $('#backdrop-image').css("transform", "scale("+escalaBackdrop+")");
    }
}


function getGenreColor(id){
    var code = "";
    switch(id){
        case 28: // Acción
            code = "#f44336";
            break;
        case 12: // Aventura
            code = "#bbb91e";
            break;
        case 16: // Animación
            code = "#96a6f5";
            break;
        case 35: // Comedia
            code = "#e2a189";
            break;
        case 80: // Crimen
            code = "#ba000d";
            break;
        case 99: // Documental
            code = "#27972a";
            break;
        case 18: // Drama
            code = "#49599a";
            break;
        case 10751: // Familia
            code = "#64b5f6";
            break;
        case 14: // Fantasía
            code = "#5e35b1";
            break;
        case 36: // Hitoria
            code = "#fdd835";
            break;
        case 27: // Terror
            code = "#333333";
            break;
        case 10402: // Música
            code = "#ff7043";
            break;
        case 9648: // Misterio
            code = "#25b091";
            break;
        case 10749: // Romance
            code = "#f06292";
            break;
        case 878: // Ciencia Ficción
            code = "#787878";
            break;
        case 10770: // Película de TV
            code = "#8b8d4b";
            break;
        case 53: // Suspense
            code = "#457957";
            break;
        case 10752: // Bélica
            code = "#da6911";
            break;
        case 37: // Western
            code = "#795548";
            break;
        // Shows
        case 10759: // Action & Adventure
            code = "#bbb91e";
            break;
        case 10762: // Kids
            code = "#9bf9ac";
            break;
        case 10764: // Reality
            code = "#793030";
            break;
        case 10765: // Sci-Fi & Fantasy"
            code = "#787878";
            break;
        case 10766: // Soap
            code = "#a2ff67";
            break;
        case 10767: // Talk
            code = "#ff7d70";
            break;
        case 10768: // War & Politics
            code = "#ff5040";
            break;
    }
    return code;
}

function showSeasonInfo(num){
    $('body').css("overflow", "hidden");
    $('#season-details-' + num).fadeIn(150);
}

function scrollPercent(){
    var total = $('body').outerHeight();
    var scroll = $(window).scrollTop() + window.innerHeight;

    var percent = (scroll/total)*100;
    return percent;
}

var page_request_movies_popularity = 1;
var page_request_movies_vote_count = 1;
var page_request_movies_now_playing = 1;

var page_request_shows_popularity = 1;
var page_request_shows_vote_count = 1;

function nextPageRequest(){
    switch(localStorage.getItem("active_tab")){
        case "#movies_popularity":
            TmdbRequestFilter('#movies_popularity', "https://api.themoviedb.org/3/discover/movie", {"language":"es-ES", "sort_by":"popularity.desc", "without_genres": "16", "include_null_first_air_dates":"false.desc", "page":page_request_movies_popularity}, "Peliculas Populares","movie", localStorage.getItem("width_poster"));
            break;
        case "#movies_vote_count":
            TmdbRequestFilter('#movies_vote_count', "https://api.themoviedb.org/3/discover/movie", {"language":"es-ES", "sort_by":"vote_count.desc", "without_genres": "16", "include_null_first_air_dates":"false.desc", "page":page_request_movies_vote_count}, "Peliculas mejor Votadas","movie", localStorage.getItem("width_poster"));
            break;
        case "#movies_theatres":
            TmdbRequestFilter('#movies_theatres', "https://api.themoviedb.org/3/movie/now_playing", {"language":"es-ES", "page":page_request_movies_now_playing}, "Peliculas En Cartelera de Cines", "movie", localStorage.getItem("width_poster"));
            break;
        case "#shows_popularity":
            TmdbRequestFilter('#shows_popularity', "https://api.themoviedb.org/3/discover/tv", {"language":"es-ES", "sort_by":"popularity.desc", "without_genres": "16", "include_null_first_air_dates":"false.desc", "page":page_request_shows_popularity}, "Series Populares", "show", localStorage.getItem("width_poster"));
            break;
        case "#shows_vote_count":
            TmdbRequestFilter('#shows_vote_count', "https://api.themoviedb.org/3/discover/tv", {"language":"es-ES", "sort_by":"vote_count.desc", "without_genres": "16", "include_null_first_air_dates":"false.desc", "page":page_request_shows_vote_count}, "Series mejor Votadas", "show", localStorage.getItem("width_poster"));
            break;
    }
}

var scroll_movies_popularity = 0;
var scroll_movies_vote_count = 0;
var scroll_movies_now_playing = 0;

var scroll_shows_popularity = 0;
var scroll_shows_vote_count = 0;

function saveScrollTab(){
    switch(localStorage.getItem("active_tab")){
        case "#movies_popularity":
            scroll_movies_popularity = $(window).scrollTop();
            break;
        case "#movies_vote_count":
            scroll_movies_vote_count = $(window).scrollTop();
            break;
        case "#movies_theatres":
            scroll_movies_now_playing = $(window).scrollTop();
            break;
        case "#shows_popularity":
            scroll_shows_popularity = $(window).scrollTop();
            break;
        case "#shows_vote_count":
            scroll_shows_vote_count = $(window).scrollTop();
            break;

    }
}

function showInfoPopup(title, overview){
    $('.info-popup-title').text(title);
    $('.info-popup-overview').text(overview);
    $('.info-popup').css("display", "flex").hide().fadeIn(100);
}

// Selecciona una lista a la que añadir una película o serie.
function selectList(elemento, type, id_list) {
    $(elemento).children().addClass('list-selected');
    $('#btnAddToList').attr("onclick", "addToList(" + type + "," + id_list + ")");
}

// Muestra un popup con la sinopsis del capitulo siguiente por ver en la página principal de TheRules
function infoEpisode(overview){
    alert(overview);
}