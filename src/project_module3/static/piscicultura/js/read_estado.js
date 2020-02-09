var est = "-"; 


function loadDoc() {

  var xhttp = new XMLHttpRequest();
  xhttp.responseType = "json";

  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {

    	//globaljson = this.response.datos;
      est=this.response.estado;

    	printer();
      //console.log(meteorology.temperatura[0]);

    }
  };

  //xhttp.open("GET", "http://192.168.0.108:8080/piscicultura/json-estado", true);
  xhttp.open("GET", "/piscicultura/json-estado", true);
  xhttp.overrideMimeType('text/xml; charset=iso-8859-1');
  xhttp.send(); 

  setTimeout(loadDoc, 1000);

}


 function printer(){

  //document.getElementById('estado').innerHTML = "Estado: "+ String(est);
  document.getElementById('estado_tomadatos').innerHTML = "Estado toma de datos: "+ String(est);

 }


loadDoc();

