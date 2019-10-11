var estadoc = false;
var estadoes = false;

function cargar(){
    // esta funcion lee los id del HTML
    eambiental = document.getElementById('eambiental')
    ecamara = document.getElementById('ecamara')
    fambiental = document.getElementById('fambiental')
    fcamara = document.getElementById('fcamara')
    inacamara = document.getElementById('inacamara')
    inaestacion = document.getElementById('inaestacion')
}

cargar()

function obtenerestado(){
    // se encarga de leer el estado y ocultar de acuerdo
    // a la peticion
    var xhr1 = new XMLHttpRequest();
    var xhr2 = new XMLHttpRequest();

    xhr1.onreadystatechange = function(){

        if (this.readyState == 4 && this.status ==200){
            stateobject = this.response;
            stateobject = JSON.parse(stateobject)
            estadoc = stateobject.activo
        }
    };

    xhr2.onreadystatechange = function(){

        if (this.readyState == 4 && this.status ==200){
            stateobject = this.response;
            stateobject = JSON.parse(stateobject)
            estadoes = stateobject.activo
        }
    };


    xhr1.open("GET", "/radioastronomia/estado/camara/1", true);
    xhr1.send();
    xhr2.open("GET", "/radioastronomia/estado/estacion/1", true);
    xhr2.send();

    if (estadoc==true){
        ecamara.style.display = "block";
        fcamara.style.display = "block";
        inacamara.style.display = "none";

    }
    else if(estadoc == false){
        ecamara.style.display = "none";
        fcamara.style.display = "none";
        inacamara.style.display = "block"
    }
    if (estadoes==true){
        eambiental.style.display = "block";
        fambiental.style.display = "block";
        inaestacion.style.display = "none";
    }
    else if(estadoes==false){
        eambiental.style.display = "none";
        fambiental.style.display = "none";
        inaestacion.style.display = "block";
    }

    setTimeout(obtenerestado, 2000);

} //fin obtener estado


function detener_estacion(){
    var xhr = new XMLHttpRequest();
    xhr.open("POST","/radioastronomia/detener/subsistemas", true);
    data = new FormData();
    data.append('detener', 'estacion')
    xhr.send(data);
}

function detener_camara(){
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/radioastronomia/detener/subsistemas", true);
    data = new FormData();
    data.append('detener', 'camara')
    xhr.send(data);


}


obtenerestado()
//eventos de click
document.getElementById("bot_estacion").addEventListener("click", detener_estacion);
document.getElementById("bot_camara").addEventListener("click", detener_camara);


// INICIO GRAFICA Y MANEJO DE PETICIONES PARA HISTORIAL - SUBSISTEMA ESTACION
// concept ex       : history
// concept value ex : day
// url ex           : "/radioastronomia/detener/subsistemas"
gctx = document.getElementById("graphcanvas").getContext('2d');
var fdates = document.getElementById("form-filter-dates");
var DATAS = []
var ll = []
var HChart = new Chart(gctx, {
    type: 'line',
    data: { labels: ll,
            datasets: DATAS
           },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});


function sendconcept(concept, concept_value, url){
    
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url , false);

    if(concept_value == "Dates"){

        data = new FormData(fdates);
    }
    else{
        data = new FormData();
    }

    // data = new FormData();
    data.append(concept, concept_value)
    //VALIDAR ANTES DE ENVIAR AL SERVIDOR////PENDIENTE
    xhr.send(data);
    
    if (xhr.status==200){
        
        var list    = JSON.parse(xhr.response).respuesta;
        var colors  = JSON.parse(xhr.response).colors;
        var fecha   = JSON.parse(xhr.response).fecha
        var message = JSON.parse(xhr.response).mensaje

        console.log(list)

        ll = []
        DATAS = [];
        HChart.data.labels = ll;
        HChart.data.datasets = DATAS;
        HChart.update();
        
        divmessage = document.getElementById("message");
        divmessage.innerHTML = message;
        divmessage.style.backgroundColor = "#c2c7cb"
        divmessage.style.width = "100%";
        divmessage.style.textAlign = "center";
        
        if(HChart.data.datasets.length == 0 && list.length>0){
            for(i=0; i<=Object.keys(list[0]).length-1; i++){
            
                // console.log("Empty list", DATAS.length, DATAS)
                DATAS.push({
                            label: Object.keys(list[0])[i],
                            data: [],
                            backgroundColor:colors[i],
                            borderColor: colors[i],
                            borderWidth: 0.1,
                            fill: false})
                }


            var counter = 1;
            for(i=0; i<=list.length-1; i++){
                HChart.data.labels.push(counter++);

                for(index=0; index<=Object.keys(list[i]).length-1; index++){
                    HChart.data.datasets[index].data.push(Object.values(list[i])[index])
                 
                }

            }
        }
        HChart.update()
    }
}


var URL_C = "/radioastronomia/weatherhistory"  // O date para solicitar info por fechas

document.getElementById("Hour").addEventListener("click", sendconcept.bind(null,  "History", "Hour", URL_C))
document.getElementById("Day").addEventListener("click", sendconcept.bind(null, "History", "Day", URL_C))
document.getElementById("Week").addEventListener("click", sendconcept.bind(null, "History", "Week", URL_C))


document.getElementById("plot").addEventListener("click", function(event){
    event.preventDefault();
    sendconcept("History", "Dates", URL_C)
})







// document.getElementById("Month").addEventListener("click", sendconcept.bind(null, "History", "Month", URL_C))

// FIN MANEJO GRAFICA DE PETICIONES PARA HISTORIAL - SUBSISTEMA ESTACION
