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
    var coords = [[47.607140, -119.653053], [47.619869, -119.459762], [47.646012, -119.358825], [47.683360, -119.128378]];
    var waypts = [];
    for (var i = 1; i < coords.length - 1; i++)
    {
        wayPoint = {"location" : {"lat" : coords[i][0], "lng": coords[i][1]}, "stopover": true};
        waypts.push(wayPoint);
    }

    directionsDisplay.setPanel(document.getElementById('directions'));

    directionsService.route({
      origin: {lat: coords[0][0], lng: coords[0][1]},
      destination: {lat: coords[coords.length - 1][0], lng: coords[coords.length - 1][1]},
      waypoints: waypts,
      optimizeWaypoints: true,
      travelMode: 'DRIVING'
    }, function(response, status) {
      if (status === 'OK') {
        directionsDisplay.setDirections(response);
        var route = response.routes[0];
      } else {
        window.alert('Directions request failed due to ' + status);
      }
});
}
