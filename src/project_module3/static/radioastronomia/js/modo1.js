function validatedSendForm(){
    var BSE_DI = document.getElementById('start').value;
    var BSE_DF = document.getElementById('end').value;

    if(BSE_DI>BSE_DF){
        window.alert("Rango de fechas inválido");

    }
    else{
        sendForm();
    }

}

var cargando = document.getElementById("loading-data");
function cargar(){
    console.log("evento")
    cargando.style.display = "block";
}
function sendForm(){
    
    

    document.getElementById("enviar").addEventListener("click", cargar);

    var formElement = document.getElementById("form_id")
    var informacion = document.getElementById("informacion")
    var fecha_min = document.getElementById("fecha_min")
    var fecha_max = document.getElementById("fecha_max")
    // en caso de querer agregar informacion extra
    // formData = new FormData(formElement)
    // formData.append("region",1); //esto es informacion extra

    var xhr = new XMLHttpRequest();
    xhr.open("POST","/radioastronomia/barrido-espectro", false);
    xhr.send(new FormData(formElement))
    

    if (xhr.status==200){
        cargando.style.display = "none";
        //esta variable lee lo que viene del servidor
        stateobject = xhr.response;
        stateobject = JSON.parse(stateobject);
        fmuestreo.innerHTML = "Frecuencia de muestreo: "+ stateobject.frec_muestreo+" Samp/s\n";
        nfft.innerHTML = "nFFT: "+ stateobject.nfft;
        // informacion.innerHTML = "Analisis comprendido entre las fechas"
        // fecha_min.innerHTML = stateobject.min_date+"\n"
        // fecha_max.innerHTML = stateobject.max_date
        //inicio grafica bandas del espectro
        Highcharts.chart('grafica', {
            chart: {
                zoomType: 'x'
            },
            title: {
                text: 'Espectro por bandas de frecuencia'
            },
            subtitle: {
                text: document.ontouchstart === undefined ?
                    'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
            },
            xAxis: {
                type: 'series',
                title:{
                    text: "Frecuencia MHz"
                }
            },
            yAxis: {
                title: {
                    text: 'Espectro'
                }
            },
            legend: {
                enabled: false
            },
            plotOptions: {
                area: {
                    fillColor: {
                        linearGradient: {
                            x1: 0,
                            y1: 0,
                            x2: 0,
                            y2: 1
                        },
                        stops: [
                            [0, Highcharts.getOptions().colors[0]],
                            [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                        ]
                    },
                    marker: {
                        radius: 2
                    },
                    lineWidth: 1,
                    states: {
                        hover: {
                            lineWidth: 1
                        }
                    },
                    threshold: null
                }
            },

            series: [{
                type: 'area',
                name: 'Espectro',
                data: stateobject.data,
                connectNulls: false // by default
            }],
            lang: {
                noData: "No hay datos"
            },
            noData: {
                style: {
                    fontWeight: 'bold',
                    fontSize: '15px',
                    color: '#303030'
                }
            }
        });
        //fin grafica bandas del espectro

        // inicio grafica de la energia
        Highcharts.chart('grafica_energia', {
            chart: {
                zoomType: 'x'
            },
            title: {
                text: 'Energia por banda de frecuencia'
            },
            subtitle: {
                text: document.ontouchstart === undefined ?
                    'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
            },
            xAxis: {
                type: 'series',
                title:{
                    text: "Frecuencia MHz"
                }
            },
            yAxis: {
                title: {
                    text: 'Energia'
                }
            },
            legend: {
                enabled: false
            },
            plotOptions: {
                area: {
                    fillColor: {
                        linearGradient: {
                            x1: 0,
                            y1: 0,
                            x2: 0,
                            y2: 1
                        },
                        stops: [
                            [0, Highcharts.getOptions().colors[0]],
                            [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                        ]
                    },
                    marker: {
                        radius: 2
                    },
                    lineWidth: 1,
                    states: {
                        hover: {
                            lineWidth: 1
                        }
                    },
                    threshold: null
                },

                column: {
                    pointPadding: 0,
                    borderWidth: 0,
                    groupPadding: 0,
                    shadow: false
                }
            },

            series: [{
                type: 'column',
                name: 'Espectro',
                data: stateobject.data_energia
            }]
        });
        //fin grafica de la energia

    }
    else{
        output.innerHTML += "Error HTTP"+ xhr.status;
    }

}

