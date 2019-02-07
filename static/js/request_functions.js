/**
 * Created by mlopez on 30/01/2019.
 */

// Return a list with Movies or Shows with the parameters you has specified
function TmdbRequestFilter(selector_container, url, parameters, description_request, info_for){

    parameters["api_key"] = "f368d6c9a2c7d460dacc7cfd42809665";

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
                <a href='/"+info_for+"/" + poster_i.id + "' class='poster-item list col s4 m3 l2 no-padding'>\
                    <img src='https://image.tmdb.org/t/p/w300" + poster_i.poster_path + "' />\
                 </a>\
                ";

                $(selector_container).append(poster_str);
            }
            resizePosters();
        }
    }).fail(function( jqXHR, textStatus, errorThrown ) {
        console.error('La solicitud: "' + description_request + '", a fallado: ' +  textStatus);
    });
}

// Return a specific number of random movies from your list
function RecommendedMovies() {
    $.ajax({
        data: {
            "api_key":"f368d6c9a2c7d460dacc7cfd42809665",
            "language": "es-ES"
        },
        type: "GET",
        dataType: "json",
        url: "https://api.themoviedb.org/3/movie/424783?api_key=&language=es",
    }).done(function(data, textStatus, jqXHR) {
        var recommended_movie = data;
        var backdrop_path_style = "style='background-image: url(https://image.tmdb.org/t/p/w500" + recommended_movie.backdrop_path + ")'";
        var recommended_movie_str = "\
                <a href='/movie/" + recommended_movie.id + "' class='poster-item recommended col s12 no-padding' " + backdrop_path_style +"></a>";

        $("#home_portada").append(recommended_movie_str);

    }).fail(function( jqXHR, textStatus, errorThrown ) {
        console.error('La solicitud: Pelicula Recomendada, a fallado: ' +  textStatus);
    });
}

// Get all information from Movie
function InformationMovie(id, parameters, colorGenres, csrf_token) {

    parameters["api_key"] = "f368d6c9a2c7d460dacc7cfd42809665";

    // Basic Information
    $.ajax({
        data: parameters,
        type: "GET",
        dataType: "json",
        url: "https://api.themoviedb.org/3/movie/" + id,
    }).done(function(movie, textStatus, jqXHR) {
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
        $('.toSee').attr("alt", movie.poster_path);
        $('.toSee').attr("rel", movie.title);
        $('#poster-img').attr("src", "https://image.tmdb.org/t/p/w300" + movie.poster_path);
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
                                    <img src='https://image.tmdb.org/t/p/w300" + part.poster_path + "' />\
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
            if(response.result != "null"){
                $('.toSee').text("playlist_add_check");
                $('.toSee').attr("onclick", "removeMovieToSee(" + id + ", this, '" + csrf_token +"')");
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
                    <img src='https://image.tmdb.org/t/p/w300" + poster_i.poster_path + "' />\
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
                    <img src='https://image.tmdb.org/t/p/w300" + poster_i.poster_path + "' />\
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
        data: {"api_key":"f368d6c9a2c7d460dacc7cfd42809665"},
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

// Get all information from Show
function InformationShow(id, parameters, colorGenres) {

    parameters["api_key"] = "f368d6c9a2c7d460dacc7cfd42809665";

    // Basic Information
    $.ajax({
        data: parameters,
        type: "GET",
        dataType: "json",
        url: "https://api.themoviedb.org/3/tv/" + id,
    }).done(function(show, textStatus, jqXHR) {
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
        $('#poster-img').attr("src", "https://image.tmdb.org/t/p/w300" + show.poster_path);
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
                seasons_str += '<div class="season-poster poster-item list col s4 m3 l2 no-padding" onclick="showSeasonInfo(' + i + ')">\
                    <img src="https://image.tmdb.org/t/p/w300/' + season.poster_path + '">\
                    </div>';

                // Information for each season
                InformationSeason(id, i, parameters);
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
                    <img src='https://image.tmdb.org/t/p/w300" + poster_i.poster_path + "' />\
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
                    <img src='https://image.tmdb.org/t/p/w300" + poster_i.poster_path + "' />\
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
        data: {"api_key":"f368d6c9a2c7d460dacc7cfd42809665"},
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

function InformationSeason(id_show, num_season, parameters){
    parameters["api_key"] = "f368d6c9a2c7d460dacc7cfd42809665";

    // Basic Information
    $.ajax({
        data: parameters,
        type: "GET",
        dataType: "json",
        url: "https://api.themoviedb.org/3/tv/" + id_show + "/season/" + num_season,
    }).done(function(season_info, textStatus, jqXHR) {
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
                <img class="season-poster shadow" src="https://image.tmdb.org/t/p/w300/' + season_info.poster_path + '">\
                <h3 class="date-season">' + season_date_format + '</h3>\
                <p class="num-episodes-season">' + season_info.episodes.length + ' Episodios</p>\
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
                            <div class="collapsible-header"><i class="material-icons" onclick="changeStateEpisode(this, ' + id_show + ','+ num_season + ',' + episode.episode_number + ')" id="' + id_show + '_' + num_season + '_' + episode.episode_number + '">radio_button_unchecked</i>' + episode.name + '</div>\                            <div class="collapsible-body row no-margin"><p class="date-last-episode col s6">' + episode.air_date + '</p><p class="col s6 last-episode-number">T' + episode.season_number + ' x E' + episode.episode_number+ '</p><p class="col s12 last-episode-overview">' + overview + '</p></div>\
                        </li>'
        }

        season_info_str += '</ul></div></div>';

        $('#seasons').append(season_info_str);

        $('.collapsible').collapsible();


        // Se marca muchas veces
        $('.season-episodes .collapsible-header i').click(function(e) {
            e.stopPropagation();
        });


        $('.close-season-details').click(function(){
            $('body').css("overflow", "auto");
            $(this).parent().parent().fadeOut(150);
        });

    }).fail(function( jqXHR, textStatus, errorThrown ) {
        console.error('La solicitud: Información de la Temporada, a fallado: ' +  textStatus);
        $('#season-details-' + num_season).remove();
        $(".season-poster[onclick='showSeasonInfo(" + num_season + ")']").remove();
    });
}

// Check/Uncheck episode like seen
function changeStateEpisode(elemento, id, season, episode){
    // Pedición para cambiar el estado de visualización del capitulo
    if($(elemento).text() == "radio_button_unchecked"){
        $(elemento).text("radio_button_checked");
    } else{
        $(elemento).text("radio_button_unchecked");
    }

}

// Add a movie to list of user movies
function addMovieToSee(id, elemento, csrf_token){
    var data = new FormData();
    data.append('id', id);
    data.append('title', $(elemento).attr("rel"));
    data.append('poster_path', $(elemento).attr("alt"));
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
            $(elemento).attr("onclick", "removeMovieToSee(" + id + ", this, '" + csrf_token +"')");
        }
    });
}

// Remove a movie to list of user movies
function removeMovieToSee(id, elemento, csrf_token){

    var data = new FormData();
    data.append('id', id);
    data.append('title', $(elemento).attr("rel"));
    data.append('poster_path', $(elemento).attr("alt"));
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
            $(elemento).attr("onclick", "addMovieToSee(" + id + ", this, '" + csrf_token +"')");
        }
    });
}

function MyMoviesToSee(csrf_token, selector){
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
                    <img src='https://image.tmdb.org/t/p/w300" + poster_i.poster_path + "' />\
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

// Set a movie like seen
function setMovieToSeen(id, elemento, csrf_token){
    $(elemento).attr("src", "/static/images/on_list.png")
    $(elemento).attr("onclick", "setMovieToNotSeen(" + id + ", this, '" + csrf_token +"')");
/*
    var data = new FormData();
    data.append('id', id);
    data.append('title', $(elemento).attr("rel"));
    data.append('poster_path', $(elemento).attr("alt"));
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
            $(elemento).attr("onclick", "removeMovieToSee(" + id + ", this, '" + csrf_token +"')");
        }
    });
    */
}

// Set a movie like not seen
function setMovieToNotSeen(id, elemento, csrf_token){
    $(elemento).attr("src", "/static/images/not_on_list.png")
    $(elemento).attr("onclick", "setMovieToSeen(" + id + ", this, '" + csrf_token +"')");
/*
    var data = new FormData();
    data.append('id', id);
    data.append('title', $(elemento).attr("rel"));
    data.append('poster_path', $(elemento).attr("alt"));
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
            $(elemento).attr("onclick", "removeMovieToSee(" + id + ", this, '" + csrf_token +"')");
        }
    });
    */
}
