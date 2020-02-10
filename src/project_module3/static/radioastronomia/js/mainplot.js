var ctx = document.getElementById('myChart').getContext('2d');
var iresponse;

var idatasets = [];

var xhttp = new XMLHttpRequest();
xhttp.responseType = "json";

xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {

    iresponse = this.response;
    constructor(iresponse);
    }

};


xhttp.open("GET", "/radioastronomia/monitoreo-ambiental", true);
xhttp.send(); 

function getter(){
    var xhttp = new XMLHttpRequest();
    xhttp.responseType = "json";

    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {

            iresponse = this.response;
            pusher(iresponse)
        }
    };

    xhttp.open("GET", "/radioastronomia/monitoreo-ambiental", true);
    xhttp.send(); 
    setTimeout(getter, 3000)
}

getter();

function constructor(response){
    
    var colors   = response["colors"]
    var units    = response["units"]
    var response = response["wheather"]
    var id       = response["id"]

    for(i=0; i<= Object.keys(response).length-1; i++){
        var color = "#000";
        
        idatasets.push({data: [],
                        backgroundColor:colors[i],
                        borderColor: colors[i],
                        borderWidth: 2,
                        pointRadius: 1.5,
                        hoverRadius: 2,
                        pointHitRadius: 10,
                        fill: false,
                  label: Object.keys(response)[i]})

        var nodevalue = document.createElement("div");
        var currentdata = document.createTextNode(Object.keys(response)[i] +": "+ Object.values(response)[i]+" "+units[i])
        nodevalue.appendChild(currentdata)
        document.getElementById("cvalues").appendChild(nodevalue)
    }


    MainChart.update()
}

var ll = [];

var pp = 0 
function pusher(response){
    var id       = response["id"]
    var fulldate = response["Date"]
    var units    = response["units"]
    var response = response["wheather"]
    
    

    var c = pp++
    for(i=0; i<=Object.keys(response).length-1; i++){
        
        MainChart.data.datasets[i].data.push({x: new Date(),y:Object.values(response)[i]})
        var currentdata = document.createTextNode(Object.keys(response)[i] +": "+ Object.values(response)[i]+" "+units[i])
        item = document.getElementById("cvalues").childNodes[i]
        item.replaceChild(currentdata, item.childNodes[0])
        var muestra = MainChart.data.datasets[i].data.length;
        document.getElementById("winfo").innerHTML = " Muestras totales: "+ id +"<br>"+ " Muestras Actuales: " + c + "<br>"+"Tiempo de muestra: "+fulldate;
    }
    

    if(pp>51){
        for(i=0; i<=Object.keys(response).length-1; i++){
            MainChart.data.datasets[i].data.shift()

        }

    }
    MainChart.update()
}

// MainChart.defaults.line.spanGaps = true;

 var MainChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ll,
        datasets: idatasets
           },
    options: {
        responsive: true,
        title: {
            display: false,
            text: '',
        },
        scales: {
             xAxes: [{
                type: 'time',
                time: {
                    parser: 'MM/DD/YYYY HH:mm',
                    // round: 'day'
                    tooltipFormat: 'll HH:mm'
                },
                scaleLabel: {
                    display: true,
                    labelString: 'Fecha'
                }
			 	}],

            yAxes: [{
                type: 'linear',
                display: 'true',
                gridLines:{
                    display: true
                    },
                ticks:{
                    fontColor: '#000',
                    autoSkip: true
                    },
                position: 'left',
                id: 'y-axis-1'}
                ]
            }
        }
});






