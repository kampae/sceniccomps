import sys
import json
from urllib.request import urlretrieve
import os

def get_carleton_streetview():
    apiKey = 'AIzaSyBJN20CtR9R9AdWsInx-sAF_CoLRkI66so'
    urlstring = 'https://maps.googleapis.com/maps/api/streetview?size=600x300&location=1+North+College+Street,+Northfield,+MN+55057&heading=151.78&pitch=-0.76&key=' + apiKey
    saveLoc = "C:/Users/evierosenberg/Desktop"
    fileName = "CarletonImage.jpg"
    urlretrieve(urlstring, fileName)
    
get_carleton_streetview()
