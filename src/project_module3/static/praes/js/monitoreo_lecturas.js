$(document).ready(function(){
    // evento del click del boton con id = hour1

        $.ajax({
            type: "GET",
            url: "/app_praes/variables-json/",
            data: {},
            dataType: 'json',
            success: function (data){
                   // conversion de los datos del tiempo a epoch
                    // for (var i=0; i<data.temperatura.length; i++){
                    //     var year = data.temperatura[i][0].slice(0, 4)
                    //     var month = parseInt(data.temperatura[i][0].slice(5, 7))-1
                    //     var day = data.temperatura[i][0].slice(8, 10)
                    //     var hour = data.temperatura[i][0].slice(11,13)
                    //     var minute = data.temperatura[i][0].slice(14,16)
                    //     var second = data.temperatura[i][0].slice(17,18)
                    //     data.temperatura[i][0]=Date.UTC(year,month,day,hour,minute, second) 
                    //         }
                    // for (var i=0; i<data.humedad.length; i++){
                    //     var year = data.humedad[i][0].slice(0, 4)
                    //     var month = parseInt(data.humedad[i][0].slice(5, 7))-1
                    //     var day = data.humedad[i][0].slice(8, 10)
                    //     var hour = data.humedad[i][0].slice(11,13)
                    //     var minute = data.humedad[i][0].slice(14,16)
                    //     var second = data.humedad[i][0].slice(17,18)
                    //     data.humedad[i][0]=Date.UTC(year,month,day,hour,minute, second) 
                    //         }
                    // for (var i=0; i<data.presion.length; i++){
                    //     var year = data.presion[i][0].slice(0, 4)
                    //     var month = parseInt(data.presion[i][0].slice(5, 7))-1
                    //     var day = data.presion[i][0].slice(8, 10)
                    //     var hour = data.presion[i][0].slice(11,13)
                    //     var minute = data.presion[i][0].slice(14,16)
                    //     var second = data.presion[i][0].slice(17,18)
                    //     data.presion[i][0]=Date.UTC(year,month,day,hour,minute, second) 
                    //         }
                    for (var i=0; i<data.co.length; i++){
                        var year = data.co[i][0].slice(0, 4)
                        var month = parseInt(data.co[i][0].slice(5, 7))-1
                        var day = data.co[i][0].slice(8, 10)
                        var hour = data.co[i][0].slice(11,13)
                        var minute = data.co[i][0].slice(14,16)
                        var second = data.co[i][0].slice(17,18)
                        data.co[i][0]=Date.UTC(year,month,day,hour,minute, second) 
                            }
                    // for (var i=0; i<data.co2.length; i++){
                    //     var year = data.co2[i][0].slice(0, 4)
                    //     var month = parseInt(data.co2[i][0].slice(5, 7))-1
                    //     var day = data.co2[i][0].slice(8, 10)
                    //     var hour = data.co2[i][0].slice(11,13)
                    //     var minute = data.co2[i][0].slice(14,16)
                    //     var second = data.co2[i][0].slice(17,18)
                    //     data.co2[i][0]=Date.UTC(year,month,day,hour,minute, second) 
                    //         }
                    for (var i=0; i<data.ch4.length; i++){
                        var year = data.ch4[i][0].slice(0, 4)
                        var month = parseInt(data.ch4[i][0].slice(5, 7))-1
                        var day = data.ch4[i][0].slice(8, 10)
                        var hour = data.ch4[i][0].slice(11,13)
                        var minute = data.ch4[i][0].slice(14,16)
                        var second = data.ch4[i][0].slice(17,18)
                        data.ch4[i][0]=Date.UTC(year,month,day,hour,minute, second) 
                            }
                    // for (var i=0; i<data.polvo.length; i++){
                    //     var year = data.polvo[i][0].slice(0, 4)
                    //     var month = parseInt(data.polvo[i][0].slice(5, 7))-1
                    //     var day = data.polvo[i][0].slice(8, 10)
                    //     var hour = data.polvo[i][0].slice(11,13)
                    //     var minute = data.polvo[i][0].slice(14,16)
                    //     var second = data.polvo[i][0].slice(17,18)
                    //     data.polvo[i][0]=Date.UTC(year,month,day,hour,minute, second) 
                    //         }
                    // for (var i=0; i<data.so2.length; i++){
                    //     var year = data.so2[i][0].slice(0, 4)
                    //     var month = parseInt(data.so2[i][0].slice(5, 7))-1
                    //     var day = data.so2[i][0].slice(8, 10)
                    //     var hour = data.so2[i][0].slice(11,13)
                    //     var minute = data.so2[i][0].slice(14,16)
                    //     var second = data.so2[i][0].slice(17,18)
                    //     data.so2[i][0]=Date.UTC(year,month,day,hour,minute, second) 
                    //         }
                    // for (var i=0; i<data.no2.length; i++){
                    //     var year = data.no2[i][0].slice(0, 4)
                    //     var month = parseInt(data.no2[i][0].slice(5, 7))-1
                    //     var day = data.no2[i][0].slice(8, 10)
                    //     var hour = data.no2[i][0].slice(11,13)
                    //     var minute = data.no2[i][0].slice(14,16)
                    //     var second = data.no2[i][0].slice(17,18)
                    //     data.no2[i][0]=Date.UTC(year,month,day,hour,minute, second) 
                    //         }
                    for (var i=0; i<data.o3.length; i++){
                        var year = data.o3[i][0].slice(0, 4)
                        var month = parseInt(data.o3[i][0].slice(5, 7))-1
                        var day = data.o3[i][0].slice(8, 10)
                        var hour = data.o3[i][0].slice(11,13)
                        var minute = data.o3[i][0].slice(14,16)
                        var second = data.o3[i][0].slice(17,18)
                        data.o3[i][0]=Date.UTC(year,month,day,hour,minute, second) 
                            }
                    // for (var i=0; i<data.tvoc.length; i++){
                    //     var year = data.tvoc[i][0].slice(0, 4)
                    //     var month = parseInt(data.tvoc[i][0].slice(5, 7))-1
                    //     var day = data.tvoc[i][0].slice(8, 10)
                    //     var hour = data.tvoc[i][0].slice(11,13)
                    //     var minute = data.tvoc[i][0].slice(14,16)
                    //     var second = data.tvoc[i][0].slice(17,18)
                    //     data.tvoc[i][0]=Date.UTC(year,month,day,hour,minute, second) 
                    //         }
                    for (var i=0; i<data.luzuv.length; i++){
                        var year = data.luzuv[i][0].slice(0, 4)
                        var month = parseInt(data.luzuv[i][0].slice(5, 7))-1
                        var day = data.luzuv[i][0].slice(8, 10)
                        var hour = data.luzuv[i][0].slice(11,13)
                        var minute = data.luzuv[i][0].slice(14,16)
                        var second = data.luzuv[i][0].slice(17,18)
                        data.luzuv[i][0]=Date.UTC(year,month,day,hour,minute, second) 
                            }
                    for (var i=0; i<data.c3h8.length; i++){
                        var year = data.c3h8[i][0].slice(0, 4)
                        var month = parseInt(data.c3h8[i][0].slice(5, 7))-1
                        var day = data.c3h8[i][0].slice(8, 10)
                        var hour = data.c3h8[i][0].slice(11,13)
                        var minute = data.c3h8[i][0].slice(14,16)
                        var second = data.c3h8[i][0].slice(17,18)
                        data.c3h8[i][0]=Date.UTC(year,month,day,hour,minute, second) 
                            }
            //        Highcharts.chart('grafica_temperatura', {
            //         chart: {
            //             zoomType: 'x'
            //         },
            //         title: {
            //             text: 'Temperatura °C'
            //         },
            //         subtitle: {
            //             text: document.ontouchstart === undefined ?
            //                     'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
            //         },
            //         xAxis: {
            //             type: 'datetime',
            //             labels: {
            //               format: '{value:%l:%M %p}'
            //             }
                        
            //         },
                    
            //         yAxis: {
            //             title: {
            //                 text: 'Temperatura °C'
            //             }
            //         },
            //         legend: {
            //             enabled: false
            //         },
            //         plotOptions: {
            //             area: {
            //                 fillColor: {
            //                     linearGradient: {
            //                         x1: 0,
            //                         y1: 0,
            //                         x2: 0,
            //                         y2: 1
            //                     },
            //                     stops: [
            //                         [0, Highcharts.getOptions().colors[0]],
            //                         [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
            //                     ]
            //                 },
            //                 marker: {
            //                     radius: 2
            //                 },
            //                 lineWidth: 1,
            //                 states: {
            //                     hover: {
            //                         lineWidth: 1
            //                     }
            //                 },
            //                 threshold: null
            //             }
            //         },
        
            //         time: {
            //             timezone: 'America/Bogota'
            //         },
                    
            //         series: [{
            //             type: 'area',
            //             name: 'Temperatura',
            //             data: data.temperatura,
            //                 }]
            //     }); //fin temperatura


            //        // humedad
            //        Highcharts.chart('grafica_humedad', {
            //         chart: {
            //             zoomType: 'x'
            //         },
            //         title: {
            //             text: 'Humedad %'
            //         },
            //         subtitle: {
            //             text: document.ontouchstart === undefined ?
            //                     'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
            //         },
            //         xAxis: {
            //             type: 'datetime',
                        
            //         },
                    
            //         yAxis: {
            //             title: {
            //                 text: 'Humedad %'
            //             }
            //         },
            //         legend: {
            //             enabled: false
            //         },
            //         plotOptions: {
            //             area: {
            //                 fillColor: {
            //                     linearGradient: {
            //                         x1: 0,
            //                         y1: 0,
            //                         x2: 0,
            //                         y2: 1
            //                     },
            //                     stops: [
            //                         [0, Highcharts.getOptions().colors[0]],
            //                         [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
            //                     ]
            //                 },
            //                 marker: {
            //                     radius: 2
            //                 },
            //                 lineWidth: 1,
            //                 states: {
            //                     hover: {
            //                         lineWidth: 1
            //                     }
            //                 },
            //                 threshold: null
            //             }
            //         },
        
            //         time: {
            //             timezone: 'America/Bogota'
            //         },
                    
            //         series: [{
            //             type: 'area',
            //             name: 'Humedad',
            //             data: data.humedad,
            //                 }]
            //     }); //fin humedad


            //     // presion
            //     Highcharts.chart('grafica_presion', {
            //     chart: {
            //         zoomType: 'x'
            //     },
            //     title: {
            //         text: 'Presión Atmosférica mbar '
            //     },
            //     subtitle: {
            //         text: document.ontouchstart === undefined ?
            //                 'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
            //     },
            //     xAxis: {
            //         type: 'datetime',
                    
            //     },
                
            //     yAxis: {
            //         title: {
            //             text: 'mbar'
            //         }
            //     },
            //     legend: {
            //         enabled: false
            //     },
            //     plotOptions: {
            //         area: {
            //             fillColor: {
            //                 linearGradient: {
            //                     x1: 0,
            //                     y1: 0,
            //                     x2: 0,
            //                     y2: 1
            //                 },
            //                 stops: [
            //                     [0, Highcharts.getOptions().colors[0]],
            //                     [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
            //                 ]
            //             },
            //             marker: {
            //                 radius: 2
            //             },
            //             lineWidth: 1,
            //             states: {
            //                 hover: {
            //                     lineWidth: 1
            //                 }
            //             },
            //             threshold: null
            //         }
            //     },

            //     time: {
            //         timezone: 'America/Bogota'
            //     },
                
            //     series: [{
            //         type: 'area',
            //         name: 'Presion',
            //         data: data.presion, 
            //             }]
            // }); //fin presion


                // CO
                Highcharts.chart('grafica_CO', {
                    chart: {
                        zoomType: 'x'
                    },
                    title: {
                        text: 'Monóxido de carbono '
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
                            text: 'ppm'
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
                        name: 'CO',
                        data: data.co,
                            }]
                }); //fin CO

                // // dioxido de carbono
                // Highcharts.chart('grafica_CO2', {
                //     chart: {
                //         zoomType: 'x'
                //     },
                //     title: {
                //         text: 'Dióxido de carbono'
                //     },
                //     subtitle: {
                //         text: document.ontouchstart === undefined ?
                //                 'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
                //     },
                //     xAxis: {
                //         type: 'datetime',
                        
                //     },
                    
                //     yAxis: {
                //         title: {
                //             text: 'ppm'
                //         }
                //     },
                //     legend: {
                //         enabled: false
                //     },
                //     plotOptions: {
                //         area: {
                //             fillColor: {
                //                 linearGradient: {
                //                     x1: 0,
                //                     y1: 0,
                //                     x2: 0,
                //                     y2: 1
                //                 },
                //                 stops: [
                //                     [0, Highcharts.getOptions().colors[0]],
                //                     [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                //                 ]
                //             },
                //             marker: {
                //                 radius: 2
                //             },
                //             lineWidth: 1,
                //             states: {
                //                 hover: {
                //                     lineWidth: 1
                //                 }
                //             },
                //             threshold: null
                //         }
                //     },
    
                //     time: {
                //         timezone: 'America/Bogota'
                //     },
                    
                //     series: [{
                //         type: 'area',
                //         name: 'CO2',
                //         data: data.co2,
                //             }]
                // }); //fin dioxido de carbono

                // metano
                Highcharts.chart('grafica_CH4', {
                    chart: {
                        zoomType: 'x'
                    },
                    title: {
                        text: 'Metano CH4'
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
                            text: 'ppm'
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
                        name: 'metano',
                        data: data.ch4,
                            }]
                }); //fin metano

                // material paraticulado
                // Highcharts.chart('grafica_PM', {
                //     chart: {
                //         zoomType: 'x'
                //     },
                //     title: {
                //         text: 'PM2.5-PM10'
                //     },
                //     subtitle: {
                //         text: document.ontouchstart === undefined ?
                //                 'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
                //     },
                //     xAxis: {
                //         type: 'datetime',
                        
                //     },
                    
                //     yAxis: {
                //         title: {
                //             text: 'ug/m^3'
                //         }
                //     },
                //     legend: {
                //         enabled: false
                //     },
                //     plotOptions: {
                //         area: {
                //             fillColor: {
                //                 linearGradient: {
                //                     x1: 0,
                //                     y1: 0,
                //                     x2: 0,
                //                     y2: 1
                //                 },
                //                 stops: [
                //                     [0, Highcharts.getOptions().colors[0]],
                //                     [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                //                 ]
                //             },
                //             marker: {
                //                 radius: 2
                //             },
                //             lineWidth: 1,
                //             states: {
                //                 hover: {
                //                     lineWidth: 1
                //                 }
                //             },
                //             threshold: null
                //         }
                //     },
    
                //     time: {
                //         timezone: 'America/Bogota'
                //     },
                    
                //     series: [{
                //         type: 'area',
                //         name: 'PM',
                //         data: data.presion,
                //             }]
                // }); //fin material particulado

                // // polvo
                // Highcharts.chart('grafica_polvo', {
                //     chart: {
                //         zoomType: 'x'
                //     },
                //     title: {
                //         text: 'Polvo'
                //     },
                //     subtitle: {
                //         text: document.ontouchstart === undefined ?
                //                 'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
                //     },
                //     xAxis: {
                //         type: 'datetime',
                        
                //     },
                    
                //     yAxis: {
                //         title: {
                //             text: 'mg/m^3'
                //         }
                //     },
                //     legend: {
                //         enabled: false
                //     },
                //     plotOptions: {
                //         area: {
                //             fillColor: {
                //                 linearGradient: {
                //                     x1: 0,
                //                     y1: 0,
                //                     x2: 0,
                //                     y2: 1
                //                 },
                //                 stops: [
                //                     [0, Highcharts.getOptions().colors[0]],
                //                     [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                //                 ]
                //             },
                //             marker: {
                //                 radius: 2
                //             },
                //             lineWidth: 1,
                //             states: {
                //                 hover: {
                //                     lineWidth: 1
                //                 }
                //             },
                //             threshold: null
                //         }
                //     },
    
                //     time: {
                //         timezone: 'America/Bogota'
                //     },
                    
                //     series: [{
                //         type: 'area',
                //         name: 'polvo',
                //         data: data.polvo,
                //             }]
                // }); //fin polvo

                // velocidad_viento
                // Highcharts.chart('grafica_velocidad_viento', {
                //     chart: {
                //         zoomType: 'x'
                //     },
                //     title: {
                //         text: 'Velocidad viento'
                //     },
                //     subtitle: {
                //         text: document.ontouchstart === undefined ?
                //                 'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
                //     },
                //     xAxis: {
                //         type: 'datetime',
                        
                //     },
                    
                //     yAxis: {
                //         title: {
                //             text: 'm/s'
                //         }
                //     },
                //     legend: {
                //         enabled: false
                //     },
                //     plotOptions: {
                //         area: {
                //             fillColor: {
                //                 linearGradient: {
                //                     x1: 0,
                //                     y1: 0,
                //                     x2: 0,
                //                     y2: 1
                //                 },
                //                 stops: [
                //                     [0, Highcharts.getOptions().colors[0]],
                //                     [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                //                 ]
                //             },
                //             marker: {
                //                 radius: 2
                //             },
                //             lineWidth: 1,
                //             states: {
                //                 hover: {
                //                     lineWidth: 1
                //                 }
                //             },
                //             threshold: null
                //         }
                //     },
    
                //     time: {
                //         timezone: 'America/Bogota'
                //     },
                    
                //     series: [{
                //         type: 'area',
                //         name: 'viento',
                //         data: data.presion,
                //             }]
                // }); //fin velociadad_viento

                // // SO2
                // Highcharts.chart('grafica_SO2', {
                //     chart: {
                //         zoomType: 'x'
                //     },
                //     title: {
                //         text: 'Dióxido de azufre SO2'
                //     },
                //     subtitle: {
                //         text: document.ontouchstart === undefined ?
                //                 'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
                //     },
                //     xAxis: {
                //         type: 'datetime',
                        
                //     },
                    
                //     yAxis: {
                //         title: {
                //             text: 'ppm'
                //         }
                //     },
                //     legend: {
                //         enabled: false
                //     },
                //     plotOptions: {
                //         area: {
                //             fillColor: {
                //                 linearGradient: {
                //                     x1: 0,
                //                     y1: 0,
                //                     x2: 0,
                //                     y2: 1
                //                 },
                //                 stops: [
                //                     [0, Highcharts.getOptions().colors[0]],
                //                     [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                //                 ]
                //             },
                //             marker: {
                //                 radius: 2
                //             },
                //             lineWidth: 1,
                //             states: {
                //                 hover: {
                //                     lineWidth: 1
                //                 }
                //             },
                //             threshold: null
                //         }
                //     },
    
                //     time: {
                //         timezone: 'America/Bogota'
                //     },
                    
                //     series: [{
                //         type: 'area',
                //         name: 'SO2',
                //         data: data.so2,
                //             }]
                // }); //fin dioxido de azufre

                // // NO2
                // Highcharts.chart('grafica_NO2', {
                //     chart: {
                //         zoomType: 'x'
                //     },
                //     title: {
                //         text: 'Dióxido de Nitrógeno NO2'
                //     },
                //     subtitle: {
                //         text: document.ontouchstart === undefined ?
                //                 'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
                //     },
                //     xAxis: {
                //         type: 'datetime',
                        
                //     },
                    
                //     yAxis: {
                //         title: {
                //             text: 'ppm'
                //         }
                //     },
                //     legend: {
                //         enabled: false
                //     },
                //     plotOptions: {
                //         area: {
                //             fillColor: {
                //                 linearGradient: {
                //                     x1: 0,
                //                     y1: 0,
                //                     x2: 0,
                //                     y2: 1
                //                 },
                //                 stops: [
                //                     [0, Highcharts.getOptions().colors[0]],
                //                     [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                //                 ]
                //             },
                //             marker: {
                //                 radius: 2
                //             },
                //             lineWidth: 1,
                //             states: {
                //                 hover: {
                //                     lineWidth: 1
                //                 }
                //             },
                //             threshold: null
                //         }
                //     },
    
                //     time: {
                //         timezone: 'America/Bogota'
                //     },
                    
                //     series: [{
                //         type: 'area',
                //         name: 'NO2',
                //         data: data.no2,
                //             }]
                // }); //fin NO2

                // O3
                Highcharts.chart('grafica_O3', {
                    chart: {
                        zoomType: 'x'
                    },
                    title: {
                        text: 'Ozono O3'
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
                            text: 'ppm'
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
                        name: 'O3',
                        data: data.o3,
                            }]
                }); //fin O3

                // // compuestos organicos volatiles
                // Highcharts.chart('grafica_compuesto_organico', {
                //     chart: {
                //         zoomType: 'x'
                //     },
                //     title: {
                //         text: 'Compuestos orgánicos volátiles TVOC'
                //     },
                //     subtitle: {
                //         text: document.ontouchstart === undefined ?
                //                 'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
                //     },
                //     xAxis: {
                //         type: 'datetime',
                        
                //     },
                    
                //     yAxis: {
                //         title: {
                //             text: 'ppm'
                //         }
                //     },
                //     legend: {
                //         enabled: false
                //     },
                //     plotOptions: {
                //         area: {
                //             fillColor: {
                //                 linearGradient: {
                //                     x1: 0,
                //                     y1: 0,
                //                     x2: 0,
                //                     y2: 1
                //                 },
                //                 stops: [
                //                     [0, Highcharts.getOptions().colors[0]],
                //                     [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                //                 ]
                //             },
                //             marker: {
                //                 radius: 2
                //             },
                //             lineWidth: 1,
                //             states: {
                //                 hover: {
                //                     lineWidth: 1
                //                 }
                //             },
                //             threshold: null
                //         }
                //     },
    
                //     time: {
                //         timezone: 'America/Bogota'
                //     },
                    
                //     series: [{
                //         type: 'area',
                //         name: 'TVOC',
                //         data: data.tvoc,
                //             }]
                // }); //fin Compuestos organicos volatiles

                // UV
                Highcharts.chart('grafica_UV', {
                    chart: {
                        zoomType: 'x'
                    },
                    title: {
                        text: 'Luz Ultravioleta 300~360 nm'
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
                            text: 'mW/cm^2'
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
                        name: 'UV',
                        data: data.luzuv,
                            }]
                }); //fin UV

                // LPG
                Highcharts.chart('grafica_propano', {
                    chart: {
                        zoomType: 'x'
                    },
                    title: {
                        text: 'Gases inflamables'
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
                            text: 'ppm'
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
                        name: 'propano',
                        data: data.c3h8,
                            }]
                }); //LPG

           } //fin success
        }); // fin ajax

}); //document ready