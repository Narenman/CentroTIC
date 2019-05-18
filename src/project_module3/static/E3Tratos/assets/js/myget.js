
var globaljson = "-"; 
var meteorology = []
var attitude; 


function loadDoc() {
  
  var xhttp = new XMLHttpRequest();
  xhttp.responseType = "json";

  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {

    	globaljson = this.response.datos;
    	globaljson = globaljson[globaljson.length-1];
    	window.meteorology = globaljson[1].meteorology_var;
      window.tiempovuelo = globaljson[1].geo.tiempo_vuelo;
      window.attitude = globaljson[1].attitude;
      window.geo      = globaljson[1].geo;
      window.inside   = globaljson[1].inside;
    	printer();

    }
  };

  
  xhttp.open("GET", "http://34.74.6.16/E3Tratos/datos-json", true);
  xhttp.send(); 
  
  setTimeout(loadDoc, 1000);

}

function outputvar(){
  return globaljson;
}

var i = 0;

function printer(){

	document.getElementById('v_temp').innerHTML = meteorology.temperatura;
	document.getElementById('v_pres').innerHTML = meteorology.presion;
	document.getElementById('v_hum').innerHTML = meteorology.humedad;
	document.getElementById('v_co2').innerHTML = meteorology.co2;
	document.getElementById('v_rad').innerHTML = meteorology.radiacion_uv; 
	document.getElementById('v_pm25').innerHTML = meteorology.PM25;
  document.getElementById('v_X').innerHTML = attitude.X;
  document.getElementById('v_Y').innerHTML = attitude.Y;
  document.getElementById('v_tvuelo').innerHTML = datev(tiempovuelo[0])+":"+datev(tiempovuelo[1])+":"+datev(tiempovuelo[2]);
	document.getElementById('v_lng').innerHTML = geo.lng;
  document.getElementById('v_lat').innerHTML = geo.lat;
  document.getElementById('v_distancia').innerHTML = geo.distancia;
  document.getElementById('v_humINS').innerHTML = inside.humedad;
  document.getElementById('v_tempINS').innerHTML = inside.temperatura;
  document.getElementById('v_altura').innerHTML = geo.altura;
  document.getElementById('v_altitud').innerHTML = geo.altitud;

}


loadDoc();

