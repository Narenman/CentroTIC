function loadMap() {

    var mapOptions = {
      center:new google.maps.LatLng(7.14100675, -73.1220363),
      zoom:18,
      mapTypeId:google.maps.MapTypeId.ROADMAP};
      var map = new google.maps.Map(document.getElementById("sample"),mapOptions);
  
      setMarkers(map);
  
  
    }
  
  google.maps.event.addDomListener(window, 'load', loadMap);
  
  var beaches = [
    ['USRP1', 7.140915, -73.123057],
    //['USRP2', 7.141836, -73.122145, 5],
    ['USRP2', 7.140937, -73.122547, 3],
  
  ];
  
  function setMarkers(map) {
    // Adds markers to the map.
  
    // Marker sizes are expressed as a Size of X,Y where the origin of the image
    // (0,0) is located in the top left of the image.
  
    // Origins, anchor positions and coordinates of the marker increase in the X
    // direction to the right and in the Y direction down.
    var image = {
      url: 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png',
      //url: '/home/radiogis/Escritorio/Carpeta/124575-200.jpg',
  
      // This marker is 20 pixels wide by 32 pixels high.
      size: new google.maps.Size(40, 52),
      // The origin for this image is (0, 0).
      origin: new google.maps.Point(0, 0),
      // The anchor for this image is the base of the flagpole at (0, 32).
      anchor: new google.maps.Point(0, 32)
    };
    // Shapes define the clickable region of the icon. The type defines an HTML
    // <area> element 'poly' which traces out a polygon as a series of X,Y points.
    // The final coordinate closes the poly by connecting to the first coordinate.
    var shape = {
      coords: [1, 1, 1, 20, 18, 20, 18, 1],
      type: 'poly'
    };
    for (var i = 0; i < beaches.length; i++) {
      var beach = beaches[i];
      var marker = new google.maps.Marker({
        position: {lat: beach[1], lng: beach[2]},
        map: map,
        icon: image,
        shape: shape,
        title: beach[0],
        zIndex: beach[3]
      });
    }
  }
  