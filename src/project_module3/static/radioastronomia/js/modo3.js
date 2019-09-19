/*Este archivo se encarga de administrar el el analisis 
temporal por cada banda espectral */

function validatedSendForm_A(){
    var BSE_DI = document.getElementById('start_A').value;
    var BSE_DF = document.getElementById('end_A').value;
    if(BSE_DI>BSE_DF){
        window.alert("Rango de fechas inválido", );
    }
    else{
        sendForm(document.getElementById('form_modo3_A'));
    }
}

function validatedSendForm_E(){
    var BSE_DI = document.getElementById('start_E').value;
    var BSE_DF = document.getElementById('end_E').value;
    if(BSE_DI>BSE_DF){
        window.alert("Rango de fechas inválido", );
    }
    else{
        
        sendForm(document.getElementById('form_modo3_E'));
    }
}


function sendForm(formElement){
 
    // alert(formElement.id)
    // en caso de querer agregar informacion extra
    formData = new FormData(formElement)
    // formData.append(csrftoken); //esto es informacion extra
    var posiciones = document.getElementById("posiciones")

    var xhr = new XMLHttpRequest();
    xhr.open("POST","/radioastronomia/posiciones-angulares", false)
    xhr.send(formData)

    if (xhr.status==200){
        
        //esta variable lee lo que viene del servidor
        stateobject = xhr.response;
        stateobject = JSON.parse(stateobject);
        angular = stateobject.angular
        angulos = stateobject.pos
        
        
        //inicio grafica polar
        Highcharts.chart('polar', {

            chart: {
                polar: true
            },
        
            title: {
                text: 'Energia por angulos'
            },
        
            subtitle: {
                text: 'Posiciones angulares'
            },
        
            pane: {
                startAngle: 0,
                endAngle: 360
            },
        
            xAxis: {
                tickInterval: 45,
                min: 0,
                max: 360,
                labels: {
                    format: '{value}°'
                }
            },
        
            yAxis: {
                min: 0
            },
        
            plotOptions: {
                series: {
                    pointStart: 0,
                    pointInterval: 45
                },
                column: {
                    pointPadding: 0,
                    groupPadding: 0
                }
            },
        
            series: [{
                type: 'area',
                name: 'Energia mW',
                data: angular
            }]
        });
        //fin grafica polar

        posiciones.innerHTML = "Energía por ángulos "+angulos

    }
    else{
        output.innerHTML += "Error HTTP"+ xhr.status;
    }

}

