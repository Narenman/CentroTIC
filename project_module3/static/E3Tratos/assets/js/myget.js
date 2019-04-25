
var globaljson = "-"; 
var meteorology = []
function loadDoc() {
  
  var xhttp = new XMLHttpRequest();
  xhttp.responseType = "json";

  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {

    	globaljson = this.response.datos;
    	globaljson = globaljson[globaljson.length-1];
    	meteorology = globaljson[1][0].meteorology_var;
    	printer();
    }
  };
  xhttp.open("GET", "http://localhost:8000/E3Tratos/datos-json", true);
  xhttp.send(); 

  setTimeout(loadDoc, 600);
}

var datos = [];

function printer(){

	console.log(meteorology);
	document.getElementById('v_temp').innerHTML = meteorology.temperatura;
	document.getElementById('v_pres').innerHTML = meteorology.presion;
	document.getElementById('v_hum').innerHTML = meteorology.humedad;
	document.getElementById('v_co2').innerHTML = meteorology.co2;
	document.getElementById('v_rad').innerHTML = meteorology.radiacion_uv; 
	document.getElementById('v_pm25').innerHTML = meteorology.PM25;
	
}


loadDoc();


