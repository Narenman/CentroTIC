
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
    	//globaljson = globaljson[globaljson.length-1];

      /*
    	meteorology = globaljson[1].meteorology_var;
      tiempovuelo = globaljson[1].geo.tiempo_vuelo;
      window.attitude = globaljson[1].attitude;
      window.geo      = globaljson[1].geo;
      window.inside   = globaljson[1].inside;
      */
    	printer();
      //console.log(meteorology.temperatura[0]);
      updaterchart();
    }
  };

  xhttp.open("GET", "http://127.0.0.1:8080/piscicultura/variables-json-last/", true);
  xhttp.overrideMimeType('text/xml; charset=iso-8859-1');
  xhttp.send(); 

  setTimeout(loadDoc, 5000);

}
/*
function outputvar(){
  console.log("el globaljson",globaljson)
  return globaljson;
}
*/
/**/


function downloadall(){

  var xhttp = new XMLHttpRequest();
  xhttp.responseType = "json";

  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {

      globaljson = this.response.datos;
      //console.log(meteorology.temperatura[0]);
      
    }
  };

  xhttp.open("GET", "http://34.74.6.16/E3Tratos/datos-json-all", true);
  xhttp.overrideMimeType('text/xml; charset=iso-8859-1');
  xhttp.send(); 

}

var i = 0;

//fecha= String(temp[0]);

 function printer(){
  //console.log("temperatra", meteorology.presion)
  fecha= new Date(String(temp[0]));

  document.getElementById('last_update1').innerHTML = "Última actualización: " + String(fecha.toLocaleString());
 	document.getElementById('temp_value').innerHTML = String(temp[1])+" °C";
  document.getElementById('ph_value').innerHTML = ph[1];
  document.getElementById('od_value').innerHTML = String(od[1])+" mg/L";

 	document.getElementById('tempCaja_value').innerHTML = String(tempC[1])+" °C";
  document.getElementById('humCaja_value').innerHTML = humC[1];
  document.getElementById('voltBat_value').innerHTML = String(voltajeB[1])+" V";

 }


loadDoc();



// var ctx = document.getElementById("myChart").getContext('2d');


//     // body...
//     var chart = new Chart(ctx, {
//     type: 'line',
//     data: {
        
//         labels: [],
        
//         datasets: [{
//             label: 'temperatura',
//             data: [],
//             yAxisID: 'y-axis-1',
//             fill: false,       
//             backgroundColor: ['#f44336'],
//             borderColor: ['#f44336'],
//             borderWidth: 1,
//             showLine: true
//             },

//             { 
//             label: "2",
//             data:[],
//             yAxisID: 'y-axis-1',
//             fill: false,
//             backgroundColor: ['#9c27b0'],
//             borderColor: ['#9c27b0'],
//             borderWidth: 1
//             },

//                       { 
//             label: "3",
//             data:[],
//             yAxisID: 'y-axis-1',
//             fill: false,
//             backgroundColor: ['#2196f3'],
//             borderColor: ['#2196f3'],
//             borderWidth: 1
//             },

//                       { 
//             label: "4",
//             data:[],
//             yAxisID: 'y-axis-1',
//             fill: false,
//             backgroundColor: ['#009688'],
//             borderColor: ['#009688'],
//             borderWidth: 1
//             },


//             { 
//             label: "5",
//             data:[],
//             yAxisID: 'y-axis-1',
//             fill: false,
//             backgroundColor: ['#4caf50'],
//             borderColor: ['#4caf50'],
//             borderWidth: 1
//             },

//             { 
//             label: "6",
//             data:[],
//             yAxisID: 'y-axis-1',
//             fill: false,
//             backgroundColor: ['#cddc39'],
//             borderColor: ['#cddc39'],
//             borderWidth: 1
//             }

//             ]
//     },
//     options: {
//         responsive: true,
//         title: {
//             display: false,
//             text: 'Temp',
//         },
//         scales: {
//             yAxes: [{
//                 type: 'linear',
//                 display: 'true',
//                 gridLines:{
//                     display: false
//                     },
//                 ticks:{
//                     fontColor: '#00b4ff',
//                     },
//                 position: 'left',
//                 id: 'y-axis-1'}



//                 ]
//             }
//         }
//     });
// console.log("carga")

// var jj = 0;

// function updaterchart() {
//     //console.log(meteorology.temperatura, mydatetime())

//     // chart.data.labels.push(jj++)
//     // chart.data.datasets[1-1].data.push(meteorology.temperatura[0])
//     // chart.data.datasets[2-1].data.push(meteorology.presion[0])
//     // chart.data.datasets[3-1].data.push(meteorology.humedad[0])
//     // chart.data.datasets[4-1].data.push(meteorology.co2[0])
//     // chart.data.datasets[5-1].data.push(meteorology.radiacion_uv[0])
//     // chart.data.datasets[6-1].data.push(meteorology.PM25[0])

//     chart.data.labels.push(jj++)
//     chart.data.datasets[1-1].data.push(1)
//     chart.data.datasets[2-1].data.push(2)
//     chart.data.datasets[3-1].data.push(3)
//     chart.data.datasets[4-1].data.push(4)
//     chart.data.datasets[5-1].data.push(5)
//     chart.data.datasets[6-1].data.push(6)


//     if (jj>10) {
//         chart.data.labels.shift()
//         chart.data.datasets[1-1].data.shift()
//         chart.data.datasets[2-1].data.shift()
//         chart.data.datasets[3-1].data.shift()
//         chart.data.datasets[4-1].data.shift()
//         chart.data.datasets[5-1].data.shift()
//         chart.data.datasets[6-1].data.shift()
//     }
//     chart.update();
    


//       //  console.log(Math.max(maptoint))
//       //console.log("ok");
//      // maxTemp.innerHTML = Math.max(maptoint)
//      // minTemp.innerHTML = Math.min(maptoint)






//     setTimeout(updaterchart, 1000);

// }

// updaterchart()