/**
 * Created by mlopez on 30/01/2019.
 */

var api_key = "f368d6c9a2c7d460dacc7cfd42809665";

// Return a list with Movies or Shows with the parameters you has specified
function TmdbRequestFilter(selector_container, url, parameters, description_request, info_for, width_poster){
    parameters["api_key"] = api_key;
    $.ajax({
        data: parameters,
        type: "GET",
        dataType: "json",
        url: url,
    }).done(function(data, textStatus, jqXHR) {
        $('.gif-loading').fadeOut(100);
        $("main").addClass("main-active");
        if(data.results.length > 0) {
            for (var i = 0; i < data.results.length; i++) {
                poster_i = data.results[i];

                var poster_str = "\
                <a href='/"+info_for+"/" + poster_i.id + "' class='"+poster_i.id+" poster-item list col s4 m3 l2 no-padding'>\
                    <img src='https://image.tmdb.org/t/p/w" + width_poster + poster_i.poster_path + "' />\
                    <i class='material-icons i-vista'>visibility</i>\
                    <i class='material-icons i-pendiente'>playlist_add_check</i>\
                 </a>\
                ";

                $(selector_container).append(poster_str);

                if(info_for=="movie") {
                    urlCheck = "/isMovieOnMyList/";
                }
                else{
                    urlCheck = "/isShowOnMyList/";
                }
                // Check if is in my list
                var dataMovie = new FormData();
                dataMovie.append('id', poster_i.id);
                $.ajax({
                    url: urlCheck,
                    type: "POST",
                    mimeType: "multipart/form-data",
                    dataType: 'json',
                    processData: false,
                    contentType: false,
                    data: dataMovie,
                    success: function (response) {
                        if (response.states != "null") {

                            for (var i = 0; i < response.states.length; i++) {
                                var state = response.states[i];

                                if (state.id == 2) {
                                    $('.' + response.id).addClass("pendiente")
                                }

                                if (state.id == 1) {
                                    $('.' + response.id).addClass("vista")
                                }

                            }

                        }
                    }
                });
            }

            if(parameters["sort_by"]){
                switch(parameters["sort_by"]){
                    case "popularity.desc":
                        page_request_movies_popularity += 1;
                        break;
                    case "vote_count.desc":
                        page_request_movies_vote_count += 1;
                        break;
                }
            }
            if(url == "https://api.themoviedb.org/3/movie/now_playing"){
                page_request_movies_now_playing +=1
            }

            allowRequest = true;
            resizePosters();

        }
    }).fail(function( jqXHR, textStatus, errorThrown ) {
        console.error('La solicitud: "' + description_request + '", a fallado: ' +  textStatus);
    });
}

// Return a specific number of random movies from your list
function Recommendations(width_poster) {
    $.ajax({
        data: {
            "api_key":api_key,
            "language": "es-ES",
            "without_genres": "16",
        },
        type: "GET",
        dataType: "json",
        url: "https://api.themoviedb.org/3/trending/movie/day",
    }).done(function(data, textStatus, jqXHR) {
        var randomIndex = Math.floor(Math.random() * 18);
        var movie = data.results[randomIndex];

        if(movie.backdrop_path != undefined && movie.poster_path != null)
        {
            var title_style = "";

            if(movie.title.length > 20){
                title_style = "font-size: 1.6em";
            }

            var recommended_movie_str = '<div class="backdrop-recommend"  style="background-image: url(https://image.tmdb.org/t/p/w500' + movie.backdrop_path + ')"></div>\
                    <a href="/movie/' + movie.id + '" class="poster-item list recommended-poster col s4 m3 l2 no-padding box-shadow">\
                        <img src="https://image.tmdb.org/t/p/w' + width_poster + movie.poster_path + '" class="shadow"/>\
                    </a>\
                    <div class="recommended-info col s8 m9 l10 offset-s4 offset-m3 offset-l2">\
                        <h1 style="'+title_style+'">' + movie.title + '</h1>\
                        <div class="circle-average">\
                            <svg viewBox="0 0 36 36" class="circular-chart">\
                                <path class="circle" stroke-dasharray="'+(movie.vote_average*10)+', 100" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />\
                            </svg>\
                            <p>'+movie.vote_average+'</p>\
                        </div>\
                    </div>';
            $("#recommended").html(recommended_movie_str);
        }else{
            Recommendations();
        }

    }).fail(function( jqXHR, textStatus, errorThrown ) {
        console.error('La solicitud: Pelicula Recomendada, a fallado: ' +  textStatus);
    });
}

var _movie;
// Get all information from Movie
function InformationMovie(id, parameters, colorGenres, csrf_token, width_poster) {

    parameters["api_key"] = api_key;

    // Basic Information
    $.ajax({
        data: parameters,
        type: "GET",
        dataType: "json",
        url: "https://api.themoviedb.org/3/movie/" + id,
    }).done(function(movie, textStatus, jqXHR) {
        _movie = movie;
        $('.gif-loading').fadeOut(100);
        $("main").addClass("main-active");
        var backdrop_path_style = "style='background-image: url(https://image.tmdb.org/t/p/w500" + movie.backdrop_path + ")'";

        if(movie.title.length >= 17 && movie.title.length <= 28){
            $('#title').css("font-size", "1.3em");
        }else if(movie.title.length > 28){
            $('#title').css("font-size", "1em");
        }

        $('title').text("Veo | " + movie.title);
        $('#title').text(movie.title);
        $('#backdrop-image').attr("style", "background-image: url(https://image.tmdb.org/t/p/w500" + movie.backdrop_path) + ")";

        localStorage.setItem("movie_poster_path", movie.poster_path);
        localStorage.setItem("movie_title", movie.title);

        $('#poster-img').attr("src", "https://image.tmdb.org/t/p/w" + width_poster + movie.poster_path);
        $('#sinopsis').text(movie.overview);
        $('#title').addClass('fadeIn');

        var date_release = new Date(movie.release_date);
        var meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];

        $('#date-release').text(date_release.getDate() + " de " + meses[date_release.getMonth()] + " del " + date_release.getFullYear());
        $('#average-count-num').text(movie.vote_average);
        $('#average-count-bar').css("width", (movie.vote_average)*10 + "%");

        // Collection
        if(movie.belongs_to_collection != null){

            var collection = movie.belongs_to_collection;
            $('#collection').addClass("collection-movie-container");
            $('#collection').append("<h3 class='title-section'>" + collection.name +"</h3>");

            // Request movie collection
            $.ajax({
                data: parameters,
                type: "GET",
                dataType: "json",
                url: "https://api.themoviedb.org/3/collection/" + collection.id
            }).done(function(collection_parts, textStatus, jqXHR) {
                var parts = collection_parts.parts;
                if(parts.length > 0){
                    parts_str = "";
                    for(var i=0; i < parts.length;i++){
                        part = parts[i];
                        if(part.poster_path != null)
                        {
                            parts_str += "\
                                <a href='/movie/" + part.id + "' class='poster-item list col s4 m3 l2 no-padding'>\
                                    <img src='https://image.tmdb.org/t/p/w" + width_poster + part.poster_path + "' />\
                                </a>\
                            ";
                        }
                    }
                }
                $('#collection').append(parts_str);
                resizePosters();

            }).fail(function( jqXHR, textStatus, errorThrown ) {
                console.error('La solicitud: Trailer de Película, a fallado: ' +  textStatus);
            });
        }

        // Genres
        var genres_str = "";
        for(var i=0; i<movie.genres.length;i++) {
            var genre = movie.genres[i];
            if(colorGenres == true) {
                var codeColor = getGenreColor(genre.id);
                genres_str += "<div class='genre' style='background-color: " + codeColor + "'>" + genre.name + "</div>";
            }else{
                genres_str += "<div class='genre'>" + genre.name + "</div>";
            }
        }
        $('#genres').append(genres_str);

    }).fail(function( jqXHR, textStatus, errorThrown ) {
        console.error('La solicitud: Información de Película, a fallado: ' +  textStatus);
    });

    // Trailer
    $.ajax({
        data: parameters,
        type: "GET",
        dataType: "json",
        url: "https://api.themoviedb.org/3/movie/" + id + "/videos"
    }).done(function(data, textStatus, jqXHR) {
        var trailer_movie = data.results;
        if(trailer_movie.length > 0){
            $('.btn-trailer').attr("href", "https://www.youtube.com/watch?v=" + trailer_movie[0].key);
            $('.btn-trailer').fadeIn(150);
        }else{
            $('.btn-trailer').hide();
        }
    }).fail(function( jqXHR, textStatus, errorThrown ) {
        console.error('La solicitud: Trailer de Película, a fallado: ' +  textStatus);
    });

    // Check if is in my list of Movies
    var data = new FormData();
    data.append('id', id);
    data.append('csrfmiddlewaretoken', csrf_token);
    $.ajax({
        url: '/isMovieOnMyList/',
        type: "POST",
        mimeType: "multipart/form-data",
        dataType: 'json',
        processData: false,
        contentType: false,
        data: data,
        success: function (response) {
            if(response.states != "null"){
                for(var i=0; i < response.states.length; i++){
                    var state = response.states[i];

                    if(state.id == 2) {
                        $('.toSee').text("playlist_add_check");
                        $('.toSee').attr("onclick", "removeMovieToSee(this, '" + csrf_token + "')");
                    }

                    if(state.id == 1){
                        $('.seen').attr("src", "/static/images/seen.png")
                        $('.seen').attr("onclick", "setMovieToNotSeen(this, '" + csrf_token +"')");
                    }

                }
            }
        }
    });

    // Cast
    $.ajax({
        data: parameters,
        type: "GET",
        dataType: "json",
        url: "http://api.themoviedb.org/3/movie/" + id + "/casts"
    }).done(function(data, textStatus, jqXHR) {
        var cast_movie = data.cast;
        var cast_movie_str = '';
        for(var i=0; i < cast_movie.length;i++){
            actor = cast_movie[i];
            if(actor.profile_path != null) {
                cast_movie_str += '\
                <a target="_blank" href="https://www.google.es/search?q=' + actor.name.replace(" ", "+") + '" class="actor">\
                    <img src="https://image.tmdb.org/t/p/w300' + actor.profile_path + '" />\
                    <div class="footer-actors"><h1>' + actor.name + '</h1><h2>(' + actor.character + ')</h2></div>\
                 </a>\
                ';
            }
        }
        $('#cast').append(cast_movie_str);
        resizePosters();

    }).fail(function( jqXHR, textStatus, errorThrown ) {
        console.error('La solicitud: Trailer de Película, a fallado: ' +  textStatus);
    });

    // Related Movies
    parameters["page"] = "1";
    $.ajax({
        data: parameters,
        type: "GET",
        dataType: "json",
        url: "https://api.themoviedb.org/3/movie/" + id + "/similar"
    }).done(function(data, textStatus, jqXHR) {
        var related_movies = data.results;
        if(related_movies.length > 0) {
            for (var i = 0; i < related_movies.length; i++) {
                poster_i = data.results[i];

                var poster_str = "\
                <a href='/movie/" + poster_i.id + "' class='poster-item list col s4 m3 l2 no-padding'>\
                    <img src='https://image.tmdb.org/t/p/w" + width_poster + poster_i.poster_path + "' />\
                 </a>\
                ";

                $('#related').append(poster_str);
            }
            resizePosters();
        }else{
            $('#related').append("<p class='infoPeticion'>No hay películas similares</p>");
        }
    }).fail(function( jqXHR, textStatus, errorThrown ) {
        console.error('La solicitud: Trailer de Película, a fallado: ' +  textStatus);
    });

    // Recommended Movies
    parameters["page"] = "1";
    $.ajax({
        data: parameters,
        type: "GET",
        dataType: "json",
        url: "https://api.themoviedb.org/3/movie/" + id + "/recommendations"
    }).done(function(data, textStatus, jqXHR) {
        var recommendations = data.results;
        if(recommendations.length > 0) {
            for (var i = 0; i < recommendations.length; i++) {
                poster_i = data.results[i];

                var poster_str = "\
                <a href='/show/" + poster_i.id + "' class='poster-item list col s4 m3 l2 no-padding'>\
                    <img src='https://image.tmdb.org/t/p/w" + width_poster + poster_i.poster_path + "' />\
                 </a>\
                ";

                $('#recommendations').append(poster_str);
            }
            resizePosters();
        }else{
            $('#recommendations').append("<p class='infoPeticion'>No hay series recomendadas</p>");
        }
    }).fail(function( jqXHR, textStatus, errorThrown ) {
        console.error('La solicitud: Trailer de Película, a fallado: ' +  textStatus);
    });

    // Images from Movie
    $.ajax({
        data: {"api_key":api_key},
        type: "GET",
        dataType: "json",
        url: "https://api.themoviedb.org/3/movie/" + id + "/images"
    }).done(function(data, textStatus, jqXHR) {
        var images = data;

        if(images.backdrops.length > 0){
            images_str = "";
            for(var i=0; i<images.backdrops.length; i++){
                var image = images.backdrops[i];
                images_str += '<div class="col s12 m4"><img class="materialboxed" src="https://image.tmdb.org/t/p/w500' + image.file_path + '" /></div>'
            }
            $('#images').append(images_str);
        }else{
            $('#images').append("<p class='infoPeticion'>No hay ninguna imagen</p>");
        }

        $('.materialboxed').materialbox();

    }).fail(function( jqXHR, textStatus, errorThrown ) {
        console.error('La solicitud: Trailer de Película, a fallado: ' +  textStatus);
    });

}

