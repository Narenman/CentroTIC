var ctx = document.getElementById('myChart').getContext('2d');
var iresponse;



function updater(){
    var xhttp = new XMLHttpRequest();
    xhttp.responseType = "json";

    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {

        iresponse = this.response;


        //console.log(iresponse);

        }
    };

  xhttp.open("GET", "/radioastronomia/json-estacion", true);
  xhttp.send(); 

  setTimeout(updater, 1000);

}

updater();

idatasets = [{data: [9, 2, 3, 4, 5, 6, 7, 8, 9],
                    backgroundColor: "#000",
                    borderColor: "#000",
                    borderWidth:1,
                    fill: false,
                    label: "Data test"
                    }]

console.log(typeof idatasets)
console.log("response", iresponse)
console.log(Object.keys(idatasets[0]))

//console.log(Object.keys(response))

var MainChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [9, 2, 3, 4, 5, 6, 7, 8, 9],
        datasets: idatasets
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});



console.log(MainChart.data.datasets[0])