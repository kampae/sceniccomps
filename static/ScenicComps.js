function initAutocomplete() 
{
    var autocomplete = new google.maps.places.Autocomplete( (document.getElementById('start_input')),
        {types: ['geocode']});
    
    var autocomplete = new google.maps.places.Autocomplete( (document.getElementById('end_input')),
        {types: ['geocode']});
}

function getInputs()
{   
    var startAddress = document.getElementById("start_input").value;
    
    var endAddress = document.getElementById("end_input").value;
    
    var maxTime = + document.getElementById("hours_input").value * 60 + + document.getElementById("minutes_input").value;
    
    var scenery = document.getElementById("scenery_select").value;
    
    var inputs = [startAddress, endAddress, maxTime, scenery];
    
    // deal with invalid inputs
    
    document.location.href = 'http://localhost:5000/' + startAddress + "/" + endAddress + "/" + maxTime + "/" + scenery + "/";
        
        //'file:///Users/evierosenberg/Desktop/Comps/sceniccomps/route.html';
    
    return inputs;
}



function onFindRoute()
{
    var inputs = getInputs();
    var url = 'http://localhost:5000/map/';
    xmlHttpRequest = new XMLHttpRequest();
    xmlHttpRequest.open('get', url);
    
    xmlHttpRequest.send(null);
}
