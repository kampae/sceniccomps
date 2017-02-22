function initAutocomplete()
{

    var autocomplete = new google.maps.places.Autocomplete( (document.getElementById('start_input')),
        {types: ['geocode']});
    
    var autocomplete = new google.maps.places.Autocomplete( (document.getElementById('end_input')),
        {types: ['geocode']});
}

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
        document.getElementById('badinput').style.display = 'block';
        document.getElementById('badinput').innerHTML += "Your destination cannot be reached in the provided time limit.";
    }
}

function getInputs()
{   
    var startAddress = document.getElementById("start_input").value;
    
    var endAddress = document.getElementById("end_input").value;
    
    var maxTime = + document.getElementById("hours_input").value * 60 + + document.getElementById("minutes_input").value;
    
    var scenery = document.getElementById("scenery_select").value;
    
    var inputs = [startAddress, endAddress, maxTime, scenery];
    
    // deal with invalid inputs
    
//    document.location.href = 'http://localhost:5000/route/'; 
//        + startAddress + "/" + endAddress + "/" + maxTime + "/" + scenery + "/";
    
    var url = 'route/'; //'http://localhost:5000/' + startAddress + "/" + //endAddress + "/" + maxTime + "/" + scenery + "/";
    
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
        
        //'file:///Users/evierosenberg/Desktop/Comps/sceniccomps/route.html';
    //alert(inputs);

//    document.location.href = 'file:///Users/evierosenberg/Desktop/Comps/sceniccomps/route.html';
        
        //'http://localhost:5000/' + startAddress + "/" + endAddress + "/" + maxTime + "/" + scenery + "/";
    
    return inputs;
}

function getInputsCallback(responseText)
{
    
}



function onFindRoute()
{
    var inputs = getInputs();
    var url = 'http://localhost:5000/map/';
    xmlHttpRequest = new XMLHttpRequest();
    xmlHttpRequest.open('get', url);
    
    xmlHttpRequest.send(null);
}
