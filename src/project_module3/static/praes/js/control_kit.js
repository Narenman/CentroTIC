$(document).ready(function(){
    // evento del click para graficar la temperatura

    $("#control1s").click(function(event){
        $.ajax({
            type: "POST",
            url: "/app_praes/control_kit/",
            data: {"info":"1 medicion"},
            dataType: 'json',
            success: function (data){

            }//sucess
        }); //fin ajax
       
    }); // fin evento

    $("#control30s").click(function(event){
        $.ajax({
            type: "POST",
            url: "/app_praes/control_kit/",
            data: {"info":"30 segundos"},
            dataType: 'json',
            success: function (data){

            }//sucess
        }); //fin ajax

      
    }); // fin evento

    $("#control1m").click(function(event){
        $.ajax({
            type: "POST",
            url: "/app_praes/control_kit/",
            data: {"info":"1 minuto"},
            dataType: 'json',
            success: function (data){

            }//sucess
        }); //fin ajax

      
    }); // fin evento

    $("#control5m").click(function(event){
        $.ajax({
            type: "POST",
            url: "/app_praes/control_kit/",
            data: {"info":"5 minutos"},
            dataType: 'json',
            success: function (data){

            }//sucess
        }); //fin ajax

     
    }); // fin evento

    $("#modo-nariz").click(function(event){
        $.ajax({
            type: "POST",
            url: "/app_praes/control_kit/",
            data: {"info":"modo-nariz"},
            dataType: 'json',
            success: function (data){

            }//sucess
        }); //fin ajax

     
    }); // fin evento

});