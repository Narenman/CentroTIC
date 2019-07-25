var chart; // global
function requestData() {
    $.ajax({
        url: '/app_praes/json-ph/',
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
            chart.series[0].addPoint(point.temperatura, true, shift);
            
            // call it again after one second
            setTimeout(requestData, 2000);    
        },
        cache: true
    });
}

document.addEventListener('DOMContentLoaded', function() {
    chart = Highcharts.chart('grafica_ph', {
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
            tickPixelInterval: 150,
            maxZoom: 20 * 1000
        },
        yAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                text: 'PH',
                margin: 80
            }
        },
        series: [{
            name: 'PH',
            data: []
        }]
    });        
});