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
            //console.log(response);
        }
    });
}