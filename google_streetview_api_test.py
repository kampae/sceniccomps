import sys
import json
from urllib.request import urlretrieve
import os

def get_carleton_streetview():
    apiKey = 'AIzaSyBJN20CtR9R9AdWsInx-sAF_CoLRkI66so'
    #gets google street view images with varying heading (horizontal view) and pitch (vertical view)
    for i in range(0,7):
        for j in range(0,7):
            heading = str(i*50)
            pitch = str(j*10)
            urlstring = 'https://maps.googleapis.com/maps/api/streetview?size=600x300&location=1+North+College+Street,+Northfield,+MN+55057&heading=' + heading + '&pitch=' + pitch + '&key=' + apiKey
            fileName = "CarletonImage" + heading + "," + pitch + ".jpg"
            urlretrieve(urlstring, fileName)
    
get_carleton_streetview()
