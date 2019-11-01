var sstate = false;
var frequency;
var azimut;
var eloadining;
var elevacion;


 function loaderloader(){
     
    eloadining  = document.getElementById('aplotinfo');
    meloadining = document.getElementById('aplotinfo_M');
    eform       = document.getElementById('aform');
    mform       = document.getElementById('mform');
    efreq       = document.getElementById('efreq');
    eazimut     = document.getElementById('eazimut');
    eelevacion  = document.getElementById('eelevacion');

 }

 loaderloader();

 function gettingstate(){

     var xhttp = new XMLHttpRequest();
     //xhttp.responseType = "application/json";

     xhttp.onreadystatechange = function() {
    
     if (this.readyState == 4 && this.status == 200) {

         stateobject = this.response;
         stateobject = JSON.parse(stateobject);
         sstate       = stateobject.activo;
         frequency   = stateobject.frecuencia;
         azimut = stateobject.azimut;
         elevacion = stateobject.elevacion;
         
         }
     };

     xhttp.open("GET", "/radioastronomia/estado/1", true);
     xhttp.send();

     efreq.innerHTML = frequency;
     eazimut.innerHTML = azimut;
     eelevacion.innerHTML = elevacion;

      if (sstate == true){
          eloadining.style.display = "block";
          meloadining.style.display = "block";
          eform.style.display = "none";
          mform.style.display = "none";
      }
      else if(sstate == false){
          eloadining.style.display = "none";
          meloadining.style.display = "none";
          eform.style.display = "block";
          mform.style.display = "block";
      }

    //  console.log(sstate, frequency)
     setTimeout(gettingstate, 500);

 }

 //document.getElementById('aplotinfo').style.display = "none"
 gettingstate();

//  function rotor(){
     
//      var xhttp1 = new XMLHttpRequest();
//      xhttp1.open("GET", "/radioastronomia/estado/posicion/1", true);
//      xhttp1.send();
//      xhttp1.onreadystatechange = function() {
         
//          if (this.readyState == 4 && this.status == 200) {
             
//             stateobject = this.response;
//             stateobject = JSON.parse(stateobject);
//             sstate       = stateobject.activo;
//             console.log("estado", sstate);
//             }
//         };
//      if(sstate==true){
//         rotor.style.display = "block";
//     };
//  }
//  document.getElementById("Afsubmit").addEventListener("click", rotor);
//  document.getElementById("AMsubmit").addEventListener("click", rotor);

