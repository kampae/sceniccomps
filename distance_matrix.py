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
                #resultString = result['rows'][0].get("elements")[k].get('duration').get('text')
                resultString = resultString + " " + (result['rows'][0].get("elements")[k].get('distance').get('text'))
                matrix[i][destination_list[k]] = resultString
    return matrix

def getCrowDistance(coordinates):
    for i in range(len(coordinates)-1):
        for j in range(i+1, len(coordinates)):
            dist = vincenty(coordinates[i], coordinates[j]).km
            print(i, j, dist)

def get_scenic_coordinates(coords, scenery):
    coordinates = []
    for item in coords:
        if item[0]==scenery:
            coordinates.append(item[1])
    return coordinates


if __name__ == '__main__':
    start = '49.7016339,-123.1558121' #vancouver
    #end = '36.1699412,-115.1398296' #las vegas
    end = '47.6062095,-122.3320708' #seattle
    # vancouver, seattle, sanFran, spokane, portland, bend, las vegas
    #coordinates = [[49.7016339,-123.1558121], [47.6062095,-122.3320708], [37.7749295,-122.4194155], [47.6587802, -117.4260466], [45.5230622, -122.6764816], [44.0581728,-121.3153096], [36.1699412,-115.1398296]]
   #vancouver, richmond, burnaby, delta
    coordinates = [[49.7016339,-123.1558121], [49.185992, -123.097537], [49.220953, -123.00881], [49.134848, -123.032913]] 
    w, h = len(coordinates), len(coordinates) 
    matrix = [[0 for x in range(w)] for y in range(h)]

    print(get_distances(coordinates, end, matrix))
    getCrowDistance(coordinates)
    #print(result['rows'][0].get("elements")[k].get('duration').get('value'))
    #matrix[i][destination_list[k]] = result['rows'][0].get("elements")[k].get('duration').get('value')