var _show;
// Get all information from Show
function InformationShow(id, parameters, colorGenres, csrf_token, width_poster) {

    parameters["api_key"] = api_key;

    // Basic Information
    $.ajax({
        data: parameters,
        type: "GET",
        dataType: "json",
        url: "https://api.themoviedb.org/3/tv/" + id,
    }).done(function(show, textStatus, jqXHR) {
        _show = show;
        $('.gif-loading').fadeOut(100);
        $("main").addClass("main-active");
        if(show.name.length >= 17 && show.name.length <= 28){
            $('#title').css("font-size", "1.3em");
        }else if(show.name.length > 28){
            $('#title').css("font-size", "1em");
        }

        $('title').text("Veo | " + show.name);
        $('#title').text(show.name);

        $('#backdrop-image').attr("style", "background-image: url(https://image.tmdb.org/t/p/w500" + show.backdrop_path) + ")";
        $('#poster-img').attr("src", "https://image.tmdb.org/t/p/w" + width_poster + show.poster_path);
        $('#sinopsis').text(show.overview);
        $('#title').addClass('fadeIn');

        var date_release = new Date(show.first_air_date);
        var meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];

        $('#date-release').text(date_release.getDate() + " de " + meses[date_release.getMonth()] + " del " + date_release.getFullYear());

        $('#average-count-num').text(show.vote_average);
        $('#average-count-bar').css("width", (show.vote_average)*10 + "%");

        // Genres
        var genres_str = "";
        for(var i=0; i<show.genres.length;i++) {
            var genre = show.genres[i];
            if(colorGenres == true) {
                var codeColor = getGenreColor(genre.id);
                genres_str += "<div class='genre' style='background-color: " + codeColor + "'>" + genre.name + "</div>";
            }else{
                genres_str += "<div class='genre'>" + genre.name + "</div>";
            }
        }
        $('#genres').append(genres_str);

        var seasons_str = '';
        for(var i=0; i<show.seasons.length; i++){
            var season = show.seasons[i];
            if(season.poster_path != null) {
                seasons_str += '<div class="season-poster poster-item list col s4 m3 l2 no-padding" onclick="showSeasonInfo(' + season.season_number + ')">\
                    <img src="https://image.tmdb.org/t/p/w' + width_poster + season.poster_path + '">\
                    </div>';

                // Information for each season
                InformationSeason(id, season.season_number, parameters, csrf_token, width_poster);
            }
        }

        $('#seasons-posters-list').append(seasons_str);

        resizePosters();

        // Last episode Air

        var d_last_episode = new Date(show.last_episode_to_air.air_date);
        var meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];

        var date_last_episode = d_last_episode.getDate() + " de " + meses[d_last_episode.getMonth()] + " del " + d_last_episode.getFullYear();

        var overview = show.last_episode_to_air.overview;
        if(overview == ""){
            overview = "No hay ninguna descripción disponible";
        }
        var last_episode_str = '\
            <ul class="collapsible">\
                <li>\
                    <div class="collapsible-header"><i class="material-icons">update</i>' + show.last_episode_to_air.name + '<span class="last-episode-span">(Último Episodio)</span></div>\
                    <div class="collapsible-body row no-margin"><p class="date-last-episode col s6">' + date_last_episode + '</p><p class="col s6 last-episode-number">T' + show.last_episode_to_air.season_number + ' x E' + show.last_episode_to_air.episode_number+ '</p><p class="col s12 last-episode-overview">' + overview + '</p></div>\
                </li>\
            </ul>';
        $('#last-episode-air').append(last_episode_str);

    }).fail(function( jqXHR, textStatus, errorThrown ) {
        console.error('La solicitud: Información de Serie, a fallado: ' +  textStatus);
    });

    // Trailer
    $.ajax({
        data: parameters,
        type: "GET",
        dataType: "json",
        url: "https://api.themoviedb.org/3/tv/" + id + "/videos"
    }).done(function(trailes_data, textStatus, jqXHR) {
        var trailer_movie = trailes_data.results;
        if(trailer_movie.length > 0){
            $('.btn-trailer').attr("href", "https://www.youtube.com/watch?v=" + trailer_movie[0].key);
            $('.btn-trailer').fadeIn(150);
        }else{
            $('.btn-trailer').hide();
        }


    }).fail(function( jqXHR, textStatus, errorThrown ) {
        console.error('La solicitud: Trailer de Película, a fallado: ' +  textStatus);
    });


    // Check if is in my list of Shows
    var data = new FormData();
    data.append('id', id);
    data.append('csrfmiddlewaretoken', csrf_token);
    $.ajax({
        url: '/isShowOnMyList/',
        type: "POST",
        mimeType: "multipart/form-data",
        dataType: 'json',
        processData: false,
        contentType: false,
        data: data,
        success: function (response) {
            if(response.states != "null"){
                for(var i=0; i < response.states.length; i++){
                    var state = response.states[i];

                    if(state.id == 2) {
                        $('.toSee').text("playlist_add_check");
                        $('.toSee').attr("onclick", "removeShowToSee(this, '" + csrf_token + "')");
                    }

                    if(state.id == 1){
                        $('.seen').attr("src", "/static/images/seen.png")
                        $('.seen').attr("onclick", "setShowToNotSeen(this, '" + csrf_token +"')");
                    }

                }
            }
        }
    });

    // Related Shows
    parameters["page"] = "1";
    $.ajax({
        data: parameters,
        type: "GET",
        dataType: "json",
        url: "https://api.themoviedb.org/3/tv/" + id + "/similar"
    }).done(function(data, textStatus, jqXHR) {
        var related_shows = data.results;
        if(related_shows.length > 0) {
            for (var i = 0; i < related_shows.length; i++) {
                poster_i = data.results[i];

                var poster_str = "\
                <a href='/show/" + poster_i.id + "' class='poster-item list col s4 m3 l2 no-padding'>\
                    <img src='https://image.tmdb.org/t/p/w" + width_poster + poster_i.poster_path + "' />\
                 </a>\
                ";

                $('#related').append(poster_str);
            }
            resizePosters();
        }else{
            $('#related').append("<p class='infoPeticion'>No hay series similares</p>");
        }
    }).fail(function( jqXHR, textStatus, errorThrown ) {
        console.error('La solicitud: Trailer de Película, a fallado: ' +  textStatus);
    });

    // Recommended Shows
    parameters["page"] = "1";
    $.ajax({
        data: parameters,
        type: "GET",
        dataType: "json",
        url: "https://api.themoviedb.org/3/tv/" + id + "/recommendations"
    }).done(function(data, textStatus, jqXHR) {
        var recommendations = data.results;
        if(recommendations.length > 0) {
            for (var i = 0; i < recommendations.length; i++) {
                poster_i = data.results[i];

                var poster_str = "\
                <a href='/show/" + poster_i.id + "' class='poster-item list col s4 m3 l2 no-padding'>\
                    <img src='https://image.tmdb.org/t/p/w" + width_poster + poster_i.poster_path + "' />\
                 </a>\
                ";

                $('#recommendations').append(poster_str);
            }
            resizePosters();
        }else{
            $('#recommendations').append("<p class='infoPeticion'>No hay series recomendadas</p>");
        }
    }).fail(function( jqXHR, textStatus, errorThrown ) {
        console.error('La solicitud: Trailer de Película, a fallado: ' +  textStatus);
    });

    // Images from Show
    $.ajax({
        data: {"api_key":api_key},
        type: "GET",
        dataType: "json",
        url: "https://api.themoviedb.org/3/tv/" + id + "/images"
    }).done(function(data, textStatus, jqXHR) {
        var images = data;

        if(images.backdrops.length > 0){
            images_str = "";
            for(var i=0; i<images.backdrops.length; i++){
                var image = images.backdrops[i];
                images_str += '<div class="col s12 m4"><img class="materialboxed" src="https://image.tmdb.org/t/p/w500' + image.file_path + '" /></div>'
            }
            $('#images').append(images_str);
        }else{
            $('#images').append("<p class='infoPeticion'>No hay ninguna imagen</p>");
        }

        $('.materialboxed').materialbox();

    }).fail(function( jqXHR, textStatus, errorThrown ) {
        console.error('La solicitud: Trailer de Película, a fallado: ' +  textStatus);
    });

}

var _seasons = [];
function InformationSeason(id_show, num_season, parameters, csrf_token, width_poster){
    parameters["api_key"] = api_key;

    // Basic Information
    $.ajax({
        data: parameters,
        type: "GET",
        dataType: "json",
        url: "https://api.themoviedb.org/3/tv/" + id_show + "/season/" + num_season,
    }).done(function(season_info, textStatus, jqXHR) {

        episodes = []

        for (var i=0; i<season_info.episodes.length; i++){
            episodes.push({"id": season_info.episodes[i].id, "episode_number":season_info.episodes[i].episode_number})
        }

        season_JSON = {"season_number": season_info.season_number, episodes:episodes};

        _seasons.push(season_JSON)

        /* Información de cada temporada */
        var season_date_str = season_info.air_date;

        var season_date = new Date(season_date_str);
        var meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];

        var season_date_format = season_date.getDate() + " " + meses[season_date.getMonth()] + " " + season_date.getFullYear();

        var season_info_str = '<div id="season-details-'+ num_season + '" class="season-details">\
         <div class="header-season row col s12">\
            <div class="close-season-details">\
                <i class="material-icons">close</i>\
            </div>\
            <div class="col s4 m2 no-padding">\
                <img class="season-poster shadow" src="https://image.tmdb.org/t/p/w' + width_poster + season_info.poster_path + '">\
                <h3 class="date-season">' + season_date_format + '</h3>\
                <p class="num-episodes-season" id="num-episodes-season-'+num_season+'">' + season_info.episodes.length + ' Episodios</p>\
            </div>\
            <div class="season-info col s8 m10">\
                 <h5 class="col s12">' + season_info.name + '</h5>\
                 <div class="season-overview col s12">';

        if(season_info.overview != ""){
            season_info_str += season_info.overview + '</div>';
        }else{
            season_info_str += 'Ninguna descripción disponible</div>';
        }

        season_info_str += '</div>\
         </div>\
         <div class="col s12 season-episodes no-padding">\
            <ul class="collapsible no-margin">\
         ';

        // Collapsible for each episode
        for(var i=0; i<season_info.episodes.length; i++){
            var episode = season_info.episodes[i];
            var overview = episode.overview;
            if(overview == ""){
                overview = "No hay ninguna descripción disponible";
            }
            season_info_str += '\
                        <li>\
                            <div class="collapsible-header"><i class="material-icons" onclick="changeStateEpisode(this,' + id_show + ',' + num_season + ',' + episode.id + ',\''+ csrf_token +'\')" id="' + id_show + '_' + num_season + '_' + episode.episode_number + '">radio_button_unchecked</i>' + episode.name + '</div>\                            <div class="collapsible-body row no-margin"><p class="date-last-episode col s6">' + episode.air_date + '</p><p class="col s6 last-episode-number">T' + episode.season_number + ' x E' + episode.episode_number+ '</p><p class="col s12 last-episode-overview">' + overview + '</p></div>\
                        </li>'
        }
        season_info_str += '</ul></div></div>';

        $('#seasons').append(season_info_str);

        $('.collapsible').collapsible();

        $('.season-episodes .collapsible-header i').click(function(e) {
            e.stopPropagation();
        });

        $('.close-season-details').click(function(){
            $('body').css("overflow", "auto");
            $(this).parent().parent().fadeOut(150);
        });


        // Syncronize episodes seen
        var data = new FormData();
        data.append('id_show', id_show);
        data.append('season_number', num_season);
        data.append('csrfmiddlewaretoken', csrf_token);
        $.ajax({
            url: '/syncronizeEpisodes/',
            type: "POST",
            mimeType: "multipart/form-data",
            dataType: 'json',
            processData: false,
            contentType: false,
            data: data,
            success: function (response) {
                if(response.results.length > 0){
                    $('#num-episodes-season-' + num_season).text(response.results.length + "/" + $('#num-episodes-season-' + num_season).text())
                    for(var i=0; i<response.results.length; i++){
                        $('#' + response.results[i].id).text("radio_button_checked")
                    }
                }
            }
        });



    }).fail(function( jqXHR, textStatus, errorThrown ) {
        console.error('La solicitud: Información de la Temporada, a fallado: ' +  textStatus);
        $('#season-details-' + num_season).remove();
        $(".season-poster[onclick='showSeasonInfo(" + num_season + ")']").remove();
    });

}

