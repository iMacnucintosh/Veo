/**
 * Created by mlopez on 29/01/2019.
 */

$(document).ready(function(){
    $('ul.tabs').tabs({
        swipeable: false,
        //swipeable: true,
        //responsiveThreshold: Infinity
    });

    $('.carousel.carousel-slider').carousel({
        fullWidth: true,
        indicators: true
    });

    $('.fixed-action-btn').floatingActionButton({
        direction: 'left',
    });

    $('.tooltipped').tooltip();

    $('.modal').modal();

    $('form input').addClass("validate");

    $('#search').submit(function() {
        $(this).attr("action", "/search/" + $(this).find('input').val().replace(/ /g, "_"));
    });

    allowRequest = true;

    // ------- SCROLL EVENT -------
    $(window).scroll(function(){

        if(scrollPercent() >= 90 && allowRequest){
            setTimeout(function(){nextPageRequest()}, 150);
            allowRequest = false;
        }

        var scrollActual = $(window).scrollTop()

        if(scrollActual == 0){
            $('.fixed-action-btn').removeClass("fixed-action-btn-hidden ");
        }else{
            $('.fixed-action-btn').addClass("fixed-action-btn-hidden ");
        }

        if($('.tabs').length > 0) {
            if (scrollActual >= 80) {
                if($('main').hasClass("main-home")){
                    $('.tabs').addClass("tabs-fixed");
                    $('main').addClass("home-main-tabs");
                }else
                {
                    $('.tabs').addClass("tabs-fixed");
                    if (!$('main').hasClass("main-info")) {
                        $('main').addClass("main-tabs");
                    } else {
                        $('main').addClass("main-tabs-info");
                    }
                }
            } else {
                if($('main').hasClass("main-home")){
                    $('.tabs').removeClass("tabs-fixed");
                    $('main').removeClass("home-main-tabs");
                }else {
                    $('.tabs').removeClass("tabs-fixed");
                    $('main').removeClass("main-tabs");
                    $('main').removeClass("main-tabs-info");
                }
            }
        }

        saveScrollTab()

    });

    // Resize del tamaño de los posters si cambiamos la orientación del smartphone
    $(window).resize(function(){
        resizePosters();
    });

    // AutoZoomIn-Out to Backdrop image
    //setInterval(zoomBackdrop, 15);

    if(localStorage.getItem("active_tab") != null){
        $('.tabs').tabs('select', localStorage.getItem("active_tab").replace("#",""));
    }

    // ------------------------ CLICK EVENTS ------------------------------

    /* Scroll al inicio si clickamos en una tab */
    $('.tab-btn').click(function(){

        var tab = $(this);

        localStorage.setItem("active_tab", $(tab).attr("href"));

        switch($(tab).attr("href")){

            case "#movies_popularity":
                if(scroll_movies_popularity >= 80){
                    console.log(scroll_movies_popularity);
                    $('html, body').animate({
                        scrollTop: scroll_movies_popularity
                    },0);
                }else{
                    $('html, body').animate({
                        scrollTop: 0
                    },0);
                }
                break;
            case "#movies_vote_count":
                if(scroll_movies_vote_count >= 80){
                    $('html, body').animate({
                        scrollTop: scroll_movies_vote_count
                    },0);
                }else{
                    $('html, body').animate({
                        scrollTop: 0
                    },0);
                }
                break;
            case "#movies_theatres":
                if(scroll_movies_now_playing >= 80){
                    $('html, body').animate({
                        scrollTop: scroll_movies_now_playing
                    },0);
                }else{
                    $('html, body').animate({
                        scrollTop: 0
                    },0);
                }
                break;
            case "#shows_popularity":
                if(scroll_shows_popularity >= 80){
                    $('html, body').animate({
                        scrollTop: scroll_shows_popularity
                    },0);
                }else{
                    $('html, body').animate({
                        scrollTop: 0
                    },0);
                }
                break;
            case "#shows_vote_count":
                if(scroll_shows_vote_count >= 80){
                    $('html, body').animate({
                        scrollTop: scroll_shows_vote_count
                    },0);
                }else{
                    $('html, body').animate({
                        scrollTop: 0
                    },0);
                }
                break;
        }
        allowRequest = true;
    });

    /* Abrimos el panel de Configuración */
    $('.img-profile').click(function(){
        $('#settings').fadeIn(150);
    });

    /* Cerramos el panel de Configuración */
    $('.close-settings-container').click(function() {
        $('#settings').fadeOut(150);
    });

    $('.search-container').click(function(){
        $('.search-field').fadeIn(150);
    });

    $('.search-field i').click(function(){
        $('.search-field').fadeOut(150);
    });

    /* Volvemos a la pagina anterior desde una película o serie */
    $('.btn-back-list').click(function(){
        history.back();
    });
});