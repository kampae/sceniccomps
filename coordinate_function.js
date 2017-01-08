//import js_coords;
    var roads_list = [];
    var coor_list = [];
    var directionDisplay, directionsService, map, marker;
    
    // Initialize our map and call our function right away
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
        //map.addListener('click',function(e){getClosestRoad(e.latLng)});
        
        var rawFile = new XMLHttpRequest();
        rawFile.open("GET", "coords_test.csv", false);
        rawFile.onreadystatechange = function ()
        {
            if(rawFile.readyState === 4)
                {
                    if(rawFile.status === 200 || rawFile.status == 0)
                        {
                            var allText = rawFile.responseText;
                            var allTextLines = allText.split(/[\n,]/);
                            for(i=0; i<allTextLines.length; i++) {
                                coor_list.push(parseFloat(allTextLines[i]));       
                            }
                        }
                }
        }
        rawFile.send(null);
//        var test_thing = [41.436, -86.058145];
//        alert(coor_list[40001]);
//        var coords = [{lat: coor_list[40000], lng: coor_list[40001]},{lat: coor_list[40002], lng: coor_list[40003]}, {lat: coor_list[40004], lng: coor_list[40005]}, {lat: coor_list[40006], lng: coor_list[40007]}];
                      
                      //{lat: 41.273877, lng: -86.058145},{lat: 47.753731, lng: -125.359647}, {lat: 41.273877, lng: -85.058145}];
        //[{lat: 47.753731, lng: -125.359647}] //js_coords.coords; //
        var coords = [41.273877, -86.058145];
        //getClosestRoad(coords);
        
        var road_coords = [];
        for (i = 0; i < coor_list.length; i+=2)
            {
                //trying to use timers to delay it, but it isn't working
                setTimeout( function(i) {
                    var coordinate = {lat: coor_list[i], lng: coor_list[i+1]};
                    getClosestRoad(coordinate);
                    alert(i)
                }, 100, i);
                //alert(road_coord);
                //road_coords.push(road_coord);
            }
        setTimeout( function(roads_list) {
            var write_test = roads_list[0];
            //alert(roads_list.length);
            for(i=1; i<roads_list.length; i++) {
                write_test+="\n" + roads_list[i];
            }
            window.open('data:text/csv;charset=utf-8,' + escape(write_test));
        }, 1000, roads_list);
      }
    
  
    // Function: 
    // input: lat and lang coordinates (hard-coded above) in format {lat: 41.436, lng: -87.144}
    // outputs: coordinates of the closest road, and places a marker on our map
    function getClosestRoad(latLng) {
        marker.setMap(null);
        var request = {
            origin:latLng,
            destination:latLng,
            // .DRIVING: Indicates standard driving directions using the road network 
            travelMode: google.maps.DirectionsTravelMode.DRIVING
        };
        // 
        directionsService.route(request, function(response, status) {
            console.log(response)
            if (status == google.maps.DirectionsStatus.ZERO_RESULTS) {
                //alert("ZERO RESULTS");
            }
            if (status == google.maps.DirectionsStatus.OK) {
                var point=response.routes[0].legs[0];
                marker.setOptions({map:map, position:point.start_location});
                map.setCenter(point.start_location);
               
                var road = point.start_location.toString();
                
                //alert(response.routes[0].summary+'\n'+point.start_location.toString());
                //alert(point.start_location.toString());
                roads_list.push(road);
                //return road;
            }
        });
      }

    
