import sys
import json
from urllib.request import urlretrieve
import os
from PIL import Image

def get_carleton_streetview():
    apiKey = 'AIzaSyBJN20CtR9R9AdWsInx-sAF_CoLRkI66so'
    #gets google street view images with varying heading (horizontal view) and pitch (vertical view)
    all_images = []
#    for j in range(0,2):
#        for i in range(0,5):
#            heading = str(i*10)
#            pitch = str(j*10)
#            urlstring = 'https://maps.googleapis.com/maps/api/streetview?size=600x300&location=1+North+College+Street,+Northfield,+MN+55057&heading=' + heading + '&pitch=' + pitch + '&key=' + apiKey
#            fileName = "CarletonImage" + heading + "," + pitch + ".jpg"
#            image = urlretrieve(urlstring, fileName)
#            all_images.append(image)
#    for i in range(0, 3):
#        heading = str(i * 120)
#        urlstring = 'https://maps.googleapis.com/maps/api/streetview?size=600x300&location=1+North+College+Street,+Northfield,+MN+55057&fov=120&heading=' + heading + '&key=' + apiKey   
#        fileName = "CarletonImage" + heading + ".jpg"
#        image = urlretrieve(urlstring, fileName)
#        all_images.append(image)    
        
    for i in range(0, 3):
        heading = str(i * 120)
        urlstring = 'https://maps.googleapis.com/maps/api/streetview?size=600x300&location=40.811306, -73.966917&fov=120&heading=' + heading + '&key=' + apiKey   
        fileName = "HHPkwy" + heading + ".jpg"
        image = urlretrieve(urlstring, fileName)
        all_images.append(image)

    return all_images

## http://stackoverflow.com/questions/30227466/combine-several-images-horizontally-with-python

def stitch_images(all_images):
    images = []
    for x in all_images:
        images.append(Image.open(x[0]))
#    images = map(Image.open, ['CarletonImage0,0.jpg', 'CarletonImage0,10.jpg'])
#    print(images)
#    widths, heights = zip(*(i.size for i in images))
    
    widths = []
    heights = []
    
    for i in images:
        widths.append(i.size[0])
        heights.append(i.size[1])

    total_width = int(sum(widths)/20) + max(widths)
    max_height = max(heights)   
    
    new_image = Image.new('RGB', (total_width, max_height))
    
    x_offset = 0 
    y_offset = 0
    
    for j in range(0, 2):
        x_offset=0
        for k in range(0, 5):
            cur = k+(5*j)
            new_image.paste(images[cur], (x_offset, y_offset))
            x_offset += int(images[cur].size[0]/10)
        y_offset+=10
        
    
#    for image in images:
#        print("loop")
#        new_image.paste(image, (x_offset,0))
#        x_offset += int(image.size[0]/10)
        
    new_image.save('StitchTest.jpg')
    
get_carleton_streetview()

#stitch_images(get_carleton_streetview())