/* ------------------------------ MOVIE ----------------------------------------------------------------------------- */
// Add a movie to list of pending movies
function addMovieToSee(elemento, csrf_token){
    var data = new FormData();
    data.append('id', _movie.id);
    data.append('title', _movie.title);
    data.append('poster_path',  _movie.poster_path);
    data.append('vote_average',  _movie.vote_average);
    data.append('csrfmiddlewaretoken', csrf_token);
    $.ajax({
        url: '/addMovieToSee/',
        type: "POST",
        mimeType: "multipart/form-data",
        dataType: 'json',
        processData: false,
        contentType: false,
        data: data,
        success: function (response) {
            M.toast({html: 'Has añadido ' + $('#title').text() + " a tu lista de pendientes"})
            $(elemento).text("playlist_add_check");
            $(elemento).attr("onclick", "removeMovieToSee(this, '" + csrf_token +"')");

        }
    });
}

// Remove a movie to list of pending movies
function removeMovieToSee(elemento, csrf_token){

    var data = new FormData();
    data.append('id', _movie.id);
    data.append('csrfmiddlewaretoken', csrf_token);
    $.ajax({
        url: '/removeMovieToSee/',
        type: "POST",
        mimeType: "multipart/form-data",
        dataType: 'json',
        processData: false,
        contentType: false,
        data: data,
        success: function (response) {
            M.toast({html: 'Has eliminado ' + $('#title').text() + " de tu lista de pendientes"})
            $(elemento).text("playlist_add")
            $(elemento).attr("onclick", "addMovieToSee(this, '" + csrf_token +"')");
        }
    });
}

// Set a movie like seen
function setMovieToSeen(elemento, csrf_token){

    var data = new FormData();
    data.append('id', _movie.id);
    data.append('title', _movie.title);
    data.append('poster_path', _movie.poster_path);
    data.append('vote_average',  _movie.vote_average);
    data.append('csrfmiddlewaretoken', csrf_token);
    $.ajax({
        url: '/setMovieToSeen/',
        type: "POST",
        mimeType: "multipart/form-data",
        dataType: 'json',
        processData: false,
        contentType: false,
        data: data,
        success: function (response) {
            M.toast({html: 'Has marcado ' + $('#title').text() + " como vista"})
            $(elemento).attr("src", "/static/images/seen.png")
            $(elemento).attr("onclick", "setMovieToNotSeen(this, '" + csrf_token +"')");

        }
    });
}

// Set a movie like not seen
function setMovieToNotSeen(elemento, csrf_token){
    var data = new FormData();
    data.append('id', _movie.id);
    data.append('csrfmiddlewaretoken', csrf_token);
    $.ajax({
        url: '/setMovieToNotSeen/',
        type: "POST",
        mimeType: "multipart/form-data",
        dataType: 'json',
        processData: false,
        contentType: false,
        data: data,
        success: function (response) {
            M.toast({html: 'Has eliminado ' + $('#title').text() + " como vista"})
            $(elemento).attr("src", "/static/images/not_seen.png")
            $(elemento).attr("onclick", "setMovieToSeen(this, '" + csrf_token +"')");
        }
    });
}

function MyMoviesToSee(csrf_token, selector, width_poster){
    var data = new FormData();
    data.append('csrfmiddlewaretoken', csrf_token);
    $.ajax({
        url: '/myMoviesToSee/',
        type: "POST",
        mimeType: "multipart/form-data",
        dataType: 'json',
        processData: false,
        contentType: false,
        data: data,
        success: function (data) {
            $('.gif-loading').fadeOut(100);
            $("main").addClass("main-active");
            if(data.results.length > 0) {
                for (var i = 0; i < data.results.length; i++) {
                    poster_i = data.results[i];

                    var poster_str = "\
                <a href='/movie/" + poster_i.id + "' class='poster-item list col s4 m3 l2 no-padding'>\
                    <img src='https://image.tmdb.org/t/p/w" + width_poster + poster_i.poster_path + "' />\
                 </a>\
                ";
                    $(selector).append(poster_str);
                }
                resizePosters();
            }else{
                $(selector).append("<p class='infoPeticion'>Aún no has añadido ninguna película a tu lista</p>");
            }

        }
    });
}

function MyMoviesSeen(csrf_token, selector, width_poster){
    var data = new FormData();
    data.append('csrfmiddlewaretoken', csrf_token);
    $.ajax({
        url: '/myMoviesSeen/',
        type: "POST",
        mimeType: "multipart/form-data",
        dataType: 'json',
        processData: false,
        contentType: false,
        data: data,
        success: function (data) {
            $('.gif-loading').fadeOut(100);
            $("main").addClass("main-active");
            if(data.results.length > 0) {
                for (var i = 0; i < data.results.length; i++) {
                    poster_i = data.results[i];

                    var poster_str = "\
                <a href='/movie/" + poster_i.id + "' class='poster-item list col s4 m3 l2 no-padding'>\
                    <img src='https://image.tmdb.org/t/p/w" + width_poster + poster_i.poster_path + "' />\
                 </a>\
                ";
                    $(selector).append(poster_str);
                }
                resizePosters();
            }else{
                $(selector).append("<p class='infoPeticion'>Aún no has visto ninguna película</p>");
            }

        }
    });
}

/* --------------------------------- SHOW --------------------------------------------------------------------------- */
// Add a show to list of pending shows
function addShowToSee(elemento, csrf_token){
    var data = new FormData();
    data.append('id', _show.id);
    data.append('name', _show.name);
    data.append('poster_path', _show.poster_path);
    data.append('vote_average',  _show.vote_average);
    data.append('seasons', JSON.stringify(_seasons));
    data.append('csrfmiddlewaretoken', csrf_token);
    $.ajax({
        url: '/addShowToSee/',
        type: "POST",
        mimeType: "multipart/form-data",
        dataType: 'json',
        processData: false,
        contentType: false,
        data: data,
        success: function (response) {
            M.toast({html: 'Has añadido ' + $('#title').text() + " a tu lista de pendientes"})
            $(elemento).text("playlist_add_check");
            $(elemento).attr("onclick", "removeShowToSee(this, '" + csrf_token +"')");

        }
    });
}

// Remove a show to list of pending shows
function removeShowToSee(elemento, csrf_token){

    var data = new FormData();
    data.append('id', _show.id);
    data.append('csrfmiddlewaretoken', csrf_token);
    $.ajax({
        url: '/removeShowToSee/',
        type: "POST",
        mimeType: "multipart/form-data",
        dataType: 'json',
        processData: false,
        contentType: false,
        data: data,
        success: function (response) {
            M.toast({html: 'Has eliminado ' + $('#title').text() + " de tu lista de pendientes"})
            $(elemento).text("playlist_add")
            $(elemento).attr("onclick", "addShowToSee(this, '" + csrf_token +"')");
        }
    });
}

// Set a movie like seen
function setShowToSeen(elemento, csrf_token){
    var data = new FormData();
    data.append('id', _show.id);
    data.append('name', _show.name);
    data.append('poster_path', _show.poster_path);
    data.append('vote_average',  _show.vote_average);
    data.append('seasons', JSON.stringify(_seasons));
    data.append('csrfmiddlewaretoken', csrf_token);
    $.ajax({
        url: '/setShowToSeen/',
        type: "POST",
        mimeType: "multipart/form-data",
        dataType: 'json',
        processData: false,
        contentType: false,
        data: data,
        success: function (response) {
            M.toast({html: 'Has marcado ' + $('#title').text() + " como vista"})
            $(elemento).attr("src", "/static/images/seen.png")
            $(elemento).attr("onclick", "setShowToNotSeen(this, '" + csrf_token +"')");
            $('.season-episodes i').text("radio_button_checked")
        }
    });
}

// Set a movie like not seen
function setShowToNotSeen(elemento, csrf_token){
    var data = new FormData();
    data.append('id', _show.id);
    data.append('csrfmiddlewaretoken', csrf_token);
    $.ajax({
        url: '/setShowToNotSeen/',
        type: "POST",
        mimeType: "multipart/form-data",
        dataType: 'json',
        processData: false,
        contentType: false,
        data: data,
        success: function (response) {
            M.toast({html: 'Has eliminado ' + $('#title').text() + " como vista"})
            $(elemento).attr("src", "/static/images/not_seen.png")
            $(elemento).attr("onclick", "setShowToSeen(this, '" + csrf_token +"')");
            $('.season-episodes i').text("radio_button_unchecked")
        }
    });
}

// List of Active Shows
function MyActiveShows(csrf_token, selector, width_poster){
    var data = new FormData();
    data.append('csrfmiddlewaretoken', csrf_token);
    $.ajax({
        url: '/myActiveShows/',
        type: "POST",
        mimeType: "multipart/form-data",
        dataType: 'json',
        processData: false,
        contentType: false,
        data: data,
        success: function (data) {
            $('.gif-loading').fadeOut(100);
            $("main").addClass("main-active");
            if(data.results.length > 0) {
                for (var i = 0; i < data.results.length; i++) {
                    poster_i = data.results[i];
                    var poster_str = "\
                        <a href='/show/" + poster_i.id + "' class='poster-item list col s4 m3 l2 no-padding'>\
                            <img src='https://image.tmdb.org/t/p/w"+ width_poster + poster_i.poster_path + "' />\
                         </a>\
                        ";
                    $(selector).append(poster_str);
                }
                resizePosters();
            }else{
                $(selector).append("<p class='infoPeticion'>Aún no has añadido ninguna serie a tu lista</p>");
            }

        }
    });
}

// List of Forgotten
function MyForgottenShows(csrf_token, selector, width_poster){
    var data = new FormData();
    data.append('csrfmiddlewaretoken', csrf_token);
    $.ajax({
        url: '/myForgottenShows/',
        type: "POST",
        mimeType: "multipart/form-data",
        dataType: 'json',
        processData: false,
        contentType: false,
        data: data,
        success: function (data) {
            $('.gif-loading').fadeOut(100);
            $("main").addClass("main-active");
            if(data.results.length > 0) {
                for (var i = 0; i < data.results.length; i++) {
                    poster_i = data.results[i];
                    var poster_str = "\
                        <a href='/show/" + poster_i.id + "' class='poster-item list col s4 m3 l2 no-padding'>\
                            <img src='https://image.tmdb.org/t/p/w" + width_poster + poster_i.poster_path + "' />\
                         </a>\
                        ";
                    $(selector).append(poster_str);
                }
                resizePosters();
            }else{
                $(selector).append("<p class='infoPeticion'>No tienes ninguna serie en el olvido</p>");
            }
        }
    });
}

// Check/Uncheck episode like seen
function changeStateEpisode(elemento, id_show, num_season, id_episode, csrf_token){
    var state;

    var current_txt =  $('#num-episodes-season-' + num_season).text();
    var episodes_count = "";
    var episodes_seen = 0;

    if(current_txt.indexOf("/") != -1){
        episodes_current = parseInt(current_txt.split("/")[0]);
        episodes_count = current_txt.split("/")[1];
    }else{
        episodes_seen = 0;
        episodes_current = 0;
        episodes_count = current_txt;
    }

    // Comprobamos si se va a marcar o desmarcar como visto
    if($(elemento).text() == "radio_button_unchecked"){
        state = 1;
        M.toast({html: 'Marcando como Visto...'});
    } else{
        state = 2;
        M.toast({html: 'Desmarcando como Visto...'});

    }

    // Petición para cambiar el estado de visualización del capitulo
    var data = new FormData();
    data.append('id_show', id_show);
    data.append('name', _show.name);
    data.append('poster_path', _show.poster_path);
    data.append('id_episode', id_episode);
    data.append('state', state);
    data.append('seasons', JSON.stringify(_seasons));
    data.append('csrfmiddlewaretoken', csrf_token);
    $.ajax({
        url: '/changeEpisodeState/',
        type: "POST",
        mimeType: "multipart/form-data",
        dataType: 'json',
        processData: false,
        contentType: false,
        data: data,
        success: function (data) {
            M.Toast.dismissAll();
            if(state==1){
                episodes_seen = episodes_current + 1;
                $('#num-episodes-season-' + num_season).text(episodes_seen + "/" + episodes_count)
                $(elemento).text("radio_button_checked");
            }else{
                episodes_seen = episodes_current - 1;

                if(episodes_seen <= 0){
                    $('#num-episodes-season-' + num_season).text(episodes_count)
                }else{
                    $('#num-episodes-season-' + num_season).text(episodes_seen + "/" + episodes_count)
                }

                $(elemento).text("radio_button_unchecked");
            }

            all_seen = true;
            num_seen = 0;
            // Si todos los episodios estan marcados establecemos la serie como vista
            $('.season-episodes i').each(function(){
                if($(this).text() == "radio_button_unchecked"){
                    all_seen = false;
                }else{
                    num_seen += 1;
                }
            });

            if(all_seen){
                M.toast({html: 'Acabas de ver todos los capitulos de esta serie'});
                $('.seen').attr("src", "/static/images/seen.png")
                $('.seen').attr("onclick", "setShowToNotSeen(this, '" + csrf_token +"')");

            }else{
                if((num_seen + 1) ==  $('.season-episodes i').length){
                    M.toast({html: 'Te queda un capitulo para terminar la serie'});
                }

                $('.seen').attr("src", "/static/images/not_seen.png")
                $('.seen').attr("onclick", "setShowToSeen(this, '" + csrf_token +"')");
            }
        }
    });


}

// List of Seen Shows
function MyShowsSeen(csrf_token, selector, width_poster){
    var data = new FormData();
    data.append('csrfmiddlewaretoken', csrf_token);
    $.ajax({
        url: '/myShowsSeen/',
        type: "POST",
        mimeType: "multipart/form-data",
        dataType: 'json',
        processData: false,
        contentType: false,
        data: data,
        success: function (data) {
            $('.gif-loading').fadeOut(100);
            $("main").addClass("main-active");
            if(data.results.length > 0) {
                for (var i = 0; i < data.results.length; i++) {
                    poster_i = data.results[i];
                    var poster_str = "\
                        <a href='/show/" + poster_i.id + "' class='poster-item list col s4 m3 l2 no-padding'>\
                            <img src='https://image.tmdb.org/t/p/w" + width_poster + poster_i.poster_path + "' />\
                         </a>\
                        ";
                    $(selector).append(poster_str);
                }
                resizePosters();
            }else{
                $(selector).append("<p class='infoPeticion'>Aún no has visto ninguna serie</p>");
            }

        }
    });
}

// List of All Activity
function AllActivity(csrf_token, selector){
    var data = new FormData();
    data.append('csrfmiddlewaretoken', csrf_token);
    $.ajax({
        url: '/allActivity/',
        type: "POST",
        mimeType: "multipart/form-data",
        dataType: 'json',
        processData: false,
        contentType: false,
        data: data,
        success: function (data) {
            $('.gif-loading').fadeOut(100);
            $("main").addClass("main-active");

            if(data.results.length > 0) {
                for (var i = 0; i < data.results.length; i++) {
                    activity_i = data.results[i];
                    var activity_str = '<div class="activity-item row">\
                                            <a href="'+activity_i.href+'" class="poster-activity">\
                                                <img src="'+activity_i.poster_path+'" />\
                                            </a>\
                                            <div class="information-activity">\
                                                <div class="col s12 date-activity no-padding">\
                                                    <p>'+activity_i.date+'</p>\
                                                </div>\
                                                <div class="col s12 description-activity no-padding">\
                                                    <p><b class="username-activity">'+activity_i.user+'</b> '+activity_i.description+'</p>\
                                                </div>\
                                            </div>\
                                        </div>';
                    $(selector).append(activity_str);
                }
            }else{
                $(selector).append("<p class='infoPeticion'>Aún no hay actividad</p>");
            }

        }
    });
}

// List of Following Activity
function MyFollowingsActivity(csrf_token, selector){
    var data = new FormData();
    data.append('csrfmiddlewaretoken', csrf_token);
    $.ajax({
        url: '/myFollowingsActivity/',
        type: "POST",
        mimeType: "multipart/form-data",
        dataType: 'json',
        processData: false,
        contentType: false,
        data: data,
        success: function (data) {
            $('.gif-loading').fadeOut(100);
            $("main").addClass("main-active");

            if(data.results.length > 0) {
                for (var i = 0; i < data.results.length; i++) {
                    activity_i = data.results[i];
                    var activity_str = '<div class="activity-item row">\
                                           <a href="'+activity_i.href+'" class="poster-activity">\
                                                <img src="'+activity_i.poster_path+'" />\
                                            </a>\
                                            <div class="information-activity">\
                                                <div class="col s12 date-activity no-padding">\
                                                    <p>'+activity_i.date+'</p>\
                                                </div>\
                                                <div class="col s12 description-activity no-padding">\
                                                    <p><b class="username-activity">'+activity_i.user+'</b> '+activity_i.description+'</p>\
                                                </div>\
                                            </div>\
                                        </div>';
                    $(selector).append(activity_str);
                }
            }else{
                $(selector).append("<p class='infoPeticion'>Aún no hay actividad</p>");
            }


        }
    });
}

