function sendForm(){
    
    var formElement = document.getElementById("form_id")
    // en caso de querer agregar informacion extra
    // formData = new FormData(formElement)
    // formData.append("region",1); //esto es informacion extra

    var xhr = new XMLHttpRequest();
    xhr.open("POST","/radioastronomia/barrido-espectro", false)
    xhr.send(new FormData(formElement))

    if (xhr.status==200){
        
        //esta variable lee lo que viene del servidor
        stateobject = xhr.response;
        stateobject = JSON.parse(stateobject);
        fmuestreo.innerHTML = "Frecuencia de muestreo: "+ stateobject.frec_muestreo+" Samp/s\n";
        nfft.innerHTML = "nFFT: "+ stateobject.nfft;

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
                data: stateobject.data
            }]
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

