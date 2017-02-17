import gsv_3images
import caffe_3images
import create_grid_coords
import os
import sys

'''
Function that takes in a list of road coordinates. Uses gsv_3images.py to gather streetview images 
at each coordinate and caffe_3images.py to classify the scenery in each image. Stores top three 
classifications for each coordinate in a classified_points csv file.
'''
def get_classifications(coords):
    file = open("ClassifiedPoints/classified_points170400.csv", "w")
    net, mu = caffe_3images.make_net()
    transformer, net = caffe_3images.make_transformer(net, mu)

    for latlng in coords:
        images = gsv_3images.get_streetview(latlng)
    
        three_classifications = []
    
        for image in images:
            classification = caffe_3images.classify(net, image, transformer)
        
            three_classifications.append(classification)
        
        three_classifications = sorted(three_classifications, key=lambda classification: classification[1], reverse=True)
        
        three_classifications.insert(0, latlng)
        file.write("%s\n" % three_classifications)
        
        os.remove("Pic0.jpg")
        os.remove("Pic1.jpg")
        os.remove("Pic2.jpg")
    
    file.close()

'''
In main, open a file of road coordinates and pass them to get_classifications.
'''
if __name__ == "__main__":
    
    coords = []
    with open('RoadCoords/roadFile170400') as inputfile:
        for line in inputfile:
            coords.append([line.strip()])
    
    get_classifications(coords)
    