import numpy as np
import matplotlib.pyplot as plt
import csv

#%matplotlib inline
plt.rcParams['figure.figsize'] = (10,10)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'            
              
import sys
caffe_root = '../'
sys.path.insert(0, caffe_root + 'python')

import caffe

import os


def makeNet():
    if os.path.isfile(caffe_root + 'models/placesCNN_upgraded/places205CNN_iter_300000_upgraded.caffemodel'):
        print 'CaffeNet found.'

    caffe.set_device(0)     # if we have multiple GPUs, pick the first one     
    caffe.set_mode_gpu()    # could also be cpu()

    model_def = caffe_root + 'models/placesCNN_upgraded/places205CNN_deploy_upgraded.prototxt'
    model_weights = caffe_root + 'models/placesCNN_upgraded/places205CNN_iter_300000_upgraded.caffemodel'

    net = caffe.Net(model_def,      # defines the structure of the model
                    model_weights,  # contains the trained weights
                    caffe.TEST)     # use test mode (e.g., don't perform dropout)

    # load the mean ImageNet image (as distributed with Caffe) for subtraction
    mu = np.load(caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy')
    mu = mu.mean(1).mean(1)  # average over pixels to obtain the mean (BGR) pixel values

    return net, mu;

def makeTransformer(net, mu):
    # create transformer for the input called 'data'
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})

    transformer.set_transpose('data', (2,0,1))  # move image channels to outermost dimension
    transformer.set_mean('data', mu)            # subtract the dataset-mean value in each channl
    transformer.set_raw_scale('data', 255)      # rescale from [0, 1] to [0, 255]
    transformer.set_channel_swap('data', (2,1,0))  # swap channels from RGB to BGR

    # set the size of the input (we can skip this if we're happy
    #  with the default; we can also change it later, e.g., for different batch sizes)
    net.blobs['data'].reshape(10,        # batch size
                              3,         # 3-channel (BGR) images
                              227, 227)  # image size is 227x227
    
    return transformer, net
    
#classification = []    
def classify(net, image, transformer):
    mydict = {}
    with open('categories.csv', mode='r') as infile:
        reader = csv.reader(infile)
        for rows in reader:
            mydict[rows[0]] = rows[1]
            
    image = caffe.io.load_image(caffe_root + 'sceniccomps/' + image) #Specify image, can be url (with more code) or image from folder
    transformed_image = transformer.preprocess('data', image)
    plt.show(image)

    # copy the image data into the memory allocated for the net
    net.blobs['data'].data[...] = transformed_image

    ### perform classification
    output = net.forward()
    
    # will store classification and probability. this is what the function will return 
    classification = []
    
    output_prob = output['prob'][0]  # the output probability vector for the first image in the batch
    
    # load ImageNet labels
    labels_file = caffe_root + 'models/placesCNN_upgraded/categoryIndex_places205.csv'

    labels = np.loadtxt(labels_file, str, delimiter='\t')
    
    classification.append(mydict[labels[output_prob.argmax()]])
    
    classification.append(output_prob[0])
    
    return classification

if __name__ == "__main__":

    image = caffe.io.load_image(caffe_root + 'sceniccomps/CarletonImage.jpg') #'examples/stitchtest.jpg')
    net, mu = makeNet()
    transformer, net = makeTransformer(net, mu)
    classify(net, image, transformer)