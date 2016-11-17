
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


def createGridCoords(coordsArray):
    try:
        f = open("js_coords.js", "w")
        f.write("var coords = [")

        # startPoint = coordsArray[0]
        # endPoint = coordsArray[1]
        bottomLeft = coordsArray[0]
        bottomRight = coordsArray[1]
        topRight = coordsArray[2]
        topLeft = coordsArray[3]
        gridArray = []
        # Do we want these? No necessarily going to be in there if increasing by .009 Lat & Long
        #  We might have duplicates-- issues? Checking for duplicates would take too much time I think
        #  WAIT: need these for the JavaScript function, in this order at the beginning
        gridArray.append(bottomLeft)
        gridArray.append(bottomRight)
        gridArray.append(topRight)
        gridArray.append(topLeft)

        # LAT lower bound
        if bottomLeft[0] <= topLeft[0]:
            lowerX = bottomLeft[0]
        else:
            lowerX = topLeft[0]

        # LAT upper bound
        if bottomRight[0] <= topRight[0]:
            upperX = topRight[0]
        else:
            upperX = bottomRight[0]

        # LONG lower bound
        if bottomLeft[1] <= bottomRight[1]:
            lowerY = bottomLeft[1]
        else: 
            lowerY = bottomRight[1]

        # LONG upper bound
        if topLeft[1] <= topRight[1]:
            upperY = topRight[1]
        else:
            upperY = topLeft[1]


        y = lowerY
        while y <= upperY:
            x = lowerX
            while x <= upperX:
                #call JavaScript function with [x,y]
                    #Check if x is in bounds
                    #Check if y is in bounds
                    #IF YES: then append
                gridArray.append([x,y])
                f.write("[" + str(x) + "," + str(y) + "]")
                x += 1 	#0.009 
                if (x <= upperX):
                    f.write(", ")
                # Increase latitude by 1 km
            #call JavaScript function with [x,y]
                #Check if x is in bounds
                #Check if y is in bounds
                #IF YES: then append
            gridArray.append([x,y])
            y += 1			#(1/(111.111 * math.cos(math.radians(x)) )) 	# Increase longitude by 1 km
        f.write("]")
        f.close()
        return gridArray #startLat, endLat, startLang, endLang, #lowerLimitX, upperLimitX, lowerLimitY, upperLimitY
        # Have gridArray: first 4 coords are our parameters!!!!
    except IOError as (errno,strerror):
        print "ERROR"

def find_nearest_road():
    print("hi")
    #code to find nearest rode
    
def returnGridCoords():
    coordsArray = find_relevant_area.return_corners()
    # [[41.850033, 87.6500523], [44, 87], [43.850033, 89.6500523], [41,89]]   #Connect to Phoebe's code here    
    answerArray = createGridCoords(coordsArray)
    return answerArray


