def check_max_time(max_time):
    
    start = "44.706885,-93.713955"
    destinations = "44.849651,-92.714665"
    apiKey = 'AIzaSyBpaOfrcYIpU-7jb-M4zOAyHgBpzoPEoqg'
    
    urlstring = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=' + start + '&destinations=' + destinations + '&mode=driving&key=' + apiKey
    
    result = simplejson.load(urlopen(urlstring))
    min_time = result['rows'][0]['elements'][0]['duration'].get('value')
    
    return max_time >= min_time