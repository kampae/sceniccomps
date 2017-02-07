function initMap(waypoints) {
    var directionsService = new google.maps.DirectionsService;
    var directionsDisplay = new google.maps.DirectionsRenderer({
        suppressMarkers: true,
        suppressInfoWindows: true,
    });
    var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 7,
      center: {lat: 47.607140, lng: -120.292142}
    });
    directionsDisplay.setMap(map);
    displayRouteMoreWpts(directionsService, directionsDisplay, waypoints);
    
    var startMarker = new google.maps.Marker({
        position: {lat: waypoints[0][0], lng: waypoints[0][1]},
        map: map,
        label: 'A'
    });
    var endMarker = new google.maps.Marker({
        position: {lat: waypoints[waypoints.length - 1][0], lng: waypoints[waypoints.length - 1][1]},
        map: map,
        label: 'B'
    });  
}


function displayRoute(directionsService, directionsDisplay, waypoints) {
    // start: [47.607140, -119.653053]
    // end: [47.683360, -119.128378]
//    47.607140, -119.653053
    // 47.435141, -120.292142
    //[47.619869, -119.459762]
    //[47.646012, -119.358825],
   if(waypoints != null) {
    var coords = waypoints;
    //var spoint = parseFloat(start);
//    var coords = [[spoint, -122.317704], [47.619869, -119.459762], [47.646012, -119.358825], [47.683360, -119.128378]];
    var waypts = [];
    for (var i = 1; i <coords.length-1; i++)
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
    
}


function displayRouteMoreWpts(directionsService, directionsDisplay, waypoints) {
   if(waypoints != null && waypoints.length <= 23) {
    var waypts = [];
    for (var i = 1; i <waypoints.length-1; i++)
    {
        wayPoint = {"location" : {"lat" : waypoints[i][0], "lng": waypoints[i][1]}, "stopover": true};
        waypts.push(wayPoint);
    }

    directionsDisplay.setPanel(document.getElementById('directions'));

    directionsService.route({
      origin: {lat: waypoints[0][0], lng: waypoints[0][1]},
      destination: {lat: waypoints[waypoints.length - 1][0], lng: waypoints[waypoints.length - 1][1]},
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
    
    else if (waypoints != null && waypoints.length > 25) {
        // Starts at 1 so that we do not count the start location as a waypoint
        var waypointsCovered = 1;
        
        while (waypointsCovered < waypoints.length - 1) {
            var waypts = [];
            var counter = 0;
            // Go through 23 waypoints at a time
            for (var i = 0; i < 23; i++)
            {
                // If there are less than 23 waypoints left in the list, break when you reach the end
                if (i + waypointsCovered > waypoints.length - 1) {
                    break;
                }
                
                var curWaypoint = waypoints[i + waypointsCovered];
                wayPoint = {"location" : {"lat" : waypoints[i + waypointsCovered][0], "lng": waypoints[i + waypointsCovered][1]}, "stopover": true};
                waypts.push(wayPoint);
                counter++;
            }
            
            waypointsCovered += counter;
            directionsDisplay.setPanel(document.getElementById('directions'));
            
            if (waypointsCovered == 30) {
                var destination = waypoints[waypoints.length - 1];
            }
            
            else {
                var destination = waypoints[waypointsCovered - 1];
            }

            directionsService.route({
              origin: {lat: waypoints[waypointsCovered - 24][0], lng: waypoints[waypointsCovered - 24][1]},
              destination: {lat: destination[0], lng: destination[1]}, //waypoints[waypointsCovered - 1][0], lng: waypoints[waypointsCovered- 1][1]},
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
    }
    
}