// List of Following Activity
function MyFollowingsRecientActivity(csrf_token, selector){
    var data = new FormData();
    data.append('csrfmiddlewaretoken', csrf_token);
    $.ajax({
        url: '/myFollowingsRecientActivity/',
        type: "POST",
        mimeType: "multipart/form-data",
        dataType: 'json',
        processData: false,
        contentType: false,
        data: data,
        success: function (data) {
            $('.gif-loading').fadeOut(100);
            $("main").addClass("main-active");

            if(data.results.length > 0) {
                for (var i = 0; i < data.results.length; i++) {
                    activity_i = data.results[i];
                    var activity_str = '<div class="activity-item row">\
                                           <a href="'+activity_i.href+'" class="poster-activity">\
                                                <img src="'+activity_i.poster_path+'" />\
                                            </a>\
                                            <div class="information-activity">\
                                                <div class="col s12 date-activity no-padding">\
                                                    <p>'+activity_i.date+'</p>\
                                                </div>\
                                                <div class="col s12 description-activity no-padding">\
                                                    <p><b class="username-activity">'+activity_i.user+'</b> '+activity_i.description+'</p>\
                                                </div>\
                                            </div>\
                                        </div>';
                    $(selector).append(activity_str);
                }
            }else{
                $(selector).append("<p class='infoPeticion'>Aún no hay actividad</p>");
            }


        }
    });
}


// Follow user
function FollowUser(elemento, id_user, csrf_token){
    var data = new FormData();
    data.append('id_user', id_user);
    data.append('csrfmiddlewaretoken', csrf_token);
    $.ajax({
        url: '/followUser/',
        type: "POST",
        mimeType: "multipart/form-data",
        dataType: 'json',
        processData: false,
        contentType: false,
        data: data,
        success: function (data) {
            $(elemento).attr("onclick", "UnFollowUser(this, "+id_user+", '"+csrf_token+"')");
            $(elemento).addClass("red");
            $(elemento).html("No Seguir");
        }
    });
}

// UnFollow user
function UnFollowUser(elemento, id_user, csrf_token){
    var data = new FormData();
    data.append('id_user', id_user);
    data.append('csrfmiddlewaretoken', csrf_token);
    $.ajax({
        url: '/unFollowUser/',
        type: "POST",
        mimeType: "multipart/form-data",
        dataType: 'json',
        processData: false,
        contentType: false,
        data: data,
        success: function (data) {
            $(elemento).attr("onclick", "FollowUser(this, "+id_user+", '"+csrf_token+"')");
            $(elemento).removeClass("red");
            $(elemento).text("Seguir");
        }
    });
}

function changeColorGenres(toogle, csrf_token) {

    var status = $(toogle).is(':checked');

    var data = new FormData();
    data.append('status', status);
    data.append('csrfmiddlewaretoken', csrf_token);
    $.ajax({
        url: '/changeGenreColors/',
        type: "POST",
        mimeType: "multipart/form-data",
        dataType: 'json',
        processData: false,
        contentType: false,
        data: data,
        success: function (response) {

        }
    });
}

// Change Avatar of user
function changeAvatar(elemento, id_avatar, csrf_token){
    var data = new FormData();
    data.append('id_avatar', id_avatar);
    data.append('csrfmiddlewaretoken', csrf_token);
    $.ajax({
        url: '/changeAvatar/',
        type: "POST",
        mimeType: "multipart/form-data",
        dataType: 'json',
        processData: false,
        contentType: false,
        data: data,
        success: function (data) {
            location.reload();
        }
    });
}

// Change Avatar of user
function changeCelularDataSavings(toogle, csrf_token){

    var status = $(toogle).is(':checked');

    var data = new FormData();
    data.append('status', status);
    data.append('csrfmiddlewaretoken', csrf_token);
    $.ajax({
        url: '/changeCelularSavings/',
        type: "POST",
        mimeType: "multipart/form-data",
        dataType: 'json',
        processData: false,
        contentType: false,
        data: data,
        success: function (response) {
            location.reload();
        }
    });
}

// Search Movies, Shows or Actors
// Return a list with Movies or Shows with the parameters you has specified
function Search(query, width_poster){
    $.ajax({
        type: "GET",
        dataType: "json",
        url: "https://api.themoviedb.org/3/search/multi?api_key=f368d6c9a2c7d460dacc7cfd42809665&language=es-ES&query=" + query.replace(/_/g, "%20") + "&page=1&include_adult=false",
    }).done(function(data, textStatus, jqXHR) {
        $('.gif-loading').fadeOut(100);
        $("main").addClass("main-active");

        if(data.total_results > 0) {

            var count_persons = 0;
            // Persons
            for (var i = 0; i < data.results.length; i++) {
                poster_i = data.results[i];

                if(poster_i.media_type == "person" && poster_i.profile_path != null) {
                    count_persons ++;
                    var info_for = "";
                    var name = poster_i.name.replace(" ", "+");

                    var poster_str = "\
                    <a href='https://www.google.es/search?q="+name+"' target='_blank' class='person-item'>\
                        <div class='img' style='background-image: url(https://image.tmdb.org/t/p/" + width_poster + poster_i.profile_path + ")'></div>\
                        <p>" + poster_i.name + "</p>\
                    </a>\
                    ";

                    $('#person-results').append(poster_str);
                }
            }

            if(count_persons == 0){
                $('#person-results').hide();
                $('#movie-show-results').css("padding-top", "0");
            }

            // Movies and Shows
            for (var i = 0; i < data.results.length; i++) {
                poster_i = data.results[i];

                if(poster_i.poster_path != null) {
                    var info_for = "";

                    if (poster_i.media_type == "movie") info_for = "movie"
                    if (poster_i.media_type == "tv") info_for = "show"

                    var poster_str = "\
                    <a href='/" + info_for + "/" + poster_i.id + "' class='poster-item list col s4 m3 l2 no-padding'>\
                        <img src='https://image.tmdb.org/t/p/w" + width_poster + poster_i.poster_path + "' />\
                     </a>\
                    ";

                    $('#movie-show-results').append(poster_str);
                }
            }
            resizePosters();
        }else{
            $('#movie-show-results').append("<p class='infoPeticion'>No hay ningún resultado</p>");
            $('#person-results').hide();
            $('#movie-show-results').css("padding-top", "0");
        }

    }).fail(function( jqXHR, textStatus, errorThrown ) {
        console.error('La solicitud; Búsqueda de: "' + query + ', a fallado: ' +  textStatus);
    });
}
