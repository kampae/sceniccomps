import sys
import json
from urllib.request import urlretrieve
import os
from PIL import Image

def get_carleton_streetview():
    apiKey = 'AIzaSyBJN20CtR9R9AdWsInx-sAF_CoLRkI66so'
    #gets google street view images with varying heading (horizontal view) and pitch (vertical view)
    urlstring = 'https://maps.googleapis.com/maps/api/streetview?size=600x300&location=1+North+College+Street,+Northfield,+MN+55057&heading=' + '0' '&pitch=' + '0' + '&key=' + apiKey
    fileName = "CarletonImage.jpg"
    image = urlretrieve(urlstring, fileName)  
    return image

get_carleton_streetview()