function initMap() {
var directionsService = new google.maps.DirectionsService;
var directionsDisplay = new google.maps.DirectionsRenderer;
var map = new google.maps.Map(document.getElementById('map'), {
  zoom: 7,
  center: {lat: 47.53, lng: -119.36}
});
directionsDisplay.setMap(map);

displayRoute(directionsService, directionsDisplay);
    
}

function displayRoute(directionsService, directionsDisplay) {
var waypts = [{location: {lat: 47.619869, lng: -119.459762},stopover: true}, {location: {lat: 47.646012,lng: -119.358825}, stopover: true}];
//var checkboxArray = document.getElementById('waypoints');
//for (var i = 0; i < checkboxArray.length; i++) {
//  if (checkboxArray.options[i].selected) {
//    waypts.push({
//      location: checkboxArray[i].value,
//      stopover: true
//    });
//  }
//}

directionsService.route({
//  origin: document.getElementById('start').value,
//  destination: document.getElementById('end').value,
  origin: {lat: 47.607140, lng: -119.653053},
  destination: {lat: 47.683360, lng: -119.128378},
  waypoints: waypts,
  optimizeWaypoints: true,
  travelMode: 'DRIVING'
}, function(response, status) {
  if (status === 'OK') {
    directionsDisplay.setDirections(response);
    var route = response.routes[0];
//    var summaryPanel = document.getElementById('directions-panel');
//    summaryPanel.innerHTML = '';
    // For each route, display summary information.
//    for (var i = 0; i < route.legs.length; i++) {
//      var routeSegment = i + 1;
//      summaryPanel.innerHTML += '<b>Route Segment: ' + routeSegment +
//          '</b><br>';
//      summaryPanel.innerHTML += route.legs[i].start_address + ' to ';
//      summaryPanel.innerHTML += route.legs[i].end_address + '<br>';
//      summaryPanel.innerHTML += route.legs[i].distance.text + '<br><br>';
//    }
  } else {
    window.alert('Directions request failed due to ' + status);
  }
});
}
