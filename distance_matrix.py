import sys
import simplejson
import urllib
from urllib2 import urlopen
import os
from geopy.distance import vincenty
import gsv_3images
import caffe_3images
import caffe_gsv_3images


def get_distances_slow(coordinates, final, matrix):
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

def get_distances(coordinates, final, matrix):
    apiKey = 'AIzaSyBpaOfrcYIpU-7jb-M4zOAyHgBpzoPEoqg'
    for i in range(0, len(coordinates)):
        destinations = ""
        destination_list = []
        for j in range(0, len(coordinates)):
            if i!=j:
                start = str(coordinates[i][0]) + ',' + str(coordinates[i][1])
                end = str(coordinates[j][0]) + ',' + str(coordinates[j][1])
                distance1 = vincenty(coordinates[i], final).miles
                distance2 = vincenty(coordinates[j], final).miles
                if distance2>distance1:
                    matrix[i][j] = 0
                else:
                    destinations = destinations + end + "|"
                    destination_list.append(j)
        destinations = destinations[:-1]
        #REMEMBER limited to destination list of less than 100 (i think)
        if len(destinations)>0:
            urlstring = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=' + start + '&destinations=' + destinations + '&mode=driving&key=' + apiKey
            result = simplejson.load(urlopen(urlstring))
            for k in range(0, len(result['rows'][0].get("elements"))):
                #print(result['rows'][0].get("elements")[k].get('duration').get('value'))
                matrix[i][destination_list[k]] = result['rows'][0].get("elements")[k].get('duration').get('value')
    return matrix

def get_scenic_coordinates(coords, scenery):
    coordinates = []
    for item in coords:
        if item[0]==scenery:
            coordinates.append(item[1])
    return coordinates

if __name__ == '__main__':
    start = '49.7016339,-123.1558121' #vancouver
    end = '36.1699412,-115.1398296' #las vegas
    
    # vancouver, seattle, sanFran, spokane, portland, bend, las vegas
    coords = [[49.7016339,-123.1558121], [47.6062095,-122.3320708], [37.7749295,-122.4194155], [47.6587802, -117.4260466], [45.5230622, -122.6764816], [44.0581728,-121.3153096], [36.1699412,-115.1398296]]
  

    #print(get_distances(coordinates, end, matrix))
    #coords = [[40.811306, -73.966917]]
    coordinates = caffe_gsv_3images.getClassifications(coords)
    coordinates = get_scenic_coordinates(coordinates, 'non-scenic')
    w, h = len(coordinates), len(coordinates) 
    matrix = [[0 for x in range(w)] for y in range(h)]
    print(get_distances(coordinates, end, matrix))