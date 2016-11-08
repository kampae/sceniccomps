import sys
import simplejson
import urllib
from urllib.request import urlopen
import os
from geopy.distance import vincenty


def get_distances(coordinates, final, matrix):
    apiKey = 'AIzaSyBpaOfrcYIpU-7jb-M4zOAyHgBpzoPEoqg'
    for i in range(0, len(coordinates)):
        for j in range(0, len(coordinates)):
            if i!=j:
                start = str(coordinates[i][0]) + ',' + str(coordinates[i][1])
                end = str(coordinates[j][0]) + ',' + str(coordinates[j][1])
                distance1 = vincenty(coordinates[i], final).miles
                distance2 = vincenty(coordinates[j], final).miles
                if distance2>distance1:
                    matrix[i][j] = 0
                else:
                    urlstring = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=' + start + '&destinations=' + end + '&mode=driving&key=' + apiKey
                    result = simplejson.load(urlopen(urlstring))
                    matrix[i][j] = result['rows'][0].get("elements")[0].get('duration').get('value')
    return matrix

if __name__ == '__main__':
    start = '49.7016339,-123.1558121'
    end = '36.1699412,-115.1398296'
    #seattle, sanFran, spokane, portland, bend
    coordinates = [[47.6062095,-122.3320708], [37.7749295,-122.4194155], [47.6587802, -117.4260466], [45.5230622, -122.6764816], [44.0581728,-121.3153096]]
    w, h = len(coordinates), len(coordinates) 
    matrix = [[0 for x in range(w)] for y in range(h)] 
    print(get_distances(coordinates, end, matrix))