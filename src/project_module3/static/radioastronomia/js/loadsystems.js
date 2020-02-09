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

// gctx = document.getElementById("graphcanvas").getContext('2d');
var fdates = document.getElementById("form-filter-dates");
var DATAS = []
var ll = []

var timeFormat = 'MM/DD/YYYY HH:mm';
// var HChart = new Chart(gctx, {
//     type: 'line',
//     data: { labels: ll,
//             datasets: DATAS
//            },
//     options: {
//         responsive: true,
//         title: {
//             display: false,
//             text: '',
//         },
//         scales: {
//             xAxes: [{
//                 gridLines:{
//                     display: true
//                     },
//                 type: 'time',
//                 time: {
//                     parser: timeFormat,
//                     // minUnit: 'hour',
//                     // round: 'month',
//                     tooltipFormat: 'll HH:mm'},
//                 // distribution: 'series',
//                 scaleLabel: {
// 							display: true,
// 							labelString: 'Date'
// 						}
//                 }],
//             yAxes: [{
//                 type: 'linear',
//                 display: 'true',
//                 gridLines:{
//                     display: true
//                     },
//                 ticks:{
//                     fontColor: '#000',
//                     autoSkip: true
//                     },
//                 position: 'left',
//                 id: 'y-axis-1'}
//                 ]
//             }
//         }
// });

function dateformat(datestr){

    var year = datestr.slice(0, 4)
    var month = parseInt(datestr.slice(5, 7))-1
    var day = datestr.slice(8, 10);
    var hour = datestr.slice(11,13)
    var minute = datestr.slice(14,16)
    var second = datestr.slice(17,18)

    return Date.UTC(year,month,day,hour,minute, second); 

}


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
        var fecha   = JSON.parse(xhr.response).fecha;
        var message = JSON.parse(xhr.response).mensaje;
  
        ll = []
        DATAS = [];
        // HChart.data.labels = ll;
        // HChart.data.datasets = DATAS;
        // HChart.update();
        
        divmessage = document.getElementById("message");
        divmessage.innerHTML = message;
        divmessage.style.backgroundColor = "#c2c7cb"
        divmessage.style.width = "100%";
        divmessage.style.textAlign = "center";
        

        var adseries = [];

        // if(HChart.data.datasets.length == 0 && list.length>0){
        if(list.length>0){
            for(i=0; i<=Object.keys(list[0]).length-1; i++){
                // console.log("fecha: ", dateformat(fecha[i].fecha))
                // console.log("Empty list", DATAS.length, DATAS)
                // DATAS.push({
                //             label: Object.keys(list[0])[i],
                //             data: [],
                //             backgroundColor:colors[i],
                //             borderColor: colors[i],
                //             borderWidth: 2,
                //             pointRadius: 0,
                //             hoverRadius: 2,
                //             pointHitRadius: 10,
                //             fill: false})
                
                adseries.push({name: Object.keys(list[0])[i],
                               data: [],
                               color: colors[i]
                        })

                }
                


            var counter = 1;
            
           
            for(i=0; i<=list.length-1; i++){
                counter++
                // HChart.data.labels.push(dateformat(fecha[i].fecha));
                // HChart.data.labels.push(dateformat(fecha[i].fecha));
                for(index=0; index<=Object.keys(list[i]).length-1; index++){
                    var met__array = {x:new Date(fecha[i].fecha),y:parseFloat(Object.values(list[i])[index])};

                    // HChart.data.datasets[index].data.push(met__array)
                    
                    // adseries[index].data.push(parseFloat(Object.values(list[i])[index]))
                    adseries[index].data.push([dateformat(fecha[i].fecha), parseFloat(Object.values(list[i])[index])])
                    // adseries[index].data.push(parseFloat(Object.values(list[i])[index]))
                    
                }

                

            }
        }
        hchartploter(adseries)
        // HChart.update()
    }
}


var URL_C = "/radioastronomia/weatherhistory"  // O date para solicitar info por fechas
sendconcept("History", "Hour", URL_C)

document.getElementById("Hour").addEventListener("click", function(){
    sendconcept("History", "Hour", URL_C)
});
document.getElementById("Day").addEventListener("click", function(){
    sendconcept("History", "Day", URL_C)
});
document.getElementById("Week").addEventListener("click", function(){
    sendconcept("History", "Week", URL_C)
});


document.getElementById("plot").addEventListener("click", function(event){
    event.preventDefault();
    sendconcept("History", "Dates", URL_C)
})



// document.getElementById("Month").addEventListener("click", sendconcept.bind(null, "History", "Month", URL_C))

// FIN MANEJO DE PETICIONES PARA HISTORIAL GRAFICA- SUBSISTEMA ESTACION

function hchartploter(adseries){

Highcharts.chart('historyplot', {
    chart: {
        zoomType: 'x'
    },
    title: {
        text: 'Variables meteorológicas'
    },

    subtitle: {
        text: 'Historial: mediciones ambientales'
    },
    xAxis:{
        type: 'datetime',
        tickPixelInterval: 100
        // maxZoom: 20 * 1000
    },
    yAxis: {
        title: {
            text: 'Variable física medida'
        }
    },
    legend: {
        layout: 'horizontal',
        align: 'center'
    },

    plotOptions: {
        series: {
            label: {
                connectorAllowed: false
            },
            pointStart: 2010
        }
    },

    series: adseries,
    responsive: {
        rules: [{
            condition: {
                maxWidth: 500
            },
            chartOptions: {
                legend: {
                    layout: 'horizontal',
                    align: 'center',
                    horizontalAlign: 'top'
                }
            }
        }]
    }

});

}




// ads = [{
//             name: 'Installation',
//             data: [43934, 52503, 57177, 69658, 97031, 119931, 137133, 154175]
//         }, {
//             name: 'Manufacturing',
//             data: [24916, 24064, 29742, 29851, 32490, 30282, 38121, 40434]
//         }, {
//             name: 'Sales & Distribution',
//             data: [11744, 17722, 16005, 19771, 20185, 24377, 32147, 39387]
//         }, {
//             name: 'Project Development',
//             data: [null, null, 7988, 12169, 15112, 22452, 34400, 34227]
//         }, {
//             name: 'Other',
//             data: [12908, 5948, 8105, 11248, 8989, 11816, 18274, 18111]
//         }]

