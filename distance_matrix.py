import sys
import simplejson
from urllib2 import urlopen
#from urllib.request import urlopen
import os
from geopy.distance import vincenty
import pulp
#import gsv_3images
#import caffe_3images
#import caffe_gsv_3images
import find_relevant_area
import new_heuristic


'''
Uses google maps distance API to calculate the road distances between points in coordinates. Only includes distances between
two points a and b in matrix if moving from a to b moves closer to the endpoint. 
NOT BEING USED ANYMORE
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
        
        #destination list must be limited to less than 100
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
                distance1 = vincenty(coordinates[i], final).km
                distance2 = vincenty(coordinates[j], final).km
                
                if distance2 <= distance1:
                    result_distance = vincenty(coordinates[i], coordinates[j]).km
                    result_time = (result_distance*1.4) + 6.0824 #(result_distance*1.875)+17.967
                    s = str(coordinates[i][0]) + ", " + str(coordinates[i][1])
                    e = str(coordinates[j][0]) + ", " + str(coordinates[j][1])
                    points = (s, e)
                    matrix[points] = result_time
                    
    return matrix, names_list

'''
Given a distance threshold it combines points that are within that distance from each other.
It returns a list of coordinates, where only one coordinate from each cluster is included,
and a dictionary of clusters
'''
def cluster_coordinates(coordinates, threshold):
    clusters = {}
    reduced_coordinates = []
    in_cluster = []
    for i in range(1, len(coordinates)-2):
        s = str(coordinates[i][0]) + ", " + str(coordinates[i][1])
        if(s not in in_cluster):
            reduced_coordinates.append(coordinates[i])
            for j in range(i+1, len(coordinates)-1):
                distance = vincenty(coordinates[i], coordinates[j]).km
                e = str(coordinates[j][0]) + ", " + str(coordinates[j][1])
                if(distance < threshold):
                    in_cluster.append(e)
                    if s in clusters:
                        existing_cluster = clusters[s]
                        existing_cluster.append(e)
                        clusters[s] = existing_cluster
                    else:
                        clusters[s] = [e]   
            
    return reduced_coordinates, clusters

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
        new_line = new_line.replace('\'', "")
        line_list = new_line.split(",")

        if(line_list[2][1:] == scenery_type or line_list[4][1:] == scenery_type or line_list[6][1:]==scenery_type):
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

    #checks if the point is within the relevant square of area, 
    #and makes sure the point is not in Canada
    outside_square = coord[0] < min_x or coord[0] > max_x or coord[1] < min_y or coord[1] > max_y
    in_top_canada = (coord[0] > 48.395038) and (coord[1] < -123.149298)
    in_bottom_canada = (coord[0] > 48.303611) and (coord[1] > -124.001312) and (coord[1] < -123.471909)
    in_canada = in_top_canada or in_bottom_canada
    
    return (not outside_square) and (not in_canada)



'''
Takes in a list of coordinates and a max distance and uses an ILP to find a subset
of coordinates to visit. Tries to maximize the size of the subset without exceeding
the max time.
'''
def route_ilp(dist, coord_names, max_dist, clusters):

    y = pulp.LpVariable.dicts("y", dist, lowBound=0, upBound=1, cat=pulp.LpInteger)
    mod = pulp.LpProblem("Scenic Routes", pulp.LpMaximize)
    # Objective
    mod += sum([y[k]*(len(clusters[k[1]])+1) for k in dist])

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
    time_sum = 0
    for t in dist:
        if(y[t].value() == 1):
            edge_list.append(t)
            time_sum = time_sum + dist[t]
    
    return edge_list


'''
Takes the subset of coordinates produced by the ILP and returns them in the order
in which they will be visited, with clustered points added back into the path. 
If the path exceeds the time limit, it continuously removes the points until the route
fits the time constraint
'''
def order_output(output_list, start, end, clusters, time):
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
                if(len(clusters[x[0]]) > 0):
                    ordered = order_clusters(clusters[x[0]], end)
                    for o in ordered:
                        o_coord = o.split(", ")
                        o_coord[0] = float(o_coord[0])
                        o_coord[1] = float(o_coord[1])
                        ordered_output.append(o_coord)
                start = x[1]
    
    coord_list = start.split(", ")
    coord_list[0] = float(coord_list[0])
    coord_list[1] = float(coord_list[1])
    ordered_output.append(coord_list)
    
    output_list = []
    for coordinates in ordered_output:
        if coordinates not in output_list:
            output_list.append(coordinates)
    
    reduced_output_list = reduce_path(output_list, time)
    
    return reduced_output_list

'''
Returns the list of cluster coordinates in order from
farthest to the end point to closest to the end
'''
def order_clusters(cluster, end):
    ordered = sorted(cluster, key = lambda coord: calc_distance(coord, end), reverse = True)
    return ordered

'''
Removes points from the path until is fits within the max time.
The highest cost point (the point that adds the most time to the route)
is removed at each iteration
'''
def reduce_path(path, max_time):
    path_time = new_heuristic.path_length(path)
    while(path_time > max_time):
        print("$$$$$$$$$$$removing a point")
        path = new_heuristic.remove_point(1, path)
        path_time = new_heuristic.path_length(path)
    return path

'''
Calculates the distance between two coordinates given as strings
'''
def calc_distance(item, end):
    coord = item.split(", ")
    coord[0] = float(coord[0])
    coord[1] = float(coord[1])
    end_list = end.split(", ")
    end_list[0] = float(end_list[0])
    end_list[1] = float(end_list[1])
    return vincenty(coord, end_list).km


'''
Calls the new heuristic for the orienteering problem 
("A Fast and Effective Heuristic for the Orienteering Problem", Chao et al.)
Given a start and end address, scenery preference and time given in hours and minutes
it returns a route that fits those constraints. 
'''
def call_new_heuristic(start, end, scenery, hours, minutes):
    api_key = 'AIzaSyDwkDK5bzGkwnkUz_0HtSs6Ab6NYq83-zQ'
    urlstring1 = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + start + "&key=" +api_key
    start_info = simplejson.load(urlopen(urlstring1))
    start_coordinate = [start_info['results'][0].get("geometry").get("location").get("lat"), start_info['results'][0].get("geometry").get("location").get("lng")]
    
    urlstring2 = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + end + "&key=" + api_key
    end_info = simplejson.load(urlopen(urlstring2))
    end_coordinate = [end_info['results'][0].get("geometry").get("location").get("lat"), end_info['results'][0].get("geometry").get("location").get("lng")]
    
    time = (int(hours)*60 + int(minutes))
    
    coordinates = read_classified_points("ClassifiedPoints/all_classified_points.csv", scenery, start_coordinate, end_coordinate, time)
    
    coordinates.append(end_coordinate)
    coordinates.insert(0, start_coordinate)
    
    route = new_heuristic.orienteering_heuristic(start_coordinate, end_coordinate, coordinates, time)
    
    return route

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
    
   
    time = (int(hours)*60 + int(minutes))
    #corners = find_relevant_area.find_relevant_area([start_coordinate, end_coordinate], time)

    coordinates = read_classified_points("ClassifiedPoints/all_classified_points.csv", scenery, start_coordinate, end_coordinate, time)
            
    
    coordinates.append(end_coordinate)
    coordinates.insert(0, start_coordinate)
    print("!!!!!!!", len(coordinates))
    
    threshold = 1
    
    #need to fiddle around with starting values for very high number of coords
    if len(coordinates) > 2000:
        threshold = 8
    
    reduced_coordinates, clusters = cluster_coordinates(coordinates, threshold)
    
    while len(reduced_coordinates) > 80:
        print("LENGTH LENGTH LENGTH: ", len(reduced_coordinates))
        threshold += 1
        print("THRESHOLD THRESHOLD: ", threshold)
        reduced_coordinates, clusters = cluster_coordinates(coordinates, threshold)
    
    print("LENGTH LENGTH LENGTH: ", len(reduced_coordinates))   
    reduced_coordinates.append(end_coordinate)
    reduced_coordinates.insert(0, start_coordinate)
    
    print("!!^!!!!", len(reduced_coordinates))
        
    distances = {}
    dist_dictionary, names_list = get_crow_distance_matrix(reduced_coordinates, end_coordinate, distances)
    
    for coord in coordinates:
        lat_lng = str(coord[0]) + ', ' + str(coord[1])
        if lat_lng not in clusters:
            clusters[lat_lng] = []
    
    output_list = route_ilp(dist_dictionary, names_list, time, clusters)
    string_start = str(start_coordinate[0]) + ", " + str(start_coordinate[1])
    string_end = str(end_coordinate[0]) + ", " + str(end_coordinate[1])
    print(string_start, string_end)
    list_of_points = order_output(output_list, string_start, string_end, clusters, time)
    print(len(list_of_points), "************")
    
    return list_of_points
