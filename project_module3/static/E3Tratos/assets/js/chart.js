var ctx = document.getElementById("myChart").getContext('2d');


    // body...
    var chart = new Chart(ctx, {
    type: 'line',
    data: {
        
        labels: [1, 2, 3, 4, 5, 6, 7, 8, 9],
        
        datasets: [{
            label: 'Temp',
            data: [1, 2, 3, 4, 5, 6, 3, 2, 1],
            yAxisID: 'y-axis-1',
            fill: false,       
            backgroundColor: ['rgba(223,232,141,1)'],
            borderColor: ['rgba(223,232,141,1)'],
            borderWidth: 1,
            showLine: true
        },{ 
            label: "Presure",
            data:[1, 2, 3, 4, 5, 6, 3, 2, 1],
            yAxisID: 'y-axis-2',
            fill: false,
            backgroundColor: ['rgba(25,105,1,1)'],
            borderColor: ['rgba(1,7,11,0)'],
            borderWidth: 1
            }]
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
                id: 'y-axis-1'},

                {
                type: 'linear',
                display: 'true',
                gridLines:{
                    display: false
                },
                ticks:{
                    fontColor: '#00b4ff',
                },
                position: 'right',
                id: 'y-axis-2',                    
                }]
        }
    }
});