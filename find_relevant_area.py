import math
from geopy.distance import vincenty
import simplejson
from urllib2 import urlopen


'''
Main function: take start and end points and max time willing to travel as input
               returns the coordinates of the four corners of the bounding square
'''
def find_relevant_area(points, max_time):
    max_time = (max_time/60)/60;
    # Initializes values needed for the start/end points
    start_point = points[0]
    end_point = points[1]
        
    Ax = start_point[0]
    Ay = start_point[1]
    Bx = end_point[0]
    By = end_point[1]
    
    # Initializes the center point between two points on the same line
    center = find_center(start_point, end_point)
    Cx = center[0]
    Cy = center[1]

    # Converts max time to max distance using the assumption time is communicated in mins and
        # you will not be traveling greater than 55mph on average
    max_dist = 55/60 * max_time
    
    # Finds the distance between the start and end points
    dist_between_points = find_dist_between_pts(start_point, end_point)
    
    # Finds the slope of the line between the start and end points, and the slope perpendicular to that
    if (By - Ay) == 0:
        slope = 0
    else:
        slope = (Bx - Ax) / (By - Ay)
        
    if slope == 0:
        perp_slope = 1
    else:
        perp_slope = 1/slope
    
    # Finds the distance from the start/end points to the corners nearest them of the eventual square bounds
    # Finds the distance from the center point to the corners of the eventual square bounds
    dist_to_edge = (max_dist - dist_between_points)/2
    c_dist_to_edge = max_dist/2
    
    # Finds the the amount we need to move in the x and y directions to get our corner points, based on
        # the start and end points, and the center point
    perp_diffs = find_new_point(perp_slope, c_dist_to_edge)
    diffs = find_new_point(slope, dist_to_edge)
    
    perp_hdiff = perp_diffs[0]
    perp_vdiff = perp_diffs[1]
    
    hdiff = diffs[0]
    vdiff = diffs[1]
    
    # Series of conditionals to make sure we add and subtract the differences at the right times
        # to get our corners
    if Ax < Bx and Ay < By:
        bottom_left = (Ax - hdiff, Ay - vdiff)
        top_right = (Bx + hdiff, By + vdiff)
        bottom_right = (Cx + perp_hdiff, Cy - perp_vdiff)
        top_left = (Cx - perp_hdiff, Cy + perp_vdiff)
        
    elif Ax < Bx and Ay > By:
        bottom_left = (Cx - perp_hdiff, Cy - perp_vdiff)
        top_right = (Cx + perp_hdiff, Cy + perp_vdiff)
        bottom_right = (Bx + hdiff, By - vdiff)
        top_left = (Ax - hdiff, By + vdiff)    
        
    elif Ax > Bx and Ay < By:
        bottom_left = (Cx - perp_hdiff, Cy - perp_vdiff)
        top_right = (Cx + perp_hdiff, Cy + perp_vdiff)
        bottom_right = (Ax + hdiff, Ay - vdiff)
        top_left = (Bx - hdiff, By + vdiff)
        
    else:
        bottom_left = (Bx - hdiff, By - vdiff)
        top_right = (Ax + hdiff, Ay + vdiff)
        bottom_right = (Cx + perp_hdiff, Cy - perp_vdiff)
        top_left = (Cx - perp_hdiff, Cy + perp_vdiff)
        
    corners = [bottom_left, bottom_right, top_right, top_left]
    
    return corners
    
'''
Given two points, finds the point on the same line, equidistant from the two given points
'''
def find_center(point1, point2):
    
    Cx = (point1[0] + point2[0])/2
    Cy = (point1[1] + point2[1])/2
    
    center = (Cx, Cy)
    return center

'''
Given two points, implements the distance formula to determine the distance between them
'''
def find_dist_between_pts(point1, point2):
    dist_between_points = math.sqrt(((point1[0]-point2[0])**2) + ((point1[1]-point2[1])**2))
    
    #dist_between_points = vincenty(point1, point2).miles
    
    return dist_between_points

'''
Given a line's slope, finds the point on that line that is h distance away
'''
def find_new_point(slope, h):
    theta = math.atan(slope)
    hdiff = h * math.sin(theta)
    vdiff = h * math.cos(theta)
    
    diffs = (hdiff, vdiff)
    
    return diffs

def return_corners():
    corners = find_relevant_area([(44.706885, -93.713955), (44.849651, -92.714665)], 120)
    print(corners)
    
    
    
    
    
    
    
    
    
    
    
    