import sys
import json
import urllib
#from urllib.request import urlretrieve
import os
from PIL import Image

def get_streetview(coords):
    apiKey = 'AIzaSyBJN20CtR9R9AdWsInx-sAF_CoLRkI66so'

    all_images = []
    
    for i in range(0, 3):
        lat = str(coords[0])
        #print("LAT: " + lat)
        lng = str(coords[1])
        #print("LNG: " + lng)
        heading = str(120 * i)
    
        urlstring = 'https://maps.googleapis.com/maps/api/streetview?size=600x300&location=' + lat + ',' + lng + '&fov=120&heading=' + heading + '&key=' + apiKey   
        fileName = "Pic" + str(i) + ".jpg"
        image = urllib.urlretrieve(urlstring, fileName)
        #print("FileName: " + fileName)
        all_images.append(fileName)
        
    return all_images