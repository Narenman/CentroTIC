var datohr = "-"; 
var datospo2 = "-"; 
var datobateria = "-"; 
var fecha = "-";
var fecha2="-";

function printer(){

  
  document.getElementById('v_hr').innerHTML = datohr + " lpm";
  document.getElementById('v_spo2').innerHTML = datospo2+ "%";
  document.getElementById('v_bateria').innerHTML =datobateria+"V";
}


function loadDoc() {

  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {

      datohr=JSON.parse(this.response).datos[1];
      datospo2= JSON.parse(this.response).datos[2];
      datobateria= JSON.parse(this.response).datos[3];
      fecha2= JSON.parse(this.response).datos[0];

      fecha= fecha2.slice(2, 16);

    	console.log(JSON.parse(this.response).datos[1])
      console.log(JSON.parse(this.response).datos[2])
      console.log(JSON.parse(this.response).datos[3])
      console.log(JSON.parse(this.response).datos[0])
      console.log(fecha)

      printer();

       updaterchart();
    }
    
  };

  xhttp.open("GET", "/pulsioximetria/datosgraf-json", true);
  xhttp.overrideMimeType('text/xml; charset=iso-8859-1');
  xhttp.send(); 

  setTimeout(loadDoc, 12000);

}


function downloadall(){

  var xhttp = new XMLHttpRequest();
  xhttp.responseType = "json";

  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {

     datohr=JSON.parse(this.response).datos[1];
     datospo2= JSON.parse(this.response).datos[2];
     datobateria= JSON.parse(this.response).datos[3];
     fecha2= JSON.parse(this.response).datos[0];
     fecha= fecha2.slice(12, 19);
    
      console.log(JSON.parse(this.response).datos[1])
      
    }
  };

  xhttp.open("GET", "/pulsioximetria/datos-json-all", true);
  xhttp.overrideMimeType('text/xml; charset=iso-8859-1');
  xhttp.send(); 

}

loadDoc();
