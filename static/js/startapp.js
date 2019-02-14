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

    // ------- SCROLL EVENT -------
    $(window).scroll(function(){

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