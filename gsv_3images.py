import sys
import json
import urllib
#from urllib.request import urlretrieve
import os
from PIL import Image

'''
Takes in a coordinate point and retrieves 3 120 degree google streetview images from that point.
'''
def get_streetview(coords):
    api_key = 'AIzaSyBJN20CtR9R9AdWsInx-sAF_CoLRkI66so' #'AIzaSyD5kbefDW2RHY30LGQv2sP6tjfY8Dj0aqs' 
    all_images = []
    
    for i in range(0, 3):
        heading = str(120 * i)
        urlstring = 'https://maps.googleapis.com/maps/api/streetview?size=600x300&location=' + coords[0].replace(" ", "") + '&fov=120&heading=' + heading + '&key=' + api_key   
        file_name = "Pic" + str(i) + ".jpg"
        image = urllib.urlretrieve(urlstring, file_name)
        all_images.append(file_name)
        
    return all_images