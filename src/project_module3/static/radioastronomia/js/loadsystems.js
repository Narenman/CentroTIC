var estadoc = false;
var estadoes = false;

function cargar(){
    // esta funcion lee los id del HTML
    eambiental = document.getElementById('eambiental')
    ecamara = document.getElementById('ecamara')
    fambiental = document.getElementById('fambiental')
    fcamara = document.getElementById('fcamara')
    inacamara = document.getElementById('inacamara')
    inaestacion = document.getElementById('inaestacion')
}

cargar()

function obtenerestado(){
    // se encarga de leer el estado y ocultar de acuerdo
    // a la peticion
    var xhr1 = new XMLHttpRequest();
    var xhr2 = new XMLHttpRequest();

    xhr1.onreadystatechange = function(){

        if (this.readyState == 4 && this.status ==200){
            stateobject = this.response;
            stateobject = JSON.parse(stateobject)
            estadoc = stateobject.activo
        }
    };

    xhr2.onreadystatechange = function(){

        if (this.readyState == 4 && this.status ==200){
            stateobject = this.response;
            stateobject = JSON.parse(stateobject)
            estadoes = stateobject.activo
        }
    };


    xhr1.open("GET", "/radioastronomia/estado/camara/1", true);
    xhr1.send();
    xhr2.open("GET", "/radioastronomia/estado/estacion/1", true);
    xhr2.send();

    if (estadoc==true){
        ecamara.style.display = "block";
        fcamara.style.display = "block";
        inacamara.style.display = "none";

    }
    else if(estadoc == false){
        ecamara.style.display = "none";
        fcamara.style.display = "none";
        inacamara.style.display = "block"
    }
    if (estadoes==true){
        eambiental.style.display = "block";
        fambiental.style.display = "block";
        inaestacion.style.display = "none";
    }
    else if(estadoes==false){
        eambiental.style.display = "none";
        fambiental.style.display = "none";
        inaestacion.style.display = "block";
    }

    setTimeout(obtenerestado, 2000);

} //fin obtener estado


function detener_estacion(){
    var xhr = new XMLHttpRequest();
    xhr.open("POST","/radioastronomia/detener/subsistemas", true);
    data = new FormData();
    data.append('detener', 'estacion')
    xhr.send(data);
}

function detener_camara(){
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/radioastronomia/detener/subsistemas", true);
    data = new FormData();
    data.append('detener', 'camara')
    xhr.send(data);
}


obtenerestado()
//eventos de click
document.getElementById("bot_estacion").addEventListener("click", detener_estacion);
document.getElementById("bot_camara").addEventListener("click", detener_camara);
