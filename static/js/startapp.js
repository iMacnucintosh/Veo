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


    if(localStorage.getItem("active_tab") != null && localStorage.getItem("active_tab") != "#related" && localStorage.getItem("active_tab") != "#recommendations" && localStorage.getItem("active_tab") != "#home-movies-pending" && localStorage.getItem("active_tab") != "#home-shows-active"){
        $('.tabs').tabs('select', localStorage.getItem("active_tab").replace("#",""));
    }

    if($('#recommendations-tab a').hasClass("active")){
        readRecommendations();
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
                    },100);
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
                    },100);
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
                    },100);
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
                    },100);
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
                    },100);
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
        $('#txt-search').focus();
    });

    $('.search-field i').click(function(){
        $('.search-field').fadeOut(150);
    });

    /* Volvemos a la pagina anterior desde una película o serie */
    $('.btn-back-list').click(function(){
        history.back();
    });

    $('.info-popup').click(function(){
        $(this).fadeOut(100);
    });

    // Abre la galeria para subir una foto de perfil
    $('#select_image').click(function(){
        $('#id_image').click();
    });

    $('#id_image').change(function(){
        var image = $(this).val();
        if(image != ""){
            $(this).parent().submit();
        }
    });

    $('#id_image').attr("accept", "image/*");

    // Selección de colores en creación de lista
    $('.color').click(function(){
        $('.color').removeClass("selected");
        $(this).addClass("selected");
    });

    $('#recommendations-tab').click(function(){
        readRecommendations();
    });

    $('.friend').click(function(){
        $(this).toggleClass("selected");
    });

});