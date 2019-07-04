$(document).ready(function(){
    // evento del click para graficar la temperatura

    $("#activar").click(function(event){
        $.ajax({
            type: "POST",
            url: "/piscicultura/toma-datos",
            data: {"info":"activar"},
            dataType: 'json',
            success: function (data){

            }//sucess
        }); //fin ajax
       
    }); // fin evento

    $("#desactivar").click(function(event){
        $.ajax({
            type: "POST",
            url: "/piscicultura/toma-datos",
            data: {"info":"desactivar"},
            dataType: 'json',
            success: function (data){

            }//sucess
        }); //fin ajax

      
    }); // fin evento



});