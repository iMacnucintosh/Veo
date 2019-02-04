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

    $("main").addClass("main-active");

    $('form input').addClass("validate");

    // ------- SCROLL EVENT -------
    $(window).scroll(function(){

        var scrollActual = $(window).scrollTop()

        if($('.tabs').length > 0) {
            if (scrollActual >= 80) {
                $('.tabs').addClass("tabs-fixed");
                if(!$('main').hasClass("main-info")){
                    $('main').addClass("main-tabs");
                }else {
                    $('main').addClass("main-tabs-info");
                }
            } else {
                $('.tabs').removeClass("tabs-fixed");
                $('main').removeClass("main-tabs");
                $('main').removeClass("main-tabs-info");
            }
        }
    });

    // Resize del tamaño de los posters si cambiamos la orientación del smartphone
    $(window).resize(function(){
        resizePosters();
    });

    // AutoZoomIn-Out to Backdrop image
    //setInterval(zoomBackdrop, 15);

    // ------------------------ CLICK EVENTS ------------------------------

    /* Scroll al inicio si clickamos en una tab */
    $('.tab-btn').click(function(){
        if($(window).scrollTop() >= 80){
            $('html, body').animate({
                scrollTop: 80
            },400);
        }
    });

    /* Abrimos el panel de Configuración */
    $('.img-profile').click(function(){
        $('#settings').fadeIn(150);
    });

    /* Cerramos el panel de Configuración */
    $('.close-settings-container').click(function() {
        $('#settings').fadeOut(150);
    });

    /* Volvemos a la pagina anterior desde una película o serie */
    $('.btn-back-list').click(function(){
        history.back();
    });


});