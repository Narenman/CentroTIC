var poly;
var map;
var image = '../static/E3Tratos/assets/img/mico.png';
var beachMarker =[];
var flightpositions;
function initMap() {

  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 15,
    disableDefaultUI: true,   // Center the map on Chicago, USA. #242f3e
    styles: [
            {elementType: 'geometry', stylers: [{color: '#22282d'}]},
            {elementType: 'labels.text.stroke', stylers: [{color: '#242f3e'}]},
            {elementType: 'labels.text.fill', stylers: [{color: '#746855'}]},
            {
              featureType: 'administrative.locality',
              elementType: 'labels.text.fill',
              stylers: [{color: '#d59563'}]
            },
            {
              featureType: 'poi',
              elementType: 'labels.text.fill',
              stylers: [{color: '#d59563'}]
            },
            {
              featureType: 'poi.park',
              elementType: 'geometry',
              stylers: [{color: '#263c3f'}]
            },
            {
              featureType: 'poi.park',
              elementType: 'labels.text.fill',
              stylers: [{color: '#6b9a76'}]
            },
            {
              featureType: 'road',
              elementType: 'geometry',
              stylers: [{color: '#38414e'}]
            },
            {
              featureType: 'road',
              elementType: 'geometry.stroke',
              stylers: [{color: '#212a37'}]
            },
            {
              featureType: 'road',
              elementType: 'labels.text.fill',
              stylers: [{color: '#9ca5b3'}]
            },
            {
              featureType: 'road.highway',
              elementType: 'geometry',
              stylers: [{color: '#746855'}]
            },
            {
              featureType: 'road.highway',
              elementType: 'geometry.stroke',
              stylers: [{color: '#1f2835'}]
            },
            {
              featureType: 'road.highway',
              elementType: 'labels.text.fill',
              stylers: [{color: '#f3d19c'}]
            },
            {
              featureType: 'transit',
              elementType: 'geometry',
              stylers: [{color: '#2f3948'}]
            },
            {
              featureType: 'transit.station',
              elementType: 'labels.text.fill',
              stylers: [{color: '#d59563'}]
            },
            {
              featureType: 'water',
              elementType: 'geometry',
              stylers: [{color: '#17263c'}]
            },
            {
              featureType: 'water',
              elementType: 'labels.text.fill',
              stylers: [{color: '#515c6d'}]
            },
            {
              featureType: 'water',
              elementType: 'labels.text.stroke',
              stylers: [{color: '#17263c'}]
            }
          ]
  }); 


  // flightpositions = [
  // {lat:7.1417204,lng:-73.1197928},
  // {lat:7.1411233,lng:-73.1197257},
  // {lat:7.1405682,lng:-73.118541},
  // {lat:7.1405652,lng:-73.113543}
  // ];
flightpositions = [{lat:7.139154666,lng:-73.1211928333}]
//flightpositions.push({lat:geo.lat,lng:geo.lng})
  // //console.log("attitude", attitude.X)

/*  poly = new google.maps.Polyline({
    path: flightpositions,
    geodesic: true,
    strokeColor: '#00b4ff',
    strokeOpacity: 1.0,
    strokeWeight: 1
  });*/



  //poly.setMap(map);
  
  beachMarker = new google.maps.Marker({
    position: flightpositions[flightpositions.length-1],
    map: map,
    icon: image
  });

  // Add a listener for the click event
  //map.addListener('click', addLatLng); 
  map.setCenter(flightpositions[flightpositions.length-1]);


  
}


var earth = 6378.137;
var acu   = 0;
pi = Math.PI,
m = (1 / ((2 * pi / 360) * earth)) / 1000;  

setInterval(function addLatLng() {
  acu = acu +1;
  
  var llat = geo.lat;// + acu*m;
  var llng = geo.lng;// + acu*m/Math.cos(geo.lng*(Math.PI/180))
  var latlng = new google.maps.LatLng(llat,llng);
  beachMarker.setPosition(latlng);
  map.setCenter(latlng);
  flightpositions.push({lat:llat,lng:llng})
  //path = poly.getPath();

  poly = new google.maps.Polyline({
    path: flightpositions,
    geodesic: true,
    strokeColor: '#00b4ff',
    strokeOpacity: 1.0,
    strokeWeight: 1
  });

  poly.setMap(map);

  // var path = poly.getPath();
  // console.log(llat)
  //// Because path is an MVCArray, we can simply append a new coordinate
  ////and it will automatically appear.
  //path.push(latLng);

  
  // //// Add a new marker at the new plotted point on the polyline.

  // var marker = new google.maps.Marker({
  //   position: event.latLng,
  //   title: '#' + path.getLength(),
  //   map: map,
  //   icon: image
  // });
  //console.log("updating position",llat, llng, acu*m)

}, 1000)

