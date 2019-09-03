var ATE_DI = document.getElementById('start').value;
var ATE_DF = document.getElementById('end').value;
var ATform = document.getElementById('form_modo2');




ATform.addEventListener('submit', function(event){

    event.preventDefault();
    var ATfdata = new FormData(ATform);
    var ATxhr = new XMLHttpRequest();


    if(ATE_DI>ATE_DF){
        window.alert("Rango de fechas inválido");

    }
    else if (ATE_DI==ATE_DF){
        window.alert("Las fechas ingresadas son iguales");
    }

    else{
        ATxhr.open("POST", '/radioastronomia/modo/analisis-tiempo', true);
        ATxhr.send(ATfdata);
    }

});
