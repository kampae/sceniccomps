var directionsService;
var map;
var routeArray;
var requestArray = [];
var renderArray = [];
var time = 0;


//initialize the map with the start and end point, and centered at the start
//set up the route information box
//begin breaking up the waypoints as needed
function initMap() 
{
    var waypointString = document.getElementById("myVar").value;
    
    var waypoints = JSON.parse(waypointString);
    console.log(waypoints);
    
    document.getElementById('routedeets').innerHTML = "" 
    document.getElementById('routedeets').innerHTML += "We found " + waypoints.length + " scenic points on your route!" + "<br />";
    
    directionsService = new google.maps.DirectionsService();
    map = new google.maps.Map(document.getElementById('map'), {
      zoom: 7,
      center: {lat: waypoints[0][0], lng: waypoints[0][1]}
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
    
}

//breaks up the waypoints into 25 point segments
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

//creates a route for each segment of waypoints
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

//ensures that the route is created in order
//manages the asynchronicity
//creates the directions renders for each route and sets the map options
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
        
}

//initializes the street view pano which is displayed at the bottom of the screen
function initializeStreetView(coords) {
    var startpt = {lat: coords[0], lng: coords[1]};
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

//creates the home button which returns the user to the start page
function onHomeButton()
{
    var url = 'http://localhost:8000/';
    window.location.href="http://localhost:8000/";
}

