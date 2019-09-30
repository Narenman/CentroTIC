


var services = servicios.replace(/&quot;/g,'"');
services = JSON.parse(services);

var canvas = document.getElementById('BoxesCanvas');


var CBox     = [];
var boxW     = 160*2;
//var boxH     = 50;


var colorBox = {"FIJO": "#09a912",
                "MOVIL": "#00b7b7",
                "AERONAUTICO": "#0069cd",
                "RADIOASTRONOMIA": "#fe3399",
                "RADIO NAVEGACION AERONAUTICA": "#c5c21d",
                "RADIO DIFUSION TV": "#c12e01",
                "RADIO DIFUSION FM": "#c12e01",
                "OPERACIONES ESPACIALES":"#c0504d",
                "METEOROLOGIA POR SATELITE": "#666633",
                "MOVIL POR SATELITE": "#68699a",
                "INVESTIGACION ESPACIAL": "#808006",
                "MOVIL SALVO MOVIL AERONAUTICO":"#00b7b7",
                "RADIOLOCALIZACION": "#e46c0a",
                "AFICIONADOS": "#bfbfbf",
                "AFICIONADOS POR SATELITE": "#7f7f7f",
                "MOVIL MARITIMO (SOCORRO Y LLAMADA POR LLSD)": "#3737cd",
                "MOVIL MARITIMO": "#3737cd",
                "MOVIL MARITIMO ": "#3737cd",
                "MOVIL MARITIMO POR SATELITE":"#68699a",
                "MOVIL AERONAUTICO": "#0069cd"
            }; 

bckgndctx = canvas.getContext('2d');
bckgndctx.fillStyle = "#000";
bckgndctx.fillRect(0, 0, cnvsW, 300)


for(i=0; i<=services.length-1; i++){

    var AllServices = services[i].servicio.split('-');
    var AllServicesUC = [];
    var freq0 = services[i].frecuencia_inicial;
    var freq1 = services[i].frecuencia_final;

    var boxH     = 300/AllServices.length + 6/AllServices.length-1; // preferiblemente Obtener desde servidor 
    for (as=0; as<=AllServices.length-1; as++){

        // var nboxH = parseInt(cnvsH-i)/i;
        // var nboxW; 

        AllServicesUC[as]= AllServices[as].toUpperCase();

        CBox[as] = canvas.getContext("2d");
        
        //CBox[as].fillStyle = "#20c997";
        DVBorder = 3
        CBox[as].fillStyle = colorBox[AllServicesUC[as]];
        CBox[as].fillRect((boxW+DVBorder)*i, as*(boxH+1), boxW, boxH);
        
        CBox[as].font="bold 12px Arial";
        CBox[as].textAlign = "center";
        CBox[as].fillStyle = "#000";
        CBox[as].fillText(AllServicesUC[as], (boxW+DVBorder)*(2*i+1)/2, (boxH+1)*(as*2+1)/2);

        if (i == services.length-1){
            CBox[as].font="10px Arial";
            CBox[as].textAlign = "left";
            CBox[as].fillStyle = "#000";
            CBox[as].fillText(freq0+" MHz", ((boxW+DVBorder)*i+5), 10);

            CBox[as].font="10px Arial";
            CBox[as].textAlign = "left";
            CBox[as].fillStyle = "#000";
            CBox[as].fillText(freq1+" MHz", cnvsW-60, 10); //((boxW+DVBorder)*i + boxW/1.29)
    
        }
        else{
            CBox[as].font="10px Arial";
            CBox[as].textAlign = "left";
            CBox[as].fillStyle = "#000";
            CBox[as].fillText(freq0+" MHz", ((boxW+DVBorder)*i+5), 10);
        }
    }






    console.log('boxes filee', typeof parseInt(cnvsH) ); 
       
}




