/**
 * Created by mlopez on 29/01/2019.
 */

$(document).ready(function(){
    M.AutoInit();

    $(".remove-player").click(function(){
        var current_players = parseInt($('.player-count').text());

        if(current_players >= 3){
            $('.player-count').text(current_players - 1);
        }
    });

    $(".add-player").click(function(){
        var current_players = parseInt($('.player-count').text())
        $('.player-count').text(current_players + 1);
    });

});