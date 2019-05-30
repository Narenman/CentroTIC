$(document).ready(function(){
    // evento del click para graficar la temperatura
    $("#graficar_temp").click(function(event){
        $.ajax({
            type: "POST",
            url: "/app_praes/json-temperatura/",
            data: {},
            dataType: 'json',
            success: function (data){
                   // temperatura
                   for (var i=0; i<data.temperatura.length; i++){
                    var year = data.temperatura[i][0].slice(0, 4)
                    var month = parseInt(data.temperatura[i][0].slice(5, 7))-1
                    var day = data.temperatura[i][0].slice(8, 10)
                    var hour = data.temperatura[i][0].slice(11,13)
                    var minute = data.temperatura[i][0].slice(14,16)
                    var second = data.temperatura[i][0].slice(17,18)
                    data.temperatura[i][0]=Date.UTC(year,month,day,hour,minute, second) 
                        }
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
                        type: 'line',
                        name: 'Temperatura',
                        data: data.temperatura,
                            }]
                }); //fin temperatura
            } //fin success
            }); // fin ajax
        });

        //evento para mostrar grafica de humedad

        $("#graficar_hum").click(function(event){
            $.ajax({
                type: "POST",
                url: "/app_praes/json-humedad/",
                data: {},
                dataType: 'json',
                success: function (data){
                       // humedad
                       for (var i=0; i<data.humedad.length; i++){
                        var year = data.humedad[i][0].slice(0, 4)
                        var month = parseInt(data.humedad[i][0].slice(5, 7))-1
                        var day = data.humedad[i][0].slice(8, 10)
                        var hour = data.humedad[i][0].slice(11,13)
                        var minute = data.humedad[i][0].slice(14,16)
                        var second = data.humedad[i][0].slice(17,18)
                        data.humedad[i][0]=Date.UTC(year,month,day,hour,minute, second) 
                            }
                       Highcharts.chart('grafica_humedad', {
                        chart: {
                            zoomType: 'x'
                        },
                        title: {
                            text: 'Humedad %'
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
                                text: '%'
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
                            name: 'Humedad',
                            data: data.humedad,
                                }]
                    }); //fin humedad
                } //fin success
                }); // fin ajax
            });


            $("#graficar_pres").click(function(event){
                $.ajax({
                    type: "POST",
                    url: "/app_praes/json-presion/",
                    data: {},
                    dataType: 'json',
                    success: function (data){
                           // presion
                           for (var i=0; i<data.presion.length; i++){
                            var year = data.presion[i][0].slice(0, 4)
                            var month = parseInt(data.presion[i][0].slice(5, 7))-1
                            var day = data.presion[i][0].slice(8, 10)
                            var hour = data.presion[i][0].slice(11,13)
                            var minute = data.presion[i][0].slice(14,16)
                            var second = data.presion[i][0].slice(17,18)
                            data.presion[i][0]=Date.UTC(year,month,day,hour,minute, second) 
                                }
                           Highcharts.chart('grafica_presion', {
                            chart: {
                                zoomType: 'x'
                            },
                            title: {
                                text: 'Presion atmosferica'
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
                                    text: 'mbar'
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
                                name: 'presion',
                                data: data.presion,
                                    }]
                        }); //fin presion
                    } //fin success
                    }); // fin ajax
                }); //fin evento presion

                //inicio evento luz uv
                $("#graficar_luzuv").click(function(event){
                    $.ajax({
                        type: "POST",
                        url: "/app_praes/json-luzuv/",
                        data: {},
                        dataType: 'json',
                        success: function (data){
                               // luzuv
                               for (var i=0; i<data.luzuv.length; i++){
                                var year = data.luzuv[i][0].slice(0, 4)
                                var month = parseInt(data.luzuv[i][0].slice(5, 7))-1
                                var day = data.luzuv[i][0].slice(8, 10)
                                var hour = data.luzuv[i][0].slice(11,13)
                                var minute = data.luzuv[i][0].slice(14,16)
                                var second = data.luzuv[i][0].slice(17,18)
                                data.luzuv[i][0]=Date.UTC(year,month,day,hour,minute, second) 
                                    }
                               Highcharts.chart('grafica_luzuv', {
                                chart: {
                                    zoomType: 'x'
                                },
                                title: {
                                    text: 'Luz UV'
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
                                    type: 'line',
                                    name: 'luzuv',
                                    data: data.luzuv,
                                        }]
                            }); //fin luzuv
                        } //fin success
                        }); // fin ajax
                    }); //fin evento luzuv

                //inicio evento co
                $("#graficar_co").click(function(event){
                    $.ajax({
                        type: "POST",
                        url: "/app_praes/json-co/",
                        data: {},
                        dataType: 'json',
                        success: function (data){
                               // co
                               for (var i=0; i<data.co.length; i++){
                                var year = data.co[i][0].slice(0, 4)
                                var month = parseInt(data.co[i][0].slice(5, 7))-1
                                var day = data.co[i][0].slice(8, 10)
                                var hour = data.co[i][0].slice(11,13)
                                var minute = data.co[i][0].slice(14,16)
                                var second = data.co[i][0].slice(17,18)
                                data.co[i][0]=Date.UTC(year,month,day,hour,minute, second) 
                                    }
                               Highcharts.chart('grafica_co', {
                                chart: {
                                    zoomType: 'x'
                                },
                                title: {
                                    text: 'co'
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
                                    type: 'line',
                                    name: 'co',
                                    data: data.co,
                                        }]
                            }); //fin co
                        } //fin success
                        }); // fin ajax
                    }); //fin evento co

               //inicio evento co2
               $("#graficar_co2").click(function(event){
                $.ajax({
                    type: "POST",
                    url: "/app_praes/json-co2/",
                    data: {},
                    dataType: 'json',
                    success: function (data){
                           // co2
                           for (var i=0; i<data.co2.length; i++){
                            var year = data.co2[i][0].slice(0, 4)
                            var month = parseInt(data.co2[i][0].slice(5, 7))-1
                            var day = data.co2[i][0].slice(8, 10)
                            var hour = data.co2[i][0].slice(11,13)
                            var minute = data.co2[i][0].slice(14,16)
                            var second = data.co2[i][0].slice(17,18)
                            data.co2[i][0]=Date.UTC(year,month,day,hour,minute, second) 
                                }
                           Highcharts.chart('grafica_co2', {
                            chart: {
                                zoomType: 'x'
                            },
                            title: {
                                text: 'CO2'
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
                                type: 'line',
                                name: 'co2',
                                data: data.co2,
                                    }]
                        }); //fin co2
                    } //fin success
                    }); // fin ajax
                }); //fin evento co2

               //inicio evento ch4
               $("#graficar_ch4").click(function(event){
                $.ajax({
                    type: "POST",
                    url: "/app_praes/json-ch4/",
                    data: {},
                    dataType: 'json',
                    success: function (data){
                           // ch4
                           for (var i=0; i<data.ch4.length; i++){
                            var year = data.ch4[i][0].slice(0, 4)
                            var month = parseInt(data.ch4[i][0].slice(5, 7))-1
                            var day = data.ch4[i][0].slice(8, 10)
                            var hour = data.ch4[i][0].slice(11,13)
                            var minute = data.ch4[i][0].slice(14,16)
                            var second = data.ch4[i][0].slice(17,18)
                            data.ch4[i][0]=Date.UTC(year,month,day,hour,minute, second) 
                                }
                           Highcharts.chart('grafica_ch4', {
                            chart: {
                                zoomType: 'x'
                            },
                            title: {
                                text: 'CH4'
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
                                type: 'line',
                                name: 'ch4',
                                data: data.ch4,
                                    }]
                        }); //fin ch4
                    } //fin success
                    }); // fin ajax
                }); //fin evento ch4

               //inicio evento polvo
               $("#graficar_polvo").click(function(event){
                $.ajax({
                    type: "POST",
                    url: "/app_praes/json-polvo/",
                    data: {},
                    dataType: 'json',
                    success: function (data){
                           // polvo
                           for (var i=0; i<data.polvo.length; i++){
                            var year = data.polvo[i][0].slice(0, 4)
                            var month = parseInt(data.polvo[i][0].slice(5, 7))-1
                            var day = data.polvo[i][0].slice(8, 10)
                            var hour = data.polvo[i][0].slice(11,13)
                            var minute = data.polvo[i][0].slice(14,16)
                            var second = data.polvo[i][0].slice(17,18)
                            data.polvo[i][0]=Date.UTC(year,month,day,hour,minute, second) 
                                }
                           Highcharts.chart('grafica_polvo', {
                            chart: {
                                zoomType: 'x'
                            },
                            title: {
                                text: 'Polvo'
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
                                    text: 'mg/m^3'
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
                                name: 'polvo',
                                data: data.polvo,
                                    }]
                        }); //fin polvo
                    } //fin success
                    }); // fin ajax
                }); //fin evento polvo

               //inicio evento so2
               $("#graficar_so2").click(function(event){
                $.ajax({
                    type: "POST",
                    url: "/app_praes/json-so2/",
                    data: {},
                    dataType: 'json',
                    success: function (data){
                           // so2
                           for (var i=0; i<data.so2.length; i++){
                            var year = data.so2[i][0].slice(0, 4)
                            var month = parseInt(data.so2[i][0].slice(5, 7))-1
                            var day = data.so2[i][0].slice(8, 10)
                            var hour = data.so2[i][0].slice(11,13)
                            var minute = data.so2[i][0].slice(14,16)
                            var second = data.so2[i][0].slice(17,18)
                            data.so2[i][0]=Date.UTC(year,month,day,hour,minute, second) 
                                }
                           Highcharts.chart('grafica_so2', {
                            chart: {
                                zoomType: 'x'
                            },
                            title: {
                                text: 'SO2'
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
                                type: 'line',
                                name: 'so2',
                                data: data.so2,
                                    }]
                        }); //fin so2
                    } //fin success
                    }); // fin ajax
                }); //fin evento so2

               //inicio evento no2
               $("#graficar_no2").click(function(event){
                $.ajax({
                    type: "POST",
                    url: "/app_praes/json-no2/",
                    data: {},
                    dataType: 'json',
                    success: function (data){
                           // no2
                           for (var i=0; i<data.no2.length; i++){
                            var year = data.no2[i][0].slice(0, 4)
                            var month = parseInt(data.no2[i][0].slice(5, 7))-1
                            var day = data.no2[i][0].slice(8, 10)
                            var hour = data.no2[i][0].slice(11,13)
                            var minute = data.no2[i][0].slice(14,16)
                            var second = data.no2[i][0].slice(17,18)
                            data.no2[i][0]=Date.UTC(year,month,day,hour,minute, second) 
                                }
                           Highcharts.chart('grafica_no2', {
                            chart: {
                                zoomType: 'x'
                            },
                            title: {
                                text: 'NO2'
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
                                type: 'line',
                                name: 'no2',
                                data: data.no2,
                                    }]
                        }); //fin no2
                    } //fin success
                    }); // fin ajax
                }); //fin evento no2

               //inicio evento o3
               $("#graficar_o3").click(function(event){
                $.ajax({
                    type: "POST",
                    url: "/app_praes/json-o3/",
                    data: {},
                    dataType: 'json',
                    success: function (data){
                           // o3
                           for (var i=0; i<data.o3.length; i++){
                            var year = data.o3[i][0].slice(0, 4)
                            var month = parseInt(data.o3[i][0].slice(5, 7))-1
                            var day = data.o3[i][0].slice(8, 10)
                            var hour = data.o3[i][0].slice(11,13)
                            var minute = data.o3[i][0].slice(14,16)
                            var second = data.o3[i][0].slice(17,18)
                            data.o3[i][0]=Date.UTC(year,month,day,hour,minute, second) 
                                }
                           Highcharts.chart('grafica_o3', {
                            chart: {
                                zoomType: 'x'
                            },
                            title: {
                                text: 'O3'
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
                                type: 'line',
                                name: 'o3',
                                data: data.o3,
                                    }]
                        }); //fin o3
                    } //fin success
                    }); // fin ajax
                }); //fin evento o3

               //inicio evento tvoc
               $("#graficar_tvoc").click(function(event){
                $.ajax({
                    type: "POST",
                    url: "/app_praes/json-tvoc/",
                    data: {},
                    dataType: 'json',
                    success: function (data){
                           // tvoc
                           for (var i=0; i<data.tvoc.length; i++){
                            var year = data.tvoc[i][0].slice(0, 4)
                            var month = parseInt(data.o3[i][0].slice(5, 7))-1
                            var day = data.tvoc[i][0].slice(8, 10)
                            var hour = data.tvoc[i][0].slice(11,13)
                            var minute = data.tvoc[i][0].slice(14,16)
                            var second = data.tvoc[i][0].slice(17,18)
                            data.tvoc[i][0]=Date.UTC(year,month,day,hour,minute, second) 
                                }
                           Highcharts.chart('grafica_tvoc', {
                            chart: {
                                zoomType: 'x'
                            },
                            title: {
                                text: 'TVOC'
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
                                type: 'line',
                                name: 'tvoc',
                                data: data.tvoc,
                                    }]
                        }); //fin tvoc
                    } //fin success
                    }); // fin ajax
                }); //fin evento tvoc

               //inicio evento lpg
               $("#graficar_lpg").click(function(event){
                $.ajax({
                    type: "POST",
                    url: "/app_praes/json-lpg/",
                    data: {},
                    dataType: 'json',
                    success: function (data){
                           // lpg
                           for (var i=0; i<data.c3h8.length; i++){
                            var year = data.c3h8[i][0].slice(0, 4)
                            var month = parseInt(data.c3h8[i][0].slice(5, 7))-1
                            var day = data.c3h8[i][0].slice(8, 10)
                            var hour = data.c3h8[i][0].slice(11,13)
                            var minute = data.c3h8[i][0].slice(14,16)
                            var second = data.c3h8[i][0].slice(17,18)
                            data.c3h8[i][0]=Date.UTC(year,month,day,hour,minute, second) 
                                }
                           Highcharts.chart('grafica_lpg', {
                            chart: {
                                zoomType: 'x'
                            },
                            title: {
                                text: 'LPG'
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
                                type: 'line',
                                name: 'lpg',
                                data: data.lpg,
                                    }]
                        }); //fin lpg
                    } //fin success
                    }); // fin ajax
                }); //fin evento lpg
        }); //document ready