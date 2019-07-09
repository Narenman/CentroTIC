       $.ajax({
            type: "GET",
            url: "/app_praes/variables-json/",
            data: {},
            dataType: 'json',
            success: function (data){
                   // conversion de los datos del tiempo a epoch
                     for (var i=0; i<data.temperatura.length; i++){
                         var year = data.temperatura[i][0].slice(0, 4)
                         var month = parseInt(data.temperatura[i][0].slice(5, 7))-1
                         var day = data.temperatura[i][0].slice(8, 10)
                         var hour = data.temperatura[i][0].slice(11,13)
                         var minute = data.temperatura[i][0].slice(14,16)
                         var second = data.temperatura[i][0].slice(17,18)
                         data.temperatura[i][0]=Date.UTC(year,month,day,hour,minute, second) 
                             }
                     for (var i=0; i<data.humedad.length; i++){
                         var year = data.humedad[i][0].slice(0, 4)
                         var month = parseInt(data.humedad[i][0].slice(5, 7))-1
                         var day = data.humedad[i][0].slice(8, 10)
                         var hour = data.humedad[i][0].slice(11,13)
                         var minute = data.humedad[i][0].slice(14,16)
                         var second = data.humedad[i][0].slice(17,18)
                         data.humedad[i][0]=Date.UTC(year,month,day,hour,minute, second) 
                             }
                     for (var i=0; i<data.presion.length; i++){
                         var year = data.presion[i][0].slice(0, 4)
                         var month = parseInt(data.presion[i][0].slice(5, 7))-1
                         var day = data.presion[i][0].slice(8, 10)
                         var hour = data.presion[i][0].slice(11,13)
                         var minute = data.presion[i][0].slice(14,16)
                         var second = data.presion[i][0].slice(17,18)
                         data.presion[i][0]=Date.UTC(year,month,day,hour,minute, second) 
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
                         labels: {
                           format: '{value:%l:%M %p}'
                         }
                        
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
                 }); //fin temperatura


                    // humedad
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
                             text: 'Humedad %'
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
                 }); //fin humedad


            // //     // presion
            // //     Highcharts.chart('grafica_presion', {
            // //     chart: {
            // //         zoomType: 'x'
            // //     },
            // //     title: {
            // //         text: 'Presión Atmosférica mbar '
            // //     },
            // //     subtitle: {
            // //         text: document.ontouchstart === undefined ?
            // //                 'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
            // //     },
            // //     xAxis: {
            // //         type: 'datetime',
                    
            // //     },
                
            // //     yAxis: {
            // //         title: {
            // //             text: 'mbar'
            // //         }
            // //     },
            // //     legend: {
            // //         enabled: false
            // //     },
            // //     plotOptions: {
            // //         area: {
            // //             fillColor: {
            // //                 linearGradient: {
            // //                     x1: 0,
            // //                     y1: 0,
            // //                     x2: 0,
            // //                     y2: 1
            // //                 },
            // //                 stops: [
            // //                     [0, Highcharts.getOptions().colors[0]],
            // //                     [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
            // //                 ]
            // //             },
            // //             marker: {
            // //                 radius: 2
            // //             },
            // //             lineWidth: 1,
            // //             states: {
            // //                 hover: {
            // //                     lineWidth: 1
            // //                 }
            // //             },
            // //             threshold: null
            // //         }
            // //     },

            // //     time: {
            // //         timezone: 'America/Bogota'
            // //     },
                
            // //     series: [{
            // //         type: 'area',
            // //         name: 'Presion',
            // //         data: data.presion, 
            // //             }]
            // // }); //fin presion

           } //fin success
        }); // fin ajax


// function callAjax(){
//     $.ajax({
//         type: "GET",
//         url: "/app_praes/json-temperatura/",
//         data: {},
//         dataType: 'json',
//         success: function (data){
//                // conversion de los datos del tiempo a epoch
                 
//                      var year = data.temperatura[1].slice(0, 4)
//                      var month = parseInt(data.temperatura[1].slice(5, 7))-1
//                      var day = data.temperatura[1].slice(8, 10)
//                      var hour = data.temperatura[1].slice(11,13)
//                      var minute = data.temperatura[1].slice(14,16)
//                      var second = data.temperatura[1].slice(17,18)
//                      data.temperatura[1]=Date.UTC(year,month,day,hour,minute, second) 
                                      
//                 Highcharts.chart('container', {
//                  chart: {
//                      zoomType: 'x'
//                  },
//                  title: {
//                      text: 'Temperatura °C'
//                  },
//                  subtitle: {
//                      text: document.ontouchstart === undefined ?
//                              'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
//                  },
//                  xAxis: {
//                      type: 'datetime',
//                      labels: {
//                        format: '{value:%l:%M %p}'
//                      }
                    
//                  },
                
//                  yAxis: {
//                      title: {
//                          text: 'Temperatura °C'
//                      }
//                  },
//                  legend: {
//                      enabled: false
//                  },
//                  plotOptions: {
//                      area: {
//                          fillColor: {
//                              linearGradient: {
//                                  x1: 0,
//                                  y1: 0,
//                                  x2: 0,
//                                  y2: 1
//                              },
//                              stops: [
//                                  [0, Highcharts.getOptions().colors[0]],
//                                  [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
//                              ]
//                          },
//                          marker: {
//                              radius: 2
//                          },
//                          lineWidth: 1,
//                          states: {
//                              hover: {
//                                  lineWidth: 1
//                              }
//                          },
//                          threshold: null
//                      }
//                  },
    
//                  time: {
//                      timezone: 'America/Bogota'
//                  },
 

//                  series: [{
//                       type: 'area',
//                       name: 'Temperatura',
//                       data: data.temperatura,
//                           }]
                        
//              }); //fin temperatura
//              interval = setTimeout(callAjax, 1000);

//             } //fin success
//         }); //fin ajax
//     }
//     callAjax()




//////
 var defaultData = 'https://demo-live-data.highcharts.com/time-data.csv';
// //var defaultData = "http://127.0.0.1:8080/app_praes/json-temperatura/"
// var pollingInput = document.getElementById('pollingTime');

 function createChart() {
     Highcharts.chart('container', {
         chart: {
             type: 'spline'
         },
         title: {
             text: 'Live Data'
         },
         data: {
             csvURL: defaultData,
             enablePolling: true,
             dataRefreshRate: 1,
         }
     });
 }

 createChart();
