import googlemaps
import simplejson
from urllib2 import urlopen
#from urllib.request import urlopen


'''
Given a max time, start point, and end point, determines if the trip from start to end can be achieved
in the provided amount of time. Returns True if so, False if not.
'''

def check_max_time(max_time, start, end):
    
    api_key = 'AIzaSyBpaOfrcYIpU-7jb-M4zOAyHgBpzoPEoqg'
    urlstring = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=' + start + '&destinations=' + end + '&mode=driving&key=' + api_key
    result = simplejson.load(urlopen(urlstring))
    min_time = result['rows'][0]['elements'][0]['duration'].get('value')
    
    return max_time >= min_time

'''
Given an address, determines if that address is valid or not.
Returns True if so, False if not.
'''
def check_address(address):
    api_key = 'AIzaSyCcZCqAof3-hzC_LuvE_iyBe56x79C4WD4'
    gmaps = googlemaps.Client(api_key)
    coords = gmaps.geocode(address)
    
    return len(coords) != 0