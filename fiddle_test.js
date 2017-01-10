
    var directionDisplay, directionsService, map, marker;
    
    function initialize() {
        directionsService = new google.maps.DirectionsService()
        directionsDisplay = new google.maps.DirectionsRenderer();
        var chicago = new google.maps.LatLng(41.850033, -87.6500523);
        var mapOptions = {
            zoom:7,
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            center: chicago
          }
          
        map = new google.maps.Map(document.getElementById('map_canvas'), mapOptions);
        marker=new google.maps.Marker();
        directionsDisplay.setMap(map);
        map.addListener('click',function(e){fx(e.latLng)});
                        
      }

    function fx(latLng) {
        marker.setMap(null);

        var request = {
            origin:latLng,
            destination:latLng,
            travelMode: google.maps.DirectionsTravelMode.DRIVING
        };
        directionsService.route(request, function(response, status) {
            console.log(response)
            if (status == google.maps.DirectionsStatus.OK) {
                var point=response.routes[0].legs[0];
                marker.setOptions({map:map, position:point.start_location});
                map.setCenter(point.start_location);
                alert(response.routes[0].summary+'\n'+point.start_location.toString());
            }
        });
      }
