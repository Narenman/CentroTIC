$(document).ready(function(){
    // evento del click del boton con id = hour1
    $("#hour1").click(function(event){
        console.log("Evento de 1 hora");

        $.ajax({
            type: "POST",
            url: "/app_sensado/presentacion-datos-json",
            data: {
                'hora': 1,
                   },
            dataType: 'json',
            success: function (data){
                   // temperatura
                   Highcharts.chart('grafica_temperatura', {
                    chart: {
                        zoomType: 'x'
                    },
                    title: {
                        text: 'Temperatura °C'
                    },
                    subtitle: {
                        text: document.ontouchstart === undefined ?
                                'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
                    },
                    xAxis: {
                        type: 'datetime',
                        
                    },
                    
                    yAxis: {
                        title: {
                            text: 'Temperatura °C'
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
        
                    time: {
                        timezone: 'America/Bogota'
                    },
                    
                    series: [{
                        type: 'area',
                        name: 'Temperatura',
                        data: data.temperatura,
                            }]
                }); //fin hightcharts


                // humedad
                Highcharts.chart('grafica_humedad', {
                    chart: {
                        zoomType: 'x'
                    },
                    title: {
                        text: 'Huemdad %'
                    },
                    subtitle: {
                        text: document.ontouchstart === undefined ?
                                'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
                    },
                    xAxis: {
                        type: 'datetime',
                        
                    },
                    
                    yAxis: {
                        title: {
                            text: 'Humedad'
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
        
                    time: {
                        timezone: 'America/Bogota'
                    },
                    
                    series: [{
                        type: 'area',
                        name: 'Humedad',
                        data: data.humedad,
                            }]
                }); //fin hightcharts
 
      
            }
        });
    });
});
