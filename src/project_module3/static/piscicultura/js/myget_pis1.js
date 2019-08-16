
var temp = "-"; 
var od = "-"; 
var ph = "-"; 
var tempC = "-"; 
var humC = "-"; 
var voltajeB = "-"; 
var fecha = "___"; 





function loadDoc() {

  var xhttp = new XMLHttpRequest();
  xhttp.responseType = "json";


  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {

    	//globaljson = this.response.datos;
      temp=this.response.temperatura;
      od= this.response.oxigenoDisuelto;
      ph= this.response.phTank;
      tempC= this.response.tempCaja;
      voltajeB= this.response.voltajeBat;
      humC= this.response.humCaja;

    	printer();
     
      updaterchart();
    }
  };
  xhttp.open("GET", "/piscicultura/json-last-est1/", true);

//  xhttp.open("GET", "http://192.168.0.108:8080/piscicultura/json-last-est1/", true);
  xhttp.overrideMimeType('text/xml; charset=iso-8859-1');
  xhttp.send(); 

  setTimeout(loadDoc, 1200);

}


//var i = 0;

//fecha= String(temp[0]);

 function printer(){
  
  fecha= new Date(String(temp[0]));

  document.getElementById('last_update1').innerHTML = "Última actualización: " + String(fecha.toLocaleString());
 	document.getElementById('temp_value').innerHTML = String(temp[1])+" °C";
  document.getElementById('ph_value').innerHTML = ph[1];
  document.getElementById('od_value').innerHTML = String(od[1])+" mg/L";

 	document.getElementById('tempCaja_value').innerHTML = String(tempC[1])+" °C";
  document.getElementById('humCaja_value').innerHTML = humC[1]+"%";
  document.getElementById('voltBat_value').innerHTML = String(voltajeB[1])+" V";

 }

loadDoc();


var ctx = document.getElementById("myChart").getContext('2d');

//ctx.style.minHeight="500px";
    // body...
    var chart = new Chart(ctx, {
    type: 'line',
    data: {
        
        labels: [],
        
        datasets: [{
            label: 'Temperatura',
            data: [],
            yAxisID: 'y-axis-1',
            fill: false,       
            backgroundColor: ['#f44336'],
            borderColor: ['#f44336'],
            borderWidth: 1,
            showLine: true
            },

            { 
            label: "PH",
            data:[],
            yAxisID: 'y-axis-1',
            fill: false,
            backgroundColor: ['#9c27b0'],
            borderColor: ['#9c27b0'],
            borderWidth: 1
            },

                      { 
            label: "Oxíg. Disuelto",
            data:[],
            yAxisID: 'y-axis-1',
            fill: false,
            backgroundColor: ['#2196f3'],
            borderColor: ['#2196f3'],
            borderWidth: 1
            },

                      { 
            label: "Temp. Caja",
            data:[],
            yAxisID: 'y-axis-1',
            fill: false,
            backgroundColor: ['#009688'],
            borderColor: ['#009688'],
            borderWidth: 1
            },


            { 
            label: "Hum. Caja",
            data:[],
            yAxisID: 'y-axis-1',
            fill: false,
            backgroundColor: ['#4caf50'],
            borderColor: ['#4caf50'],
            borderWidth: 1
            },

            { 
            label: "Volt. Batería",
            data:[],
            yAxisID: 'y-axis-1',
            fill: false,
            backgroundColor: ['#cddc39'],
            borderColor: ['#cddc39'],
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

//console.log("mete",outputvar(), mydatetime())
var jj = 0;
//var fecha_hora= String(temp[0]);


function updaterchart() {
    //console.log(meteorology.co2[0], mydatetime())
    jj++
    chart.data.labels.push(fecha.toLocaleTimeString())
    chart.data.datasets[1-1].data.push(temp[1])
    chart.data.datasets[2-1].data.push(ph[1])
    chart.data.datasets[3-1].data.push(od[1])
    chart.data.datasets[4-1].data.push(tempC[1])
    chart.data.datasets[5-1].data.push(humC[1])
    chart.data.datasets[6-1].data.push(voltajeB[1])


    if (jj>11) {
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

    //setTimeout(updaterchart, 1000);

}

//updaterchart()
