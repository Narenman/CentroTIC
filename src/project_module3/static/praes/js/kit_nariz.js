function range(start, stop, step) {
    var a = [start], b = start;
    while (b < stop) {
        a.push(b += step || 1);
    }
    return a;
}

function sendRequest(){
$.ajax({
        type: "GET",
        url: "/app_praes/modo-nariz/",
        dataType: 'json',
        success: function (data){
        var xaxes = range(0,1*data.S1.length,1)
        var ctx = document.getElementById('grafica_nariz');
        let chart = new Chart(ctx, {
            type: 'line',
            data: {
                datasets: [{
                    label: 'S1',
                    data: data.S1,
                    fill: false,
                    backgroundColor: ['#f44336'],
                    borderColor: ['#f44336'],
                },
                {   label: 'S2',
                    data: data.S2,
                    fill: false,
                     backgroundColor: ['#f49a07'],
                    borderColor: ['#f49a07'],
                },
                {   label: 'S3',
                    data: data.S3,
                    fill: false,
                     backgroundColor: ['#ccf407'],
                    borderColor: ['#ccf407'],
                },
                {   label: 'S4',
                    data: data.S4,
                    fill: false,
                     backgroundColor: ['#20f407'],
                    borderColor: ['#20f407'],
                },
                
                ],
                labels: xaxes
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            suggestedMin: 50,
                            suggestedMax: 100
                        }
                    }]
                }
            }
        });

       
        }//fin success
    
    }); // fin ajax

}

setInterval(sendRequest, 1000)
