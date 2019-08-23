var chart; // global
function requestData() {
    $.ajax({
        url: '/app_praes/json-aire/',
        success: function(point) {

            var year = point.temperatura[0].slice(0, 4)
            var month = parseInt(point.temperatura[0].slice(5, 7))-1
            var day = point.temperatura[0].slice(8, 10)
            var hour = point.temperatura[0].slice(11,13)
            var minute = point.temperatura[0].slice(14,16)
            var second = point.temperatura[0].slice(17,18)
            point.temperatura[0]=Date.UTC(year,month,day,hour,minute, second) 

            var series = chart.series[0];
            shift = series.data.length > 20; // shift if the series is 
                                                 // longer than 20

            // add the point
            var MQ2 = new Array(point.temperatura[0], point.temperatura[1][0])
            var MQ3 = new Array(point.temperatura[0], point.temperatura[1][1])
            var MQ4 = new Array(point.temperatura[0], point.temperatura[1][2])
            var MQ5 = new Array(point.temperatura[0], point.temperatura[1][3])
            var MQ6 = new Array(point.temperatura[0], point.temperatura[1][4])
            var MQ7 = new Array(point.temperatura[0], point.temperatura[1][5])
            var MQ8 = new Array(point.temperatura[0], point.temperatura[1][6])
            var MQ9 = new Array(point.temperatura[0], point.temperatura[1][7])
            var MQ135 = new Array(point.temperatura[0], point.temperatura[1][8])
            var MICS5524 = new Array(point.temperatura[0], point.temperatura[1][9])
            var eC02 = new Array(point.temperatura[0], point.temperatura[1][10])
            var tvoc = new Array(point.temperatura[0], point.temperatura[1][11])


            
            chart.series[0].addPoint(MQ2, true, shift);
            chart.series[1].addPoint(MQ3, true, shift);
            chart.series[2].addPoint(MQ4, true, shift);
            chart.series[3].addPoint(MQ5, true, shift);
            chart.series[4].addPoint(MQ6, true, shift);
            chart.series[5].addPoint(MQ7, true, shift);
            chart.series[6].addPoint(MQ8, true, shift);
            chart.series[7].addPoint(MQ9, true, shift);
            chart.series[8].addPoint(MQ135, true, shift);
            chart.series[9].addPoint(MICS5524, true, shift);
            chart.series[10].addPoint(eC02, true, shift);
            chart.series[11].addPoint(tvoc, true, shift);


            // call it again after one second
            setTimeout(requestData, 1000);    
        },
        cache: true
    });
}

document.addEventListener('DOMContentLoaded', function() {
    chart = Highcharts.chart('grafica_nariz', {
        chart: {
            type: 'spline',
            events: {
                load: requestData
            }
        },
        title: {
            text: 'Datos tomados en vivo'
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 100,
            maxZoom: 20 * 1000
        },
        yAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                text: 'Calidad del Aire',
                margin: 80
            }
        },
        series: [{
            name: 'MQ2',
            data: []
        },
            {name: "MQ3",
            data: []},

            {name: "MQ4",
            data: []},

            {name: "MQ5",
            data: []},

            {name: "MQ6",
            data: []},

            {name: "MQ7",
            data: []},

            {name: "MQ8",
            data: []},

            {name: "MQ9",
            data: []},

            {name: "MQ135",
            data: []},

            {name: "MICS5524",
            data: []},

            {name: "eCO2",
            data: []},

            {name: "tvoc",
            data: []},

        ]
    });        
});