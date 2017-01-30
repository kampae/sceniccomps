import gsv_3images
import caffe_3images
import create_grid_coords
import os
import sys


def get_classifications(coords):
    file = open("ClassifiedPoints/classified_points74400.csv", "w")
    # set up caffe net 
    net, mu = caffe_3images.makeNet()
    transformer, net = caffe_3images.makeTransformer(net, mu)

    for latlng in coords:
        # gather 3 images for the lat lng coordinates 
        images = gsv_3images.get_streetview(latlng)
    
        # will store list of 3 classifications and their probabilities
        three_classifications = []
    
        # classify all 3 images 
        for image in images:
            # classification = [classification keyword, probability]
            #print("Image I am trying to classify: ", image)
            classification = caffe_3images.classify(net, image, transformer)
        
            three_classifications.append(classification)
        
        three_classifications = sorted(three_classifications, key=lambda classification: classification[1], reverse=True)
        
        three_classifications.insert(0, latlng)
        file.write("%s\n" % three_classifications)
        
        os.remove("Pic0.jpg")
        os.remove("Pic1.jpg")
        os.remove("Pic2.jpg")
    
    file.close()
        
if __name__ == "__main__":
    # sample coordinate list
    #coords = [["44.5101349, -93.14554699999997"]] 
    
#    arguments = sys.argv
#    inputFile = arguments[1]
#    outputFile = arguments[2]
    
    coords = []
    with open('RoadCoords/roadFile74400') as inputfile:
        for line in inputfile:
            coords.append([line.strip()])
    
    get_classifications(coords)
    
    #HAD ERROR WHEN TRYING TO RUN roadFile52800!! so not all its points were classified