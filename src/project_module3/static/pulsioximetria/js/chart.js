var ctx = document.getElementById("myChart").getContext('2d'); 


    // body...
    var chart = new Chart(ctx, {
    type: 'line',
    data: {
        
        labels: [],
        
        datasets: [{
            label: 'HR',
            data: [],
            yAxisID: 'y-axis-1',
            fill: false,       
            backgroundColor: ['#a31005'],
            borderColor: ['#a31005'],
            borderWidth: 1,
            showLine: true
            },

            { 
            label: "Spo2",
            data:[],
            yAxisID: 'y-axis-1',
            fill: false,
            backgroundColor: ['#495ec9'],
            borderColor: ['#495ec9'],
            borderWidth: 1
            },

                      { 
            label: "Bateria",
            data:[],
            yAxisID: 'y-axis-1',
            fill: false,
            backgroundColor: ['#4fe35e'],
            borderColor: ['#4fe35e'],
            borderWidth: 1
            },


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
                    fontColor: '#387a96',
                    },
                position: 'left',
                id: 'y-axis-1'}



                ]
            }
        }
    });
console.log("carga")

var jj = 0;

function updaterchart() {
    

    jj++
    chart.data.labels.push(fecha)
    chart.data.datasets[1-1].data.push(datohr)
    chart.data.datasets[2-1].data.push(datospo2)
    chart.data.datasets[3-1].data.push(datobateria)
    

    if (jj>50) {
        chart.data.labels.shift()
        chart.data.datasets[1-1].data.shift()
        chart.data.datasets[2-1].data.shift()
        chart.data.datasets[3-1].data.shift()
        
    }
    chart.update();



}
