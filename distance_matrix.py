import sys
import simplejson
from urllib2 import urlopen #.request import urlopen
#from urllib2 import urlopen
import os
from geopy.distance import vincenty
import pulp
#import gsv_3images
#import caffe_3images
#import caffe_gsv_3images
import find_relevant_area



def get_distances(coordinates, final, matrix):
    apiKey = 'AIzaSyBpaOfrcYIpU-7jb-M4zOAyHgBpzoPEoqg'
    names_list = []
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
                    #matrix[i][j] = 0
                    do = "nothing"
                else:
                    destinations = destinations + end + "|"
                    destination_list.append(j)
        destinations = destinations[:-1]
        #REMEMBER limited to destination list of less than 100 (i think)
        if len(destinations)>0:
            urlstring = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=' + start + '&destinations=' + destinations + '&mode=driving&key=' + apiKey
            result = simplejson.load(urlopen(urlstring))
            for k in range(0, len(result['rows'][0].get("elements"))):
                resultString = result['rows'][0].get("elements")[k].get('distance').get('value')
                #resultString = resultString + " " + (result['rows'][0].get("elements")[k].get('distance').get('text'))
                s = str(coordinates[i][0]) + ", " + str(coordinates[i][1])
                e = str(coordinates[destination_list[k]][0]) + ", " + str(coordinates[destination_list[k]][1])
                if s not in names_list:
                    names_list.append(s)
                if e not in names_list:
                    names_list.append(e)
                points = (s, e)
                matrix[points] = resultString
                #matrix[i][destination_list[k]] = resultString
    return matrix, names_list

def getCrowDistance(coordinates):
    for i in range(len(coordinates)-1):
        for j in range(i+1, len(coordinates)):
            dist = vincenty(coordinates[i], coordinates[j]).km
            #print(i, j, dist)


def read_classified_points(file_name, scenery_type):
    classified_coord_list = []
    with open(file_name, 'r') as f:
        input_lines = f.read().splitlines()
    for x in input_lines:
        new_line = x.replace("[", "")
        new_line = new_line.replace("]", "")
        new_line = new_line.replace(",", "")
        new_line = new_line.replace('\'', "")
        line_list = new_line.split()
        if(line_list[2] == scenery_type or line_list[4] == scenery_type or line_list[6]==scenery_type):
            coordinates = [float(line_list[0]), float(line_list[1])]
            classified_coord_list.append(coordinates)
    return classified_coord_list

def route_ilp(dist, coord_names, max_dist):

    y = pulp.LpVariable.dicts("y", dist, lowBound=0, upBound=1, cat=pulp.LpInteger)
    mod = pulp.LpProblem("Scenic Routes", pulp.LpMaximize)
    # Objective
    mod += sum([y[k] for k in dist])

    # CONSTRAINTS:

    # route is shorter than max distance
    mod += sum([dist[k] * y[k] for k in dist]) <= max_dist

    # every node is visited no more than one time
    for point in range(1, len(coord_names)-1):
        mod += sum([y[k] for k in dist if coord_names[point] in k[0]]) <= 1
        mod += sum([y[k] for k in dist if coord_names[point] in k[1]]) <= 1
        mod += sum([y[k] for k in dist if coord_names[point] in k[0]]) == sum([y[k] for k in dist if coord_names[point] in k[1]])
    
    # start point is start point
    mod += sum([y[k] for k in dist if coord_names[0] in k[0]]) == 1
    mod += sum([y[k] for k in dist if coord_names[0] in k[1]]) == 0

    # end point is end point
    mod += sum([y[k] for k in dist if coord_names[len(coord_names)-1] in k[0]]) == 0
    mod += sum([y[k] for k in dist if coord_names[len(coord_names)-1] in k[1]]) == 1


    # Solve
    mod.solve()
    edge_list = []
    for t in dist:
        if(y[t].value() == 1):
            edge_list.append(t)
    return edge_list

def order_output(output_list, start, end):
    if(len(output_list) <=2):
        start_list = start.split(", ")
        start_list[0] = float(start_list[0])
        start_list[1] = float(start_list[1])
        end_list = start.split(", ")
        end_list[0] = float(end_list[0])
        end_list[1] = float(end_list[1])
        return([start_list, end_list])
    ordered_output = []
    while(start != end):
        for x in output_list:
            if(x[0] == start):
                coord_list = x[0].split(", ")
                coord_list[0] = float(coord_list[0])
                coord_list[1] = float(coord_list[1])
                ordered_output.append(coord_list)
                start = x[1]
    coord_list = start.split(", ")
    coord_list[0] = float(coord_list[0])
    coord_list[1] = float(coord_list[1])
    ordered_output.append(coord_list)
    return ordered_output


def get_waypoints(start, end, scenery, hours, minutes):
    # json conversions
        
    apiKey = 'AIzaSyDwkDK5bzGkwnkUz_0HtSs6Ab6NYq83-zQ'
    urlstring1 = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + start + "&key=" +apiKey
    start_info = simplejson.load(urlopen(urlstring1))
    start_coordinate = [start_info['results'][0].get("geometry").get("location").get("lat"), start_info['results'][0].get("geometry").get("location").get("lng")]
    
    urlstring2 = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + end + "&key=" + apiKey
    end_info = simplejson.load(urlopen(urlstring2))
    end_coordinate = [end_info['results'][0].get("geometry").get("location").get("lat"), end_info['results'][0].get("geometry").get("location").get("lng")]
    
   
    # time variable = hours + minutes
    time = int(hours)*60 + int(minutes)
    corners = find_relevant_area.find_relevant_area([start_coordinate, end_coordinate], time)
   
    coordinates = read_classified_points("testFile.csv", scenery)
    coordinates.append(end_coordinate)
    coordinates.insert(0, start_coordinate)
    
    # code to make sure coordinates within square defined by corners
    # maybe do this within read_classified_points
    # find min(x), max(x), min(y), max(y)
    
    w, h = len(coordinates), len(coordinates)
    distances = {}
    matrix = [[0 for x in range(w)] for y in range(h)]
    dist_dictionary, names_list = get_distances(coordinates, end_coordinate, distances)
    # what is max distance?
    max_distance = 25000000
    output_list = route_ilp(dist_dictionary, names_list, max_distance)
    # unsure if start and end are beginning/end of list yet
    string_start = str(start_coordinate[0]) + ", " + str(start_coordinate[1])
    string_end = str(end_coordinate[0]) + ", " + str(end_coordinate[1])
    list_of_points = order_output(output_list, string_start, string_end)
    #print(list_of_points)
    return list_of_points

if __name__ == '__main__':
#    #start = '49.7016339,-123.1558121' #vancouver
#    #end = '36.1699412,-115.1398296' #las vegas
#    start = '48.62995890000001, -124.7537899'
#    end = '48.7062475, -124.7531533'
#    #end = '47.6062095,-122.3320708' #seattle
#    # vancouver, seattle, sanFran, spokane, portland, bend, las vegas
#    #coordinates = [[49.7016339,-123.1558121], [47.6062095,-122.3320708], [37.7749295,-122.4194155], [47.6587802, -117.4260466], [45.5230622, -122.6764816], [44.0581728,-121.3153096], [36.1699412,-115.1398296]]
#   #vancouver, richmond, burnaby, delta
#    #coordinates = [[49.7016339,-123.1558121], [49.185992, -123.097537], [49.220953, -123.00881], [49.134848, -123.032913]] 
#    coordinates = read_classified_points("testFile.csv", "non-scenic")
#    w, h = len(coordinates), len(coordinates) 
#    distances = {}
#    matrix = [[0 for x in range(w)] for y in range(h)]
#    dist_dictionary, names_list = get_distances(coordinates, end, distances)
#    #print(dist_dictionary)
#    max_distance = 25000
#    #print(names_list)
#    output_list = route_ilp(dist_dictionary, names_list, max_distance)
#    print(order_output(output_list, start, end))
#    #getCrowDistance(coordinates)
#    #print(result['rows'][0].get("elements")[k].get('duration').get('value'))
#    #matrix[i][destination_list[k]] = result['rows'][0].get("elements")[k].get('duration').get('value')
    print(get_waypoints("2201+E+Newton+St,+Seattle,WA", "3324+NE+21st+Ave+Portland,OR+97212", "non-scenic", "22", "2"))
    


