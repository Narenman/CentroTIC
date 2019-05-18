var ctx = document.getElementById("myChart").getContext('2d');


    // body...
    var chart = new Chart(ctx, {
    type: 'line',
    data: {
        
        labels: [],
        
        datasets: [{
            label: '1',
            data: [],
            yAxisID: 'y-axis-1',
            fill: false,       
            backgroundColor: ['#f44336'],
            borderColor: ['#f44336'],
            borderWidth: 1,
            showLine: true
            },

            { 
            label: "2",
            data:[],
            yAxisID: 'y-axis-1',
            fill: false,
            backgroundColor: ['#9c27b0'],
            borderColor: ['#9c27b0'],
            borderWidth: 1
            },

                      { 
            label: "3",
            data:[],
            yAxisID: 'y-axis-1',
            fill: false,
            backgroundColor: ['#2196f3'],
            borderColor: ['#2196f3'],
            borderWidth: 1
            },

                      { 
            label: "4",
            data:[],
            yAxisID: 'y-axis-1',
            fill: false,
            backgroundColor: ['#009688'],
            borderColor: ['#009688'],
            borderWidth: 1
            },


            { 
            label: "5",
            data:[],
            yAxisID: 'y-axis-1',
            fill: false,
            backgroundColor: ['#4caf50'],
            borderColor: ['#4caf50'],
            borderWidth: 1
            },

            { 
            label: "6",
            data:[],
            yAxisID: 'y-axis-1',
            fill: false,
            backgroundColor: ['#cddc39'],
            borderColor: ['#cddc39'],
            borderWidth: 1
            },

            { 
            label: "7",
            data:[],
            yAxisID: 'y-axis-1',
            fill: false,
            backgroundColor: ['#ff9800'],
            borderColor: ['#ff9800'],
            borderWidth: 1
            },

            { 
            label: "8",
            data:[],
            yAxisID: 'y-axis-1',
            fill: false,
            backgroundColor: ['#ff5722'],
            borderColor: ['#ff5722'],
            borderWidth: 1
            }

            ]
    },
    options: {
        responsive: true,
        title: {
            display: false,
            text: 'Temp',
        },
        scales: {
            yAxes: [{
                type: 'linear',
                display: 'true',
                gridLines:{
                    display: false
                    },
                ticks:{
                    fontColor: '#00b4ff',
                    },
                position: 'left',
                id: 'y-axis-1'}



                ]
            }
        }
    });

var jj = 0;
function updaterchart() {
    //console.log(meteorology.temperatura, mydatetime())

    chart.data.labels.push(jj++)
    chart.data.datasets[1-1].data.push(meteorology.temperatura)
    chart.data.datasets[2-1].data.push(meteorology.presion)
    chart.data.datasets[3-1].data.push(meteorology.humedad)
    chart.data.datasets[4-1].data.push(meteorology.co2)
    chart.data.datasets[5-1].data.push(meteorology.radiacion_uv)
    chart.data.datasets[6-1].data.push(meteorology.PM25)
    if (jj>10) {
        chart.data.labels.shift()
        chart.data.datasets[1-1].data.shift()
        chart.data.datasets[2-1].data.shift()
        chart.data.datasets[3-1].data.shift()
        chart.data.datasets[4-1].data.shift()
        chart.data.datasets[5-1].data.shift()
        chart.data.datasets[6-1].data.shift()
    }
    chart.update();
    


      //  console.log(Math.max(maptoint))
      //console.log("ok");
     // maxTemp.innerHTML = Math.max(maptoint)
     // minTemp.innerHTML = Math.min(maptoint)






    setTimeout(updaterchart, 1000);

}

updaterchart()