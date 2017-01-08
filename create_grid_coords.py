
# A function that takes in an array of two coordinates, our start and end coordinates 
#  for our route. It creates a square based off our coordinates, increasing latitude values 
#  by 0.009 degree increments, and increasing longitudes by increments of (1/111.111*cos(lat)). 
#  These increments represent an increase of a km.
#		1 degree latitude = 111.111 km
#		1 degree longitude = 111.111 * cos(latitude) km
#
# By Emily Kampa
# Written Nov 8, 2016

import find_relevant_area
import math
from math import *  
import json
import io

# @app.route('/_array2python')
# def array2python():
# 	coordinateList = json.loads(request.args.get(getClosestRoad(coordinateList)))
# 	# JS file does function aka finds closest roads
# 	return jsonify(result=coordinateList)

# IDEA: PyExcJS 1.4.0: Python Package Index

arr = [[46.213079, -124.872909],[46.225226, -117.129058],[48.954045, -117.098910],[49.026333, -124.886684]]

def create_grid_coords(coordsArray):
    try:
        f = open("js_coords.csv", "w")

        # startPoint = coordsArray[0]
        # endPoint = coordsArray[1]
        bottom_left = coordsArray[0]
        bottom_right = coordsArray[1]
        top_right = coordsArray[2]
        top_left = coordsArray[3]
        grid_array = []
        # Do we want these? No necessarily going to be in there if increasing by .009 Lat & Long
        #  We might have duplicates-- issues? Checking for duplicates would take too much time I think
        #  WAIT: need these for the JavaScript function, in this order at the beginning
        grid_array.append(bottom_left)
        grid_array.append(bottom_right)
        grid_array.append(top_right)
        grid_array.append(top_left)

        # LAT lower bound
        if bottom_left[0] <= top_left[0]:
            lowerX = bottom_left[0]
        else:
            lowerX = top_left[0]

        # LAT upper bound
        if bottom_right[0] <= top_right[0]:
            upperX = top_right[0]
        else:
            upperX = bottom_right[0]

        # LONG lower bound
        if bottom_left[1] <= bottom_right[1]:
            lowerY = bottom_left[1]
        else: 
            lowerY = bottom_right[1]

        # LONG upper bound
        if top_left[1] <= top_right[1]:
            upperY = top_right[1]
        else:
            upperY = top_left[1]


        y = lowerY
        while y <= upperY:
            x = lowerX
            while x <= upperX:
                #call JavaScript function with [x,y]
                    #Check if x is in bounds
                    #Check if y is in bounds
                    #IF YES: then append
                grid_array.append([x,y])
                f.write("[" + str(x) + "," + str(y) + "]\n")
                x += 0.009 
                # Increase latitude by 1 km
            #call JavaScript function with [x,y]
                #Check if x is in bounds
                #Check if y is in bounds
                #IF YES: then append
            grid_array.append([x,y])
            y += (1/(111.111 * math.cos(math.radians(x)) )) 	# Increase longitude by 1 km
        f.close()
        return grid_array #startLat, endLat, startLang, endLang, #lowerLimitX, upperLimitX, lowerLimitY, upperLimitY
        # Have grid_array: first 4 coords are our parameters!!!!
    except IOError as (errno,strerror):
        print "ERROR"

def find_nearest_road():
    print("hi")
    #code to find nearest rode
    
def return_grid_coords():
    coords_array = find_relevant_area.return_corners()
    # [[41.850033, 87.6500523], [44, 87], [43.850033, 89.6500523], [41,89]]   #Connect to Phoebe's code here    
    answer_array = create_grid_coords(coords_array)
    return answer_array


create_grid_coords(arr)

#    
#    bottom_left = 46.213079, -124.872909
#        bottom_right = 46.225226, -117.129058
#        top_right = 48.954045, -117.098910
#        top_left = 49.026333, -124.886684
#        [[46.213079, -124.872909],[46.225226, -117.129058],[48.954045, -117.098910],[49.026333, -124.886684]]


