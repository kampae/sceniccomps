import gsv_3images
import caffe_3images
import createGridCoords


def getClassifications(coords):
    

    # list to hold top classification for each point
    classifications = []

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
        
            three_classifications.append([classification, latlng])

        top_prob = 0
        top_class = ""
    
        # find top probability 
        for classification in three_classifications:
            if classification[0][1] > top_prob:
                top_class = classification[0][0]
    
        classifications.append([top_class, classification[1]]) 
    for classi in classifications:
        print(classi)
    return classifications 

if __name__ == "__main__":
    # sample coordinate list
    #coords = [[44.461193, -93.155638]]
    coords = createGridCoords.returnGridCoords()
    
    getClassifications(coords)