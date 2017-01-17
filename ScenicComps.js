function initAutocomplete() 
{
    var autocomplete = new google.maps.places.Autocomplete( (document.getElementById('start_input')),
        {types: ['geocode']});
}
