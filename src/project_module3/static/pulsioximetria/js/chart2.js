 
var datobateria = "-"; 
var fecha = "-";
var fecha2="-";






function loadDoc() {

  var xhttp = new XMLHttpRequest();
  


  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {

        //globaljson = this.response.datos;
      datobateria= JSON.parse(this.response).datos[3];
      fecha2= JSON.parse(this.response).datos[0];

      fecha= fecha2.slice(12, 19);


    }
     updaterchart()
  };

  //xhttp.open("GET", "http://192.168.0.108:8080/piscicultura/json-last-est3/", true);
  xhttp.open("GET", "http://127.0.0.1:8000/pulsioximetria/datosgraf-json", true);
  xhttp.overrideMimeType('text/xml; charset=iso-8859-1');
  xhttp.send(); 

  setTimeout(loadDoc, 12000);

}


function downloadall(){

  var xhttp = new XMLHttpRequest();
  xhttp.responseType = "json";

  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {

      datobateria= this.response.datos[3];
      fecha2= this.response.datos[0];

      fecha= fecha2.slice(2, 10);
      //console.log(meteorology.temperatura[0]);
      console.log(JSON.parse(this.response).datos[1])
      
    }
  };

  xhttp.open("GET", "http://127.0.0.1:8000/pulsioximetria/datos-json-all", true);
  xhttp.overrideMimeType('text/xml; charset=iso-8859-1');
  xhttp.send(); 

}

//var i = 0;

//fecha= String(temp[0]);


loadDoc();








var ctx = document.getElementById("myChart2").getContext('2d'); 


    // body...
    var chart = new Chart(ctx, {
    type: 'line',
    data: {
        
        labels: [fecha],
        
        datasets: [{
            
            label: "Bateria",
            data:[],
            yAxisID: 'y-axis-1',
            fill: false,
            backgroundColor: ['#4fe35e'],
            borderColor: ['#4fe35e'],
            borderWidth: 1
            },


            ]
    },
    options: {
        responsive: true,
        title: {
            display: false,
            text: 'Temp',
        },
        scales: {
            yAxes: [{
                type: 'linear',
                display: 'true',
                gridLines:{
                    display: false
                    },
                ticks:{
                    fontColor: '#387a96',
                    },
                position: 'left',
                id: 'y-axis-1'}



                ]
            }
        }
    });

//console.log("mete",outputvar(), mydatetime())
var jj = 0;

function updaterchart() {
    //console.log(meteorology.co2[0], mydatetime())

    jj++
    chart.data.labels.push(fecha)
    chart.data.datasets[1-1].data.push(datobateria)
    
    

    if (jj>10) {
        chart.data.labels.shift()
        chart.data.datasets[1-1].data.shift()
        
    }
    chart.update();

  
    


      //  console.log(Math.max(maptoint))
      //console.log("ok");
     // maxTemp.innerHTML = Math.max(maptoint)
     // minTemp.innerHTML = Math.min(maptoint)






    //setTimeout(updaterchart, 1000);

}