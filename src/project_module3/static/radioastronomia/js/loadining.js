var sstate = false;
var frequency;

var eloadining;
 
 function loaderloader(){
     
    eloadining = document.getElementById('aplotinfo');
    eform      = document.getElementById('aform');
    efreq      = document.getElementById('efreq');
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
         }
     };

     xhttp.open("GET", "/radioastronomia/estado/1", true);
     xhttp.send();

     efreq.innerHTML = frequency;

      if (sstate == true){
          eloadining.style.display = "block";
          eform.style.display = "none";
      }
      else if(sstate == false){
          eloadining.style.display = "none";
          eform.style.display = "block";
      }

     console.log(sstate, frequency, document.getElementById('aplotinfo').style.display)
     setTimeout(gettingstate, 500);

 }


 //document.getElementById('aplotinfo').style.display = "none"
 
 gettingstate();