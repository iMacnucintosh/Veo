/**
 * Created by mlopez on 30/01/2019.
 */
function TmdbRequestFilter(selector_container, url, parameters, description_request, info_for){

    parameters["api_key"] = "f368d6c9a2c7d460dacc7cfd42809665";

    $.ajax({
        data: parameters,
        type: "GET",
        dataType: "json",
        url: url,
    }).done(function(data, textStatus, jqXHR) {
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

function InformationMovie(id, parameters) {

    parameters["api_key"] = "f368d6c9a2c7d460dacc7cfd42809665";

    // Basic Information
    $.ajax({
        data: parameters,
        type: "GET",
        dataType: "json",
        url: "https://api.themoviedb.org/3/movie/" + id,
    }).done(function(recommended_movie, textStatus, jqXHR) {
        console.log(recommended_movie);
        var backdrop_path_style = "style='background-image: url(https://image.tmdb.org/t/p/w500" + recommended_movie.backdrop_path + ")'";

        if(recommended_movie.title.length >= 17){
            $('#title').css("font-size", "1em");
        }

        $('title').text("Veo | " + recommended_movie.title);
        $('#title').text(recommended_movie.title);
        $('#backdrop-image').attr("style", "background-image: url(https://image.tmdb.org/t/p/w500" + recommended_movie.backdrop_path) + ")";
        $('#poster-img').attr("src", "https://image.tmdb.org/t/p/w300" + recommended_movie.poster_path);
        $('#date-release').text(recommended_movie.release_date);
        $('#sinopsis').text(recommended_movie.overview);
        $('#title').addClass('fadeIn');


        // Genres
        var genres_str = "";
        for(var i=0; i<recommended_movie.genres.length;i++) {
            var genre = recommended_movie.genres[i];
            genres_str += "<div class='genre'>" + genre.name + "</div>";
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
        console.log(related_movies);
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
            $('#related').append("<p class='infoPeticion'>No hay películas relacionadas</p>");
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

function InformationShow(id, parameters) {

    parameters["api_key"] = "f368d6c9a2c7d460dacc7cfd42809665";

    // Basic Information
    $.ajax({
        data: parameters,
        type: "GET",
        dataType: "json",
        url: "https://api.themoviedb.org/3/tv/" + id,
    }).done(function(recommended_show, textStatus, jqXHR) {

        var backdrop_path_style = "style='background-image: url(https://image.tmdb.org/t/p/w500" + recommended_show.backdrop_path + ")'";

        if(recommended_show.name.length >= 17){
            $('#title').css("font-size", "1em");
        }

        $('title').text("Veo | " + recommended_movie.title);
        $('#title').text(recommended_show.name);

        $('#backdrop-image').attr("style", "background-image: url(https://image.tmdb.org/t/p/w500" + recommended_show.backdrop_path) + ")";
        $('#poster-img').attr("src", "https://image.tmdb.org/t/p/w300" + recommended_show.poster_path);
        $('#sinopsis').text(recommended_show.overview);
        $('#title').addClass('fadeIn');


        /* Collapsibles for Seasons */
        var seasons_str = '';

        for(var i=0; i<recommended_show.seasons.length; i++){
            var season = recommended_show.seasons[i];
            seasons_str += '<div class="season-poster poster-item list col s4 m3 l2 no-padding" onclick="showSeasonInfo('+i+')">\
                <img src="https://image.tmdb.org/t/p/w300/' + season.poster_path + '">\
                </div>';

            // Information for each season
            InformationSeason(id, i, parameters);

        }

        $('#seasons-posters-list').append(seasons_str);

        resizePosters();

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
        console.log(season_info);

        var season_info_str = '<div id="season-details-'+ num_season + '" class="season-details">\
         <div class="header-season row col s12">\
            <div class="close-season-details">\
                <i class="material-icons">close</i>\
            </div>\
            <div class="poster-item list col s4 m3 l2 no-padding">\
                <img src="https://image.tmdb.org/t/p/w300/' + season_info.poster_path + '">\
            </div>\
            <div class="season-info col s8">\
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
            season_info_str += '\
                        <li>\
                            <div class="collapsible-header"><i class="material-icons">radio_button_unchecked</i>' + episode.name + '</div>\
                            <div class="collapsible-body"><p class="episode-overview col s12">' + episode.overview + '</p></div>\
                        </li>'
        }

        season_info_str += '</ul></div></div>';

        $('#seasons').append(season_info_str);

        $('.collapsible').collapsible();


        // Se marca muchas veces
        $('.season-episodes .collapsible-header i').on("click", function(e) {
            console.log("Marcariamos como visto o no visto");
            if($(this).text() == "radio_button_unchecked"){
                console.log("aasdf");
                $(this).text("radio_button_checked")
            }else{
                $(this).text("radio_button_unchecked")
            }
            e.stopPropagation();
            $(this).click(function(){});
        } )


        $('.close-season-details').click(function(){
            $(this).parent().parent().fadeOut(150);
        });

    }).fail(function( jqXHR, textStatus, errorThrown ) {
        console.error('La solicitud: Información de Serie, a fallado: ' +  textStatus);
    });

}

function showSeasonInfo(num){
    $('#season-details-' + num).fadeIn(150);
}