import sys
import simplejson
#from urllib2 import urlopen
#from urllib.request import urlopen
from urllib2 import urlopen
import os
from geopy.distance import vincenty
import pulp
#import gsv_3images
#import caffe_3images
#import caffe_gsv_3images
import find_relevant_area


'''
Uses google maps distance API to calculate the road distances between points in coordinates. Only includes distances between
two points a and b in matrix if moving from a to b moves closer to the endpoint. NOT BEING USED CURRENTLY
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
    clusters = {}
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
                    if(result_time < 5 and i != 0 and i != len(coordinates)-1 and  j != 0 and j != len(coordinates)-1):
                        if s in clusters:
                            existing_cluster = clusters[s]
                            existing_cluster.append(e)
                            clusters[s] = existing_cluster
                        else:
                            clusters[s] = [e]
                    else:
                        matrix[points] = result_time
                    
    return matrix, names_list, clusters

'''
Reads from a file of classified road coordinates and creates a list of only coordinates
with the given scenery classification.
'''
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
    for t in dist:
        if(y[t].value() == 1):
            edge_list.append(t)
    
    return edge_list


'''
Takes the subset of coordinates produced by the ILP and returns them in the order
in which they will be visited.
'''
def order_output(output_list, start, end, clusters):
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
    
    return ordered_output


def order_clusters(cluster, end):
    ordered = sorted(cluster, key = lambda coord: calc_distance(coord, end), reverse = True)
    return ordered

def calc_distance(item, end):
    coord = item.split(", ")
    coord[0] = float(coord[0])
    coord[1] = float(coord[1])
    end_list = end.split(", ")
    end_list[0] = float(end_list[0])
    end_list[1] = float(end_list[1])
    return vincenty(coord, end_list).km



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
    corners = find_relevant_area.find_relevant_area([start_coordinate, end_coordinate], time)

    coordinates = read_classified_points("ClassifiedPoints/classified_points14400_Tester.csv", scenery)
    coordinates.append(end_coordinate)
    coordinates.insert(0, start_coordinate)

    
    w, h = len(coordinates), len(coordinates)
    distances = {}
    matrix = [[0 for x in range(w)] for y in range(h)]
    dist_dictionary, names_list, clusters= get_crow_distance_matrix(coordinates, end_coordinate, distances)
    
    for coord in coordinates:
        lat_lng = str(coord[0]) + ',' + str(coord[1])
        if lat_lng not in clusters:
            clusters[lat_lng] = []

    max_distance = time
    output_list = route_ilp(dist_dictionary, names_list, max_distance, clusters)
    string_start = str(start_coordinate[0]) + ", " + str(start_coordinate[1])
    string_end = str(end_coordinate[0]) + ", " + str(end_coordinate[1])
    list_of_points = order_output(output_list, string_start, string_end, clusters)
    
    return list_of_points

###### NEW HEURISTIC
###### initialization


'''
finds the top n points with the largest distance from points a and b
and returns a list of those coordinates
'''
def farthest_points(a, b, coordinates, n):
    distance_list = []
    farthest_distances = []
    farthest_points = []
    for i in range(0, len(coordinates)):
         distance1 = vincenty(coordinates[i], a).km
         distance2 = vincenty(coordinates[i], b).km
         total_distance = distance1 + distance2
         distance_list.append(total_distance)
    min_value = distance_list[0]
    min_index = 0
    farthest_points.append(coordinates[0])
    farthest_distances.append(coordinates[0])
    for j in range(1, len(distance_list)):
        if(len(farthest_points) < n):
            farthest_distances.append(distance_list[j])
            farthest_points.append(coordinates[j])
            if(distance_list[j] < min_value):
                min_value = distance_list[j]
                min_index = len(farthest_points)-1
        else:
            if(distance_list[j] > min_value):
                farthest_points[min_index] = coordinates[j]
                farthest_distances[min_index] = distance_list[j]
                new_min = distance_list[j]
                new_index = min_index
                for k in range(0, len(farthest_distances)):
                    if(farthest_distances[k] < new_min):
                        new_min = farthest_distance[k]
                        min_index = k
                min_value = new_min
                min_index = new_index

    return farthest_points

'''
finds the coordinate that is closest to a given point
'''
def closest_point(a, coordinates):
    closest = 10000000000000
    closest_point = ""
    for(coord : coordinates):
        distance = vincenty(coord, a).km
        if((distance <= closest) and (coord != a)):
            closest = distance
            closest_point = coord
    return closest_point

'''
finds the total length of the path created by a list of coordinates
'''
def path_length(path):
    total_distance = 0;
    for i in range(1, len(path)):
        total_distance = total_distance + vincenty(path[i-1], path[i])
    return total_distance

'''
finds the coordinate that can be added to the path yet increases the distance of the 
path by the least distance possible - only adds the point if it doesn't create a path
that exceeds the time limit
'''
def min_cost_coordinates(path, coordinates, max_length):
    min_cost = 1000000000
    min_point = 0
    min_index
    b = 0
    
    for i in range(0, len(coordinates)):
        for j in range(1, len(path)):
            current_distance = vincenty(path[j-1], path[j]).km
            new_distance = vincenty(path[j-1], coordinates[i]).km + vincenty(coordinates[i], path[j]).km
            increased_distance = new_distance - current_distance
            if(increased_distance < min_cost and (coordinates[i] not in path)):
                min_cost = increased_distance
                min_point = coordinates[i]
                min_index = i
                b = j
    path.insert(b, min_point)
    new_length = path_length(path)
    if(new_length > max_length):
        del path[b]
        return []
    else:
        del coordinates[i]
    return path


'''
given a start and end point and one of the lth farthest points create a path
with as many points as possible without exceeding the time limit
'''
def create_path(start, end, far_point, max_length, coordinates):
    path = [start, far_point, end]
    add_to = min_cost_coordinates(path, coordinates, max_length)
    while(len(add_to) != 0):
        path = add_to
        add_to = min_cost_coordinates(path, coordinates, max_length)
    return path

'''
create L paths - one for each of the Lth farthest points
'''
def create_paths(start, end, farthest_points, max_length, coordinates):
    list_of_paths = []
    ordered_farthest_points = sorted(farthest_points, key= lambda point: distance_between(start, end, point), reverse = True)
    for l in range(0, len(farthest_points)):
        path = create_path(start, end, farthest_points[l], max_length, coordinates)
        list_of_paths.append(path)
    return list_of_paths

def distance_between(start, end, point):
    leg_one = vincenty(start, point).km
    leg_two = vincenty(point, end).km
    total_distance = leg_one + leg_two
    return total_distance

###### two point exchange
'''
NOT CORRECT YET (I THINK)
'''
def two_point_exchange(op, nop, max_length):
    for j in range(1, len(op)-1)
        for k in range(0, len(nop)):
            for i in range(1, len(nop[k])-1):
                op_length = path_length(op)
                proposed_op = op
                proposed_op[j] = nop[k][i]
                proposed_op_length = path_length(proposed_op)
                nop_length = path_length(nop[k])
                proposed_nop = nop[k]
                proposed_nop[i] = op[j]
                proposed_nop_length = path_length(proposed_nop)
                if(proposed_op_length < op_length)
                    if(proposed_nop_length<max_length):
                        op = proposed_op
                        nop[k] = proposed_nop
                    else:
                        op = proposed_op
                        nop.append() = [op[0], op[j], op[len(op)-1]]
                if(len(nop[k]) >= len(op) && nop_length<op_length):
                    op= nop[k]
                    nop[k] = proposed_op
    return op, nop
###One point Movement
#Probably wrong too
def one_point_movement(coordinates, op, nop, max_length):
    all_paths = nop.insert(0, op)
    for i in range(0, len(all_paths)):
        new_path = min_cost_coordinates(all_paths[i], coordinates, max_length)
        while(len(new_path) > 0):
            all_paths[i] = new_path
            new_path = min_cost_coordinates(all_paths[i], coordinates, max_length)
    return op, nop


#reinitialization

#find the k worst points in op then 

def reinitialization(op, nop, max_length, coordinates):
    k_value = int(min(10, .75*len(op)))
    best_op = op
    best_nop = nop
    for k in range(1, k_value):
        test_op = remove_point(k, op)
        test_nop = nop
        for i in range(0, 10):
            test_op, test_nop = two_point_exchange(test_op, test_nop, max_length)
            test_op, test_nop = one_point_movement(coordinates, test_op, test_nop, max_length)
        if(len(test_op) > len(best_op)):
            best_op = test_op
            best_nop = test_nop
    return best_op, best_nop

def remove_point(k, op):
    for i in range(0, k):
        highest_distance = 0
        index = -1
        for j in range(1, len(op)-1):
            direct_distance = vincencty(op[i-1], op[i+1]).km
            distance = vincencty(op[i-1], op[i]).km + vincencty(op[i], op[i+1]).km
            added_distance = distance-direct_distance
            if(added_distance > highest_distance):
                highest_distance = added_distance
                index = i
        del op[index]
    return op

def orienteering_heuristic(coordinates, max_length):
    #initialization
    farthest_points_list = farthest_points(coordinates[0], coordinates[len(coordinates)-1], coordinates, 10)
    paths = create_paths(coordinates[0], coordinates[len(coordinates)-1], farthest_points, max_length, coordinates)
    op_index = 0
    len_op = len(op_path)
    for i in range(1, len(paths)):
        if(len(paths[i]) > len_op):
            op_index = i
            len_op = len(paths[i])
    op_path = paths[op_index]
    del paths[op_index]

    #improvement round one
    op, nop = two_point_exchange(op_path, paths, max_length)
    op, nop = one_point_movement(coordinates, op, nop, max_length)
    op, nop = reinitialization(op, nop, max_length, coordinates)

    #improvement round two
    op, nop = two_point_exchange(op, nop, max_length)
    op, nop = one_point_movement(coordinates, op, nop, max_length)
    op, nop = reinitialization(op, nop, max_length, coordinates)

    return op
    
'''
New Orienteering problem heuristic
N= number of points in the region of interest
L = min(10, N) and is the number of paths we construct initially

Part1:
find the top L points with the farthest distance from the start and end points -> farthest points
the lth path contains the lth point
form a path through these three points and then insert points greedy onto the path
    points that are closer by
when adding a point violates the time limit
add all points within the region to a path
path with largest score = opt, all others are nop

Part 2:
two point exchange
take point i from path in nop and add it to op and point j from op onto a path in nop -
     do so in cheapest way, also keeping all paths feasible
     insert i and j onto their respective paths in a way that has minimal increase in distance
if j can't be feasibly added to a path create a new path in nop
if path in nop has higher score than op, then it becomes op
accept changes that increase score, and all changes that only decrease the score by some amount

Overwiew:
for j= the first to last point in op
    for i = the first to last point in the first to last path in nop
        if exchanging i and j is feasible and score incerases, then exhcnage, and go to A loop
        else: set the best exhcnage = the one with the highest score
    end B loop
    if the score of the best exhcange >= record-deviation then make the best exchange
end A loop

Part 3:
one-point movement
attempt to insert point i between points in the first edge of path p, then second and so on
make the move when it is still feasible and increases the score

Overview
for i = first to last point in the region (point i on path q)
    for j = the first to last point in the first to last path
    (p) in both op and nop (p!=q)
        if inserting i in front of j on path p is feasible and score incerases, then move it
        and go to A loop
        else: set the best movement = one with the highest score
    end B loop
    if score of the best movement >= record-deviation then make the best movement
end A loop

Part 4:
cleanup

Overview:
1. Initialize
    initialize
    record = score of initial solution
    p=10
    deviation p % x record
2. Improve
    for k=1,2...K
        for i= 1,2, ...I
            two point exchange
            one point exchange
            clean ip
            if no movemnt made above, end I loop
            If bettwe solution obtained, then
                record = score of new best
                deviation = p % x recod
        End I loop
        Reinitialization
    End K loop
3. set p=5 and redo step two again
'''

'''
The five-step heuristic of Chao et al. (1996b) only considers vertices
that can be reached. In a Euclidean space, these vertices lie
within an ellipse using start and end vertex as foci and Tmax as
length of the major axis. The initialisation step creates many different
paths, each starting with a vertex far away from start and end
vertex, and always assigns all other vertices to one of the paths
using cheapest insertion. The best path is selected as the initial
solution Top. The non-included vertices are also assigned to feasible
paths Tnop. The first improvement step, two-point exchange, tries
to improve Top by including an extra vertex from one of the Tnop
and moving an included vertex to one of the Tnop, also using cheapest
insertion. All paths have to remain feasible and a small decrease
of the total score is allowed. The second improvement step will
place one vertex from one path to another if feasible and if the total
score does not decrease too much. The third improvement step involves
2-Opt. Finally, a specified number of vertices with a low
score over insertion cost ratio are removed from the optimal path
and the algorithm restarts. The five-step heuristic of Chao et al.
clearly outperforms all above-mentioned heuristics
'''