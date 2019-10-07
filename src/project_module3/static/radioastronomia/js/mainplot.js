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


function getRandomColor() {
  var letters = '0123456789ABCDEF';
  var color = '#';
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}

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

    for(i=0; i<= Object.keys(response).length-1; i++){
        var color = "#000";
        
        idatasets.push({data: [],
                  backgroundColor: colors[i],
                  borderColor: colors[i],
                  borderWidth:1,
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

var pp = 1 
function pusher(response){
    
    var fulldate = response["Date"]
    var units    = response["units"]
    var response = response["wheather"]

    document.getElementById("winfo").innerHTML = "Mediciones Actuales "+fulldate[0]+" "+fulldate[1];
    var count = pp++
    ll.push(count);
    for(i=0; i<=Object.keys(response).length-1; i++){

        MainChart.data.datasets[i].data.push({x: count,y:Object.values(response)[i]})
        var currentdata = document.createTextNode(Object.keys(response)[i] +": "+ Object.values(response)[i]+" "+units[i])
        item = document.getElementById("cvalues").childNodes[i]
        item.replaceChild(currentdata, item.childNodes[0])
    }

    if(pp>31){
        for(i=0; i<=Object.keys(response).length-1; i++){
            MainChart.data.datasets[i].data.shift()
        }
        MainChart.data.labels.shift();
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
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }],
            xAxes: [{
                scaleLabel:{
                    display: true,
                }
            }]
        }
    }
});






