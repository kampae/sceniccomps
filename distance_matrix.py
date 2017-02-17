import sys
import simplejson
from urllib2 import urlopen
#from urllib.request import urlopen
#from urllib2 import urlopen
import os
from geopy.distance import vincenty
import pulp
#import gsv_3images
#import caffe_3images
#import caffe_gsv_3images
import find_relevant_area


'''
Uses google maps distance API to calculate the road distances between points in coordinates. Only includes distances between
two points a and b in matrix if moving from a to b moves closer to the endpoint.
'''
def get_distances(coordinates, final, matrix):
    api_key = 'AIzaSyBpaOfrcYIpU-7jb-M4zOAyHgBpzoPEoqg'
    names_list = []
    
    for i in range(0, len(coordinates)):
        destinations = ""
        destination_list = []
        
        for j in range(0, len(coordinates)):
            if i != j:
                start = str(coordinates[i][0]) + ',' + str(coordinates[i][1])
                end = str(coordinates[j][0]) + ',' + str(coordinates[j][1])
                distance1 = vincenty(coordinates[i], final).miles
                distance2 = vincenty(coordinates[j], final).miles
                
                if distance2 <= distance1:
                    destinations = destinations + end + "|"
                    destination_list.append(j)
        destinations = destinations[:-1]
        
        #REMEMBER limited to destination list of less than 100
        if len(destinations) > 0:
            urlstring = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=' + start + '&destinations=' + destinations + '&mode=driving&key=' + api_key
            result = simplejson.load(urlopen(urlstring))
            
            for k in range(0, len(result['rows'][0].get("elements"))):
                result_string = result['rows'][0].get("elements")[k].get('duration').get('value')
                s = str(coordinates[i][0]) + ", " + str(coordinates[i][1])
                e = str(coordinates[destination_list[k]][0]) + ", " + str(coordinates[destination_list[k]][1])
                if s not in names_list:
                    names_list.append(s)
                if e not in names_list:
                    names_list.append(e)
                points = (s, e)
                matrix[points] = result_string
                
    return matrix, names_list


'''
Calculate the distances (as the crow flies) between points in coordinates. Only includes distances between
two points a and b in matrix if moving from a to b moves closer to the endpoint.
'''
def get_crow_distance_matrix(coordinates, final, matrix):
    names_list = []
    
    for i in range(0, len(coordinates)):
        destinations = ""
        destination_list = []
        name = str(coordinates[i][0]) + ", " + str(coordinates[i][1])
        names_list.append(name)
        
        for j in range(0, len(coordinates)):
            if i != j:
                distance1 = vincenty(coordinates[i], final).miles
                distance2 = vincenty(coordinates[j], final).miles
                
                if distance2 <= distance1:
                    result_distance = vincenty(coordinates[i], coordinates[j]).km
                    result_time = result_distance*60
                    s = str(coordinates[i][0]) + ", " + str(coordinates[i][1])
                    e = str(coordinates[j][0]) + ", " + str(coordinates[j][1])
                    points = (s, e)
                    matrix[points] = result_time
                    
    return matrix, names_list

'''
Reads from a file of classified road coordinates and creates a list of only coordinates
with the given scenery classification.
'''
def read_classified_points(file_name, scenery_type, start, end, time):
    count = 0
    classified_coord_list = []
    corners = find_relevant_area.find_relevant_area([start, end], time)
    
    with open(file_name, 'r') as f:
        input_lines = f.read().splitlines()
        
    for x in input_lines:
        new_line = x.replace("[", "")
        new_line = new_line.replace("]", "")
        new_line = new_line.replace(",", "")
        new_line = new_line.replace('\'', "")
        line_list = new_line.split()
        
        if(line_list[2] == scenery_type or line_list[4] == scenery_type or line_list[6]==scenery_type):
            count += 1
            coordinates = [float(line_list[0]), float(line_list[1])]
            if coord_in_range(coordinates, corners):
                classified_coord_list.append(coordinates)
    
    print("BEFORE: ", count)
    print("AFTER: ", len(classified_coord_list))
    return classified_coord_list

'''
Checks if passed coord is in the relevant area, given the start and end coordinates
and max time.
Returns True or False
'''
def coord_in_range(coord, corners):

    x = []
    y = []
    
    for pt in corners:
        x.append(pt[0])
        y.append(pt[1])
        
    min_x = min(x)
    max_x = max(x)
    min_y = min(y)
    max_y = max(y)

    return not(coord[0] < min_x or coord[0] > max_x or coord[1] < min_y or coord[1] > max_y)



'''
Takes in a list of coordinates and a max distance and uses an ILP to find a subset
of coordinates to visit. Tries to maximize the size of the subset without exceeding
the max time.
'''
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


'''
Takes the subset of coordinates produced by the ILP and returns them in the order
in which they will be visited.
'''
def order_output(output_list, start, end):
    if(len(output_list) <2):
        start_list = start.split(", ")
        start_list[0] = float(start_list[0])
        start_list[1] = float(start_list[1])
        end_list = end.split(", ")
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

'''
Converts the inputs into the necessary format (ex. addresses to coordinates) and creates the distance_matrix,
calls the ILP and order_output and produces the final list of points that is passed back to flask_test.py.
'''
def get_waypoints(start, end, scenery, hours, minutes):
    api_key = 'AIzaSyDwkDK5bzGkwnkUz_0HtSs6Ab6NYq83-zQ'
    urlstring1 = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + start + "&key=" +api_key
    start_info = simplejson.load(urlopen(urlstring1))
    start_coordinate = [start_info['results'][0].get("geometry").get("location").get("lat"), start_info['results'][0].get("geometry").get("location").get("lng")]
    
    urlstring2 = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + end + "&key=" + api_key
    end_info = simplejson.load(urlopen(urlstring2))
    end_coordinate = [end_info['results'][0].get("geometry").get("location").get("lat"), end_info['results'][0].get("geometry").get("location").get("lng")]
    
   
    time = (int(hours)*60 + int(minutes))*60
    #corners = find_relevant_area.find_relevant_area([start_coordinate, end_coordinate], time)

    coordinates = read_classified_points("ClassifiedPoints/classified_points14400_Tester.csv", scenery, start_coordinate, end_coordinate, time)
            
    
    coordinates.append(end_coordinate)
    coordinates.insert(0, start_coordinate)

    
    w, h = len(coordinates), len(coordinates)
    distances = {}
    matrix = [[0 for x in range(w)] for y in range(h)]
    dist_dictionary, names_list = get_crow_distance_matrix(coordinates, end_coordinate, distances)
    max_distance = time
    output_list = route_ilp(dist_dictionary, names_list, max_distance)
    string_start = str(start_coordinate[0]) + ", " + str(start_coordinate[1])
    string_end = str(end_coordinate[0]) + ", " + str(end_coordinate[1])
    list_of_points = order_output(output_list, string_start, string_end)
    
#    print(min(dist_dictionary.values()))
#    print(max(dist_dictionary.values()))
    
    return list_of_points

