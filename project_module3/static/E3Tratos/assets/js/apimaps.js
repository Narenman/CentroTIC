var poly;
var map;
var image = '../static/E3Tratos/assets/img/mico.png';
function initMap() {

  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 17,
    disableDefaultUI: true   // Center the map on Chicago, USA.
  }); 


  flightpositions = [
  {lat:7.1417204,lng:-73.1197928},
  {lat:7.1411233,lng:-73.1197257},
  {lat:7.1405682,lng:-73.118541}
  ];

  poly = new google.maps.Polyline({
    path: flightpositions,
    geodesic: true,
    strokeColor: '#000000',
    strokeOpacity: 1.0,
    strokeWeight: 1
  });



  poly.setMap(map);
  
  var beachMarker = new google.maps.Marker({
    position: flightpositions[flightpositions.length-1],
    map: map,
    icon: image
  });

  // Add a listener for the click event
  map.addListener('click', addLatLng);
  map.setCenter(flightpositions[flightpositions.length-1]);
}

// Handles click events on a map, and adds a new point to the Polyline.
function addLatLng(event) {
  var path = poly.getPath();

  //// Because path is an MVCArray, we can simply append a new coordinate
  ////and it will automatically appear.
  //path.push(event.latLng);
  
  //// Add a new marker at the new plotted point on the polyline.

  // var marker = new google.maps.Marker({
  //   position: event.latLng,
  //   title: '#' + path.getLength(),
  //   map: map,
  //   icon: image
  // });
  


}

