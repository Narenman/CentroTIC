var temp3 = "-"; 
var od3 = "-"; 
var ph3 = "-"; 
var tempC3 = "-"; 
var humC3 = "-"; 
var voltajeB3 = "-"; 
var fecha3 = "___"; 





function loadDoc() {

  var xhttp = new XMLHttpRequest();
  xhttp.responseType = "json";


  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {

    	//globaljson = this.response.datos;
      temp3=this.response.temperatura;
      od3= this.response.oxigenoDisuelto;
      ph3= this.response.phTank;
      tempC3= this.response.tempCaja;
      voltajeB3= this.response.voltajeBat;
      humC3= this.response.humCaja;

    	printer();
     
      updaterchart();
    }
  };

  //xhttp.open("GET", "http://192.168.0.108:8080/piscicultura/json-last-est3/", true);
  xhttp.open("GET", "/piscicultura/json-last-est3/", true);
  xhttp.overrideMimeType('text/xml; charset=iso-8859-1');
  xhttp.send(); 

  setTimeout(loadDoc, 12000);

}


//var i = 0;

//fecha= String(temp[0]);

 function printer(){
  
  fecha3= new Date(String(temp3[0]));

  document.getElementById('last_update3').innerHTML = "Última actualización: " + String(fecha3.toLocaleString());
  document.getElementById('temp_value3').innerHTML = String(temp3[1])+" °C";
  document.getElementById('ph_value3').innerHTML = ph3[1];
  document.getElementById('od_value3').innerHTML = String(od3[1])+" mg/L";

  document.getElementById('tempCaja_value3').innerHTML = String(tempC3[1])+" °C";
  document.getElementById('humCaja_value3').innerHTML = humC3[1]+"%";
  document.getElementById('voltBat_value3').innerHTML = String(voltajeB3[1])+" V";

  document.getElementById('temp_prom3').innerHTML = "Prom. "+String(temp[2])+" °C";
  document.getElementById('ph_prom3').innerHTML = "Prom. "+ph[2];
  document.getElementById('od_prom3').innerHTML = "Prom. "+String(od[2])+" mg/L";

  document.getElementById('tempCaja_prom3').innerHTML = "Prom. "+String(tempC[2])+" °C";
  document.getElementById('humCaja_prom3').innerHTML = "Prom. "+humC[2]+"%";
  document.getElementById('voltBat_prom3').innerHTML = "Prom. "+String(voltajeB[2])+" V";

 }

loadDoc();


var ctx = document.getElementById("myChart3").getContext('2d');

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
    chart.data.labels.push(fecha3.toLocaleTimeString())
    chart.data.datasets[1-1].data.push(temp3[1])
    chart.data.datasets[2-1].data.push(ph3[1])
    chart.data.datasets[3-1].data.push(od3[1])
    chart.data.datasets[4-1].data.push(tempC3[1])
    chart.data.datasets[5-1].data.push(humC3[1])
    chart.data.datasets[6-1].data.push(voltajeB3[1])


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
