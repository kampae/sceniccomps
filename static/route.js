var directionsService;
var map;
var routeArray;
var requestArray = [];
var renderArray = [];
var time = 0;


//initMap({{ waypoints|tojson }})

function initMap() 
{
    var waypointString = document.getElementById("myVar").value;
    
    var waypoints = JSON.parse(waypointString);
    console.log(waypoints);
    
    document.getElementById('routedeets').innerHTML = "" 
    document.getElementById('routedeets').innerHTML += "We found " + waypoints.length + " scenic points on your route!" + "<br />";
    
//    var wy = waypointString.substring(1, waypointString.length-2);
//    var waypoints = wy.split(",");
    directionsService = new google.maps.DirectionsService();
    map = new google.maps.Map(document.getElementById('map'), {
      zoom: 7,
      center: {lat: 47.607140, lng: -120.292142}
    });
    
    splitRoute(waypoints);
    generateRouteSections();
    
    var startMarker = new google.maps.Marker({
        position: {lat: waypoints[0][0], lng: waypoints[0][1]},
        map: map,
        label: 'A'
    });
    
    initializeStreetView(waypoints[0]);
    
    var endMarker = new google.maps.Marker({
        position: {lat: waypoints[waypoints.length - 1][0], lng: waypoints[waypoints.length - 1][1]},
        map: map,
        label: 'B'
    });
    
    // Drag Code Start
    var i = 0;
    var dragging = false;
        $('#dragbar').mousedown(function(e){
            e.preventDefault();
       
            dragging = true;
            var pano = $('#pano');
            var dragbar = $("#dragbar");
            var ghostbar = $('<div>',
                            {id:'ghostbar',
                            css: {
                                height: dragbar.outerHeight(),
                                width: dragbar.outerWidth(),
                                top: pano.offset().top,
                                bottom: pano.offset().bottom
                                }
                            }).appendTo('body');
       
            $(document).mousemove(function(e){
                ghostbar.css("top",e.pageY+2);
            });
        });

        $(document).mouseup(function(e){
        if (dragging) 
        {
           $('#map').css("height",e.pageY+2);
           $('#pano').css("top",e.pageY+2);
           $('#ghostbar').remove();
           $(document).unbind('mousemove');
           dragging = false;
        }
    });
    
    // Drag Code End
    
    
    
    
    
    
    
    
    
    
}

function splitRoute(waypoints) 
{
    if (waypoints.length <= 25) 
    {
        routeArray = [waypoints];
    }
    
    else{
        routeArray = [];

        for (var i=0; i < waypoints.length; i+=24)
        {
            var route = [];
            for (var j=0; j<25; j++)
            {
                if (i+j < waypoints.length) 
                {
                    route[j] = waypoints[i + j];
                }
            }

            routeArray.push(route);
        }
    }
}

function generateRouteSections() 
{
    requestArray = [];
    for (var h = 0; h<routeArray.length; h++) 
    {
        var route = routeArray[h];
        var waypts = [];
        var start;
        var end;
        
        start = {location: {lat: route[0][0], lng: route[0][1]}};
        
        for (var i = 1; i < route.length-1; i++)
        {
            waypts.push({
                location: {lat: route[i][0], lng: route[i][1]},
                stopover: true
            });
        }
        
        end = {location: {lat: route[route.length-1][0], lng: route[route.length-1][1]}};
    
    
        var request = {
            origin: start,
            destination: end,
            waypoints: waypts,
            travelMode: google.maps.TravelMode.DRIVING
        };

        requestArray.push({route: route, request: request})
    }
    
    processRequests();
}

function processRequests()
{
    var i = 0;
    
    function submitRequest() 
    {
        directionsService.route(requestArray[i].request, directionResults); 
    }
    
    function directionResults(result, status)
    {
        if (status == google.maps.DirectionsStatus.OK)
        {
            renderArray[i] = new google.maps.DirectionsRenderer({
//                suppressMarkers: true,
                suppressInfoWindows: true,
                markerOptions: {
                icon: {
                    path: google.maps.SymbolPath.CIRCLE,
                    scale: 2,
                    strokeColor: 'purple'
                }}
            });
            
            //renderArray[i] = new google.maps.DirectionsRenderer();
            
            for (var j = 0; j < result["routes"][0]["legs"].length; j++)
            {
                time += result["routes"][0]["legs"][j]["duration"]["value"];
            }
            
            renderArray[i].setMap(map);
            renderArray[i].setDirections(result);
            if (i == 0)
            {
                document.getElementById('directions').innerHTML = ""; 
            }
            renderArray[i].setPanel(document.getElementById('directions'));
            nextRequest();
        }
    }
    
    function nextRequest() 
    {
        i++;
        
        if (i >= requestArray.length)
        {
            return;
        }
        
        submitRequest();
    }
    
    submitRequest();
    var hours = Math.floor(time/3600);
    var r = time%3600;
    var minutes = Math.floor(r/60);
    var seconds = time%60;
    
    document.getElementById('routedeets').innerHTML += "<br />" + "The total length of your trip is " + hours + " hours, " + minutes + " minutes, and " + seconds + " seconds."; 
    
//    map.setCenter(requestArray[0][0]);
}

function initializeStreetView(coords) {
    var startpt = {lat: coords[0], lng: coords[1]};
//    var map = new google.maps.Map(document.getElementById('map'), {
//        center: fenway,
//        zoom: 14
//    });
    var panorama = new google.maps.StreetViewPanorama(
        document.getElementById('pano'), {
            position: startpt,
            pov: {
                heading: 10,
                pitch: 1
            }
        });
    map.setStreetView(panorama);
}

function onReturnButton()
{
    //var inputs = getInputs();
    var url = 'http://localhost:5000/';
    window.location.href="http://localhost:5000/";
    
//    xmlHttpRequest = new XMLHttpRequest();
//    xmlHttpRequest.open('get', url);
//    
//    xmlHttpRequest.send(null);
}

