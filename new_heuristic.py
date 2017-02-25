import sys
import simplejson
#from urllib.request import urlopen
from urllib2 import urlopen
import os
from geopy.distance import vincenty
import pulp



'''
finds the top n points with the largest distance from points a and b
and returns a list of those coordinates
'''
def farthest_points(a, b, coordinates, n, max_time):
    ordered = sorted(coordinates, key = lambda coord: three_point_distance(a, b, coord, max_time), reverse = True)
    farthest_points = []
    for i in range(0, n):
        farthest_points.append(ordered[i])
    return farthest_points, ordered[n:len(ordered)]


def three_point_distance(start, end, point, max_time):
    leg_one = vincenty(start, point).km
    leg_two = vincenty(point, end).km
    total_distance = (1.5*leg_one +6.0842)+ (1.5*leg_two + 6.0842)
    start_to_end = vincenty(start, end).km
    point_to_end = vincenty(point,end).km
    if(total_distance > max_time or (point_to_end>start_to_end)):
        return 0
    else:
        return total_distance

'''
finds the coordinate that is closest to a given point
'''
def closest_point(a, coordinates):
    closest = 10000000000000
    closest_point = ""
    for coord in coordinates:
        distance = vincenty(coord, a).km
        if((distance <= closest) and (coord != a)):
            closest = distance
            closest_point = coord
    return closest_point

'''
finds the total length of the path created by a list of coordinates
Approximately converts km into time
'''
def path_length(path):
    total_distance = 0;
    for i in range(1, len(path)):
        total_distance = total_distance + ((1.4*vincenty(path[i-1], path[i]).km) + 6.0842)
    return total_distance

'''
finds the coordinate that can be added to the path yet increases the distance of the 
path by the least distance possible - only adds the point if it doesn't create a path
that exceeds the time limit
'''
def min_cost_coordinates(path, coordinates, max_length, end):
    min_cost = 1000000000
    min_point = 0
    min_index = 0
    b = 0
    for i in range(0, len(coordinates)):
        for j in range(1, len(path)):
            current_distance = vincenty(path[j-1], path[j]).km
            new_distance = vincenty(path[j-1], coordinates[i]).km + vincenty(coordinates[i], path[j]).km
            increased_distance = new_distance - current_distance
            distance_to_end = vincenty(path[j-1], end).km
            new_distance_to_end = vincenty(coordinates[i], end).km
            if(increased_distance < min_cost and (coordinates[i] not in path) and (new_distance_to_end<distance_to_end)):
                min_cost = increased_distance
                min_point = coordinates[i]
                min_index = i
                b = j
    path.insert(b, min_point)
    new_length = path_length(path)
    if(new_length > max_length):
        del path[b]
        return [], coordinates
    else:
        del coordinates[min_index]
        return path, coordinates

'''
if the coordinate can replace a coordinate in the path such that the path decreases in length,
then the functions returns the optimal place to put the coordinate
'''
def min_location(coordinate, path, end, max_time):
    path_time = path_length(path)
    excess_time = max_time - path_time
    distance_decrease = min(-int(excess_time/1.4), 0)
    min_place = -1
    for j in range(1, len(path)-1):
        current_distance = vincenty(path[j-1], path[j]).km
        new_distance = vincenty(path[j-1], coordinate).km + vincenty(coordinate, path[j]).km
        changed_distance = current_distance-new_distance
        distance_to_end = vincenty(path[j-1], end).km
        new_distance_to_end = vincenty(coordinate, end).km
        
        if(changed_distance > distance_decrease and (coordinate not in path) and (new_distance_to_end<distance_to_end)):
            distance_decrease = changed_distance
            min_place = j
    return min_place, distance_decrease


'''
given a start and end point and one of the lth farthest points create a path
with as many points as possible without exceeding the time limit
'''
def create_path(start, end, far_point, max_length, r_coordinates):
    path = [start, far_point, end]
    add_to, r_coordinates = min_cost_coordinates(path, r_coordinates, max_length, end)
    while(len(add_to) != 0):
        path = add_to
        add_to, r_coordinates = min_cost_coordinates(path, r_coordinates, max_length, end)
    return path, r_coordinates

'''
create L paths - one for each of the Lth farthest points
'''
def create_paths(start, end, farthest_points, max_length, r_coordinates):
    list_of_paths = []
    for l in range(0, len(farthest_points)):
        path, r_coordinates = create_path(start, end, farthest_points[l], max_length, r_coordinates)
        
        if(len(path)<1):
            path = [start, farthest_points[l], end]
        list_of_paths.append(path)
    return list_of_paths

'''
Calculates the distance of a path created by three points
'''
def distance_between(start, end, point):
    leg_one = vincenty(start, point).km
    leg_two = vincenty(point, end).km
    total_distance = leg_one + leg_two
    return total_distance


'''
Performs two point exchange
Points from op are moved to paths in nop and a point from a path in nop
is moved to op - this only occurs if making this movement decreases the
length of op
'''
def two_point_exchange(op, nop, max_time, end):
    new_op = list(op)
    for j in range(1, len(op)-1):
        for k in range(0, len(nop)):
            for i in range(1, len(nop[k])-1):
                op_index, op_improvement = min_location(nop[k][i], new_op, end, max_time)
                if(op_index != -1):
                    best_nop = -1
                    nop_index = 0
                    best_improvement = 0
                    for x in range(0, len(nop)):
                        nop_loc, nop_change = min_location(op[j], nop[x], end, max_time)
                        if(nop_loc != -1 and nop_change > best_improvement):
                            best_nop = x
                            nop_index = nop_loc
                            best_improvement = nop_change
                    if((op_improvement > 0) and (nop[k][i] not in new_op) and (op[j] not in nop[best_nop])):
                        moved_coordinate = op[j]
                        new_op.insert(op_index, nop[k][i])
                        changed_nop = nop[best_nop].insert(nop_index, moved_coordinate)
                        nop[best_nop] = changed_nop
    return new_op, nop



'''
Performs one point movement
Points from paths in nop are removed from that path and added to op
This only occurs if adding the point does not cause the path to exceed
the time limit
'''
def one_point_movement(op, nop, max_length, end):
    for k in range(0, len(nop)):
        size = len(nop[k])-1
        i=1
        while(i < len(nop[k])-1):
            op_index, op_improvement = min_location(nop[k][i], op, end, max_length)
            if(op_index != -1):
                op.insert(op_index, nop[k][i])
                changed_nop = list(nop[k])
                del changed_nop[i]
                size = size-1
                i = i-1
                nop[k] = changed_nop
            i = i+1
    return op, nop   
    


'''
Reinitialization
For values k {1...K} remove k points from op, then rerun two point exchange
and one point movement. If op improves then it is the new op.
'''
def reinitialization(op, nop, max_length, coordinates, end):
    k_value = int(min(10, .75*len(op)))
    best_op = list(op)
    best_nop = list(nop)
    for k in range(1, k_value):
        temp_op = list(op)
        test_op = remove_point(k, temp_op)
        test_nop = nop
        for i in range(0, 10):
            test_op, test_nop = two_point_exchange(test_op, test_nop, max_length, end)
            test_op, test_nop = one_point_movement(test_op, test_nop, max_length, end)
        if(len(test_op) > len(best_op)):
            best_op = list(test_op)
            best_nop = list(test_nop)
    return best_op, best_nop

'''
removing k points from op- remove the points that improve op the most 
(decrease the length of the path by the most)
'''
def remove_point(k, op):
    for i in range(0, k):
        highest_distance = 0
        index = -1

        for j in range(1, len(op)-1):
            direct_distance = vincenty(op[j-1], op[j+1]).km #distance without j
            distance = vincenty(op[j-1], op[j]).km + vincenty(op[j], op[j+1]).km #distance with j
            added_distance = distance-direct_distance

            if(added_distance > highest_distance):
                highest_distance = added_distance
                index = j
        if(index != -1):
            del op[index]
    return op

'''
Calls the different stages of the orienteering heuristic
Performs initialization of the routes, then finds the op path, then
repeatedly performs improvements to the route
'''
def orienteering_heuristic(start, end, coordinates, max_time):
    #initialization
    num_far_points = min(10, len(coordinates))
    farthest_points_list, r_coordinates= farthest_points(start, end, coordinates, num_far_points, max_time)
    paths = create_paths(start, end, farthest_points_list, max_time, r_coordinates)
    
    #find the op path (the one with the most points)
    op_index = 0
    op_path = paths[0]
    len_op = len(op_path)
    for i in range(1, len(paths)):
        if(len(paths[i]) > len_op):
            op_index = i
            len_op = len(paths[i])
    op_path = paths[op_index]
    del paths[op_index]

    #improvement round one
    op, nop = two_point_exchange(op_path, paths, max_time, end)
    op, nop = one_point_movement(op, nop, max_time, end)
    op, nop = reinitialization(op, nop, max_time, coordinates, end)
      
    ordered_op = order_route(end, op)

    return ordered_op

'''
Order the route by points that are farthest from the end point, to points
that are closest to the end point
'''
def order_route(end, coordinates):
    ordered = sorted(coordinates, key = lambda coord: distance_to_end(coord, end), reverse = True)
    
    return ordered

'''
calculate the distance between two points
'''
def distance_to_end(item, end):
    return vincenty(item, end).km

