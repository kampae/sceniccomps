//funtion to provide autocomplete on start/end addresses
function initAutocomplete()
{

    var autocomplete = new google.maps.places.Autocomplete( (document.getElementById('start_input')),
        {types: ['geocode']});
    
    var autocomplete = new google.maps.places.Autocomplete( (document.getElementById('end_input')),
        {types: ['geocode']});
}

//sets error message on bad input depending on what is wrong
function setBadinput(badInput)
{

    if(badInput == 1)
    {
        document.getElementById('badinput').style.display = 'block';
        document.getElementById('badinput').innerHTML += "Please enter a valid start address.";
    }
    if(badInput == 2)
    {
        document.getElementById('badinput').style.display = 'block';
        document.getElementById('badinput').innerHTML += "Please enter a valid end address.";
    }
    if(badInput == 3)
    {
        document.getElementById('badinputTime').style.display = 'block';
        document.getElementById('badinputTime').innerHTML += "Your destination cannot be reached in the provided time limit.";
    }
}

//gets and returns user inputs to the different fields
function getInputs()
{   
    var startAddress = document.getElementById("start_input").value;
    
    var endAddress = document.getElementById("end_input").value;
    
    var maxTime = + document.getElementById("hours_input").value * 60 + + document.getElementById("minutes_input").value;
    
    var scenery = document.getElementById("scenery_select").value;
    
    var inputs = [startAddress, endAddress, maxTime, scenery];
    
    var url = 'route/';
    
    xmlHttpRequest = new XMLHttpRequest();
    xmlHttpRequest.open('get', url);
    
    xmlHttpRequest.onreadystatechange = function()
    {
        if (xmlHttpRequest.readyState == 4 && xmlHttpRequest == 200)
            {
                getInputsCallback(xmlHttpRequest.responseText);
            }
    };
    xmlHttpRequest.send();
    
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
