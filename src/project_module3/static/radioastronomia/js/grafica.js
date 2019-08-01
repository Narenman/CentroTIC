function callAjax(){

        $.ajax({
            type: "GET",
            url: "/radioastronomia/grafica-espectro",
            //data: {},
            dataType: 'json',
            success: function (data){
                  
                   Highcharts.chart('grafica_espectro', {
                    chart: {
                        zoomType: 'x'
                    },
                    title: {
                        text: 'Espectro '
                    },
                    subtitle: {
                        text: document.ontouchstart === undefined ?
                                'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
                    },
                     xAxis: {
                         title: {
                             text: 'Frecuencia MHz',
                         }
                     },
                    
                    yAxis: {
                        title: {
                            text: 'Espectro dBm'
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
                        type: 'line',
                        name: 'Espectro',
                        data: data.espectro,
                            }]
                }); //fin grafica
                interval = setTimeout(callAjax, 4000);
            } //fin success
            }); // fin ajax

        }
callAjax()
