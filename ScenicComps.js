function initAutocomplete() 
{
    var autocomplete = new google.maps.places.Autocomplete( (document.getElementById('start_input')),
        {types: ['geocode']});
    
    var autocomplete = new google.maps.places.Autocomplete( (document.getElementById('end_input')),
        {types: ['geocode']});
}

function getInputs()
{
    /**var geocoded_start = new XMLHttpRequest();          
    geocoded_start.open("GET", "https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=AIzaSyCPn6VnGvKDcPjjnq9utmKMwVxPv0gln5w", false);
    geocoded_start.send(); 
    
    var startCoords = [];
    startCoords.push(geocoded_start["results"["geometry"["location"["lat"]]]]);    
    startCoords.push(geocoded_start["results"["geometry"["location"["lng"]]]]); **/
    
    var startAddress = document.getElementById("start_input").value;
    
    var endAddress = document.getElementById("end_input").value;
    
    var maxTime = + document.getElementById("hours_input").value * 60 + + document.getElementById("minutes_input").value;
    //maxTime += document.getElementById("minutes_input").value;
    
    var scenery = document.getElementById("scenery_select").value;
    
    var inputs = [startAddress, endAddress, maxTime, scenery];
    
    // deal with invalid inputs
    
    alert(inputs);
    return inputs;
}
