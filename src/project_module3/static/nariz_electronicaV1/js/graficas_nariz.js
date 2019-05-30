function range(start, stop, step) {
    var a = [start], b = start;
    while (b < stop) {
        a.push(b += step || 1);
    }
    return a;
}
$.ajax({
        type: "GET",
        url: "/nariz_electronica/clasificar_datos",
        dataType: 'json',
        success: function (data){
        var xaxes = range(0,1*data.S1.length,1)
        var ctx = document.getElementById('myChart');
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
                {   label: 'S5',
                    data: data.S5,
                    fill: false,
                     backgroundColor: ['#4ba540'],
                    borderColor: ['#4ba540'],
                },
                {   label: 'S6',
                    data: data.S6,
                    fill: false,
                     backgroundColor: ['#f49a07'],
                    borderColor: ['#f49a07'],
                },{   label: 'S7',
                    data: data.S7,
                    fill: false,
                     backgroundColor: ['#176e0c'],
                    borderColor: ['#176e0c'],
                },
                {   label: 'S8',
                    data: data.S8,
                    fill: false,
                     backgroundColor: ['#0fd795'],
                    borderColor: ['#0fd795'],
                },
                {   label: 'S9',
                    data: data.S9,
                    fill: false,
                     backgroundColor: ['#0ac3e8'],
                    borderColor: ['#0ac3e8'],
                },
                 {   label: 'S10',
                    data: data.S10,
                    fill: false,
                     backgroundColor: ['#0a79e8'],
                    borderColor: ['#0a79e8'],
                },
                 {   label: 'S11',
                    data: data.S11,
                    fill: false,
                     backgroundColor: ['#0a28e8'],
                    borderColor: ['#0a28e8'],
                 },
                  {   label: 'S12',
                    data: data.S12,
                    fill: false,
                     backgroundColor: ['#8254eb'],
                    borderColor: ['#8254eb'],
                },
                 {   label: 'S13',
                    data: data.S13,
                    fill: false,
                     backgroundColor: ['#665787'],
                    borderColor: ['#665787'],
                },
                 {   label: 'S14',
                    data: data.S14,
                    fill: false,
                     backgroundColor: ['#a324c9'],
                    borderColor: ['#a324c9'],
                },
                 {   label: 'S15',
                    data: data.S15,
                    fill: false,
                     backgroundColor: ['#954c8f'],
                    borderColor: ['#954c8f'],
                },
                 {   label: 'S16',
                    data: data.S16,
                    fill: false,
                     backgroundColor: ['#c41d76'],
                    borderColor: ['#c41d76'],
                }
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

        }}); // fin ajax
