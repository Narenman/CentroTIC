
var globaljson = "-"; 
var meteorology;
//var meteorology_g = ["-"]

var attitude; 


function loadDoc() {
  
  var xhttp = new XMLHttpRequest();
  xhttp.responseType = "json";

  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {

    	globaljson = this.response.datos;
    	//globaljson = globaljson[globaljson.length-1];
    	meteorology = globaljson[1].meteorology_var;
      tiempovuelo = globaljson[1].geo.tiempo_vuelo;
      window.attitude = globaljson[1].attitude;
      window.geo      = globaljson[1].geo;
      window.inside   = globaljson[1].inside;
    	printer();
      //console.log(meteorology.temperatura[0]);
      updaterchart();
    }
  };

  xhttp.open("GET", "/E3Tratos/datos-json", true);
  xhttp.overrideMimeType('text/xml; charset=iso-8859-1');
  xhttp.send(); 

  setTimeout(loadDoc, 1000);

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

  xhttp.open("GET", "/E3Tratos/datos-json-all", true);
  xhttp.overrideMimeType('text/xml; charset=iso-8859-1');
  xhttp.send(); 

}

var i = 0;

 function printer(){
  //console.log("temperatra", meteorology.presion)


 	document.getElementById('v_temp').innerHTML = meteorology.temperatura[0];
  document.getElementById('v_tempma').innerHTML = meteorology.temperatura[1];
  document.getElementById('v_tempmi').innerHTML = meteorology.temperatura[2];
  document.getElementById('v_tempme').innerHTML = meteorology.temperatura[3];
  document.getElementById('n_v1').innerHTML = meteorology.temperatura[4];
  

 	document.getElementById('v_pres').innerHTML = meteorology.presion[0];
  document.getElementById("v_prema").innerHTML = meteorology.presion[1];
  document.getElementById('v_premi').innerHTML = meteorology.presion[2];
  document.getElementById('v_preme').innerHTML = meteorology.presion[3];
  document.getElementById('n_v2').innerHTML = meteorology.presion[4];

 	document.getElementById('v_met').innerHTML = meteorology.metano[0];
  document.getElementById('v_metma').innerHTML = meteorology.metano[1];
  document.getElementById('v_metmi').innerHTML = meteorology.metano[2];
  document.getElementById('v_metme').innerHTML = meteorology.metano[3];
  document.getElementById('n_v3').innerHTML = meteorology.metano[4];

 	document.getElementById('v_co2').innerHTML = meteorology.co2[0];
  document.getElementById('v_co2ma').innerHTML = meteorology.co2[1];
  document.getElementById('v_co2mi').innerHTML = meteorology.co2[2];
  document.getElementById('v_co2me').innerHTML = meteorology.co2[3];
  document.getElementById('n_v4').innerHTML = meteorology.co2[4];

 	//document.getElementById('v_rad').innerHTML = meteorology.radiacion_uv[0]; 
 	document.getElementById('v_pm25').innerHTML = meteorology.PM25[0];
  document.getElementById('v_pm25ma').innerHTML = meteorology.PM25[1];
  document.getElementById('v_pm25mi').innerHTML = meteorology.PM25[2];
  document.getElementById('v_pm25me').innerHTML = meteorology.PM25[3];
  document.getElementById('n_v5').innerHTML = meteorology.PM25[4];

  document.getElementById('n_v6').innerHTML = meteorology.var_6[4];
  document.getElementById('v_var6').innerHTML = meteorology.var_6[0];
  document.getElementById('v_var6ma').innerHTML = meteorology.var_6[1];
  document.getElementById('v_var6mi').innerHTML = meteorology.var_6[2];
  document.getElementById('v_var6me').innerHTML = meteorology.var_6[3];


  document.getElementById('n_v7').innerHTML = meteorology.var_7[4];
  document.getElementById('v_var7').innerHTML = meteorology.var_7[0];
  document.getElementById('v_var7ma').innerHTML = meteorology.var_7[1];
  document.getElementById('v_var7mi').innerHTML = meteorology.var_7[2];
  document.getElementById('v_var7me').innerHTML = meteorology.var_7[3];

  document.getElementById('n_v8').innerHTML = meteorology.var_8[4];
  document.getElementById('v_var8').innerHTML = meteorology.var_8[0];
  document.getElementById('v_var8ma').innerHTML = meteorology.var_8[1];
  document.getElementById('v_var8mi').innerHTML = meteorology.var_8[2];
  document.getElementById('v_var8me').innerHTML = meteorology.var_8[3];



  document.getElementById('v_X').innerHTML = attitude.X;
  document.getElementById('v_Y').innerHTML = attitude.Y;
  document.getElementById('v_tvuelo').innerHTML = datev(tiempovuelo[0])+":"+datev(tiempovuelo[1])+":"+datev(tiempovuelo[2]);
	document.getElementById('v_lng').innerHTML = geo.lng;
  document.getElementById('v_lat').innerHTML = geo.lat;
  document.getElementById('v_distancia').innerHTML = geo.distancia;
  //document.getElementById('v_humINS').innerHTML = inside.humedad;
  document.getElementById('v_tempINS').innerHTML = inside.temperatura;
  document.getElementById('v_altura').innerHTML = geo.altura;
  document.getElementById('v_altitud').innerHTML = geo.altitud;


  document.getElementById('v_corriente').innerHTML = inside.corriente;
  document.getElementById('v_voltaje').innerHTML = inside.voltaje;
  document.getElementById('v_carga').innerHTML = inside.carga;


 }


loadDoc();



// var ctx = document.getElementById("myChart").getContext('2d');


//     // body...
//     var chart = new Chart(ctx, {
//     type: 'line',
//     data: {
        
//         labels: [],
        
//         datasets: [{
//             label: '1',
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
//             },

//             { 
//             label: "7",
//             data:[],
//             yAxisID: 'y-axis-1',
//             fill: false,
//             backgroundColor: ['#ff9800'],
//             borderColor: ['#ff9800'],
//             borderWidth: 1
//             },

//             { 
//             label: "8",
//             data:[],
//             yAxisID: 'y-axis-1',
//             fill: false,
//             backgroundColor: ['#ff5722'],
//             borderColor: ['#ff5722'],
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