/*Este archivo se encarga de administrar el el analisis 
temporal por cada banda espectral */

console.log(csrftoken);

function sendForm(){
    
    var formElement = document.getElementById("form_modo2")
    // en caso de querer agregar informacion extra
    formData = new FormData(formElement)
    // formData.append(csrftoken); //esto es informacion extra

    var xhr = new XMLHttpRequest();
    xhr.open("POST","/radioastronomia/grafica/tiempo-banda", false)
    xhr.send(formData)

    if (xhr.status==200){
        
        //esta variable lee lo que viene del servidor
        stateobject = xhr.response;
        stateobject = JSON.parse(stateobject);
        espectrograma = stateobject.espectrograma
        energia = stateobject.energia
        caracteristica = stateobject.caracteristica
        tiempo = stateobject.tiempo

        for(var i=0; i<espectrograma.length; i++){

            var year = espectrograma[i][0].slice(0,2)
            var month = parseInt(espectrograma[i][0].slice(3,5))-1
            var day = espectrograma[i][0].slice(6,8)
            var hour = espectrograma[i][0].slice(9,11)
            var minute = espectrograma[i][0].slice(12,14)
            var second = espectrograma[i][0].slice(15,17)
            espectrograma[i][0] = Date.UTC(year, month, day, hour, minute, second)
        }

        console.log(espectrograma[0])

        for(var i=0; i<energia.length; i++){

            var year = energia[i][0].slice(0,2)
            var month = parseInt(energia[i][0].slice(3,5))-1
            var day = energia[i][0].slice(6,8)
            var hour = energia[i][0].slice(9,11)
            var minute = energia[i][0].slice(12,14)
            var second = energia[i][0].slice(15,17)
            energia[i][0] = Date.UTC(year, month, day, hour, minute, second)
        }

        // for (var i=0; i<tiempo.length; i++){
        //     var year = tiempo[i].slice(0,2)
        //     var month = parseInt(tiempo[i].slice(3,5))-1
        //     var day = tiempo[i].slice(6,8)
        //     var hour = tiempo[i].slice(9,11)
        //     var minute = tiempo[i].slice(12,14)
        //     var second = tiempo[i].slice(15,17)
        //     tiempo[i] = Date.UTC(year, month, day, hour, minute, second)
        // }


        //inicio de espectrograma
        // Highcharts.chart('espectrograma', {

        //     chart: {
        //         type: 'heatmap',
        //         marginTop: 40,
        //         marginBottom: 80,
        //         plotBorderWidth: 1
        //     },
        
        
        //     title: {
        //         text: 'Espectrograma'
        //     },
        
        //     xAxis: {
        //     title:{text:"Frecuencia MHz"},
        //         //categories: ['Alexander', 'Marie', 'Maximilian', 'Sophia', 'Lukas', 'Maria', 'Leon', 'Anna', 'Tim', 'Laura']
        //     },
        
        //     yAxis: {
        //         //categories: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
        //         title: {text:"Tiempo"},
        //        // type:"datetime",
        //     },
        
        //     colorAxis: {
        //         min: 0,
        //         minColor: '#FFFFFF',
        //         maxColor: Highcharts.getOptions().colors[0]
        //     },
        
        //     legend: {
        //         align: 'right',
        //         layout: 'vertical',
        //         margin: 0,
        //         verticalAlign: 'top',
        //         y: 25,
        //         symbolHeight: 280
        //     },
        
        //     tooltip: {
        //         formatter: function () {
        //             return '<b>' + this.series.xAxis.categories[this.point.x] + '</b> sold <br><b>' +
        //                 this.point.value + '</b> items on <br><b>' + this.series.yAxis.categories[this.point.y] + '</b>';
        //         }
        //     },
        
        //     series: [{
        //         name: 'Sales per employee',
        //         borderWidth: 1,
        //         data:espectrograma,
        //         // data: [[10, 20, 10], [0, 0, 19], [0,5, 8], [0, 6, 24], [0, 7, 67], [9, 15, 91]],
        //         dataLabels: {
        //             enabled: false,
        //             color: '#000000'
        //         }
        //     }]
        
        // });




        Highcharts.chart('espectrograma', {

            //data: {
            //    csv: document.getElementById('csv').innerHTML
           // },
        
            chart: {
                type: 'heatmap',
                margin: [60, 10, 80, 50]
            },
        
            boost: {
                useGPUTranslations: true
            },
        
            title: {
                text: 'Highcharts heat map',
                align: 'left',
                x: 40
            },
        
            subtitle: {
                text: 'Temperature variation by day and hour through 2017',
                align: 'left',
                x: 40
            },
        
            xAxis: {
                type: 'datetime',
                min: Date.UTC(2019, 7, 1),
                max: Date.UTC(2019, 9, 1, 23, 59, 59),
                labels: {
                    align: 'left',
                    format: '{value:%d}' // long month
                },
                showLastLabel: false,
                tickLength: 16
            },
        
            yAxis: {
                title: {
                    text: null
                },
                labels: {
                    format: '{value}'
                },
                minPadding: 0,
                maxPadding: 0,
                startOnTick: false,
                endOnTick: false,
                //tickPositions: [0, 6, 12, 18, 24],
                tickWidth: 1,
                min: 50,
                max: 300,
                reversed: true
            },
        
            colorAxis: {
                stops: [
                    [0, '#3060cf'],
                    [0.5, '#fffbbc'],
                    [0.9, '#c4463a'],
                    [100, '#c4463a']
                ],
                min: -100,
                max: 0,
                startOnTick: false,
                endOnTick: false,
                labels: {
                    format: '{value}'
                }
            },
        
            series: [{
                data:[[Date.UTC(2019,08,01,0,2.7),50,20],[Date.UTC(2019,08,01,0,2.7),90,-20],
                [Date.UTC(2019,08,01,0,2.8),91,-20],
                [Date.UTC(2019,08,02,0,2.9),92,-4],
                [Date.UTC(2019,08,01,0,2.6),93,-10],
                [Date.UTC(2019,08,01,1,2.7),250,-40]],
                // data:espectrograma,
                boostThreshold: 100,
                borderWidth: 0,
                nullColor: '#EFEFEF',
                colsize: 24 * 36e5, // one day
                tooltip: {
                    headerFormat: 'Espectro<br/>',
                    pointFormat: '{point.x:%e %b, %Y} {point.y}:00: <b>{point.value} ℃</b>'
                },
                turboThreshold: Number.MAX_VALUE // #3404, remove after 4.0.5 release
            }]
        
        });
        

        //fin espectrograma

       //inicio grafica bandas del espectro
       Highcharts.chart('energia', {
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
            type: 'datetime',
            title:{
                text: "Tiempo"
            }
        },
        yAxis: {
            title: {
                text: 'Energia dBm'
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
            type: 'spline',
            name: 'Espectro',
            data: energia
        }]
    });
    //fin grafica bandas del espectro

    //Histograma de analisis de espectro

    Highcharts.chart('histograma', {
        chart: {
          type: 'column'
        },
        title: {
          text: 'Histogram using a column chart'
        },
        subtitle: {
          text: ''
        },
        xAxis: {
          crosshair: true
        },
        yAxis: {
          min: 0,
          title: {
            text: ''
          }
        },
        tooltip: {
          headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
          pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y:.1f}</b></td></tr>',
          footerFormat: '</table>',
          shared: true,
          useHTML: true
        },
        plotOptions: {
          column: {
            pointPadding: 0,
            borderWidth: 0,
            groupPadding: 0,
            shadow: false
          }
        },
        series: [{
          name: 'Data',
          data: caracteristica
      
        }]
      });
      

    //fin grafica del histograma
       
    }
    else{
        output.innerHTML += "Error HTTP"+ xhr.status;
    }

}

