import sys
import simplejson
from urllib.request import urlopen
import os
import googlemaps
#you need to do pip install -U googlemaps to get the python google maps client 
#you should also replace my api key with one of your own
    #follow the directions on here cause you have to set it up https://github.com/googlemaps/google-maps-services-python
#then you can just put in a file to read from and a file name to write to and it will
#convert the original coordinates to nearby road coordinates
#this is suing python3
# Phoebe's API key: AIzaSyBEQ0xXnvLUr_tA3qSvk62XKjsLtpZKLyw
# Emily's API key: AIzaSyCS4cJEpYt-1u6xRkJmqsiBKV1LHnYB0Mg

def directions(coordinates):
    output_list = []
    for n in coordinates:
        gmaps = googlemaps.Client(key='AIzaSyARnHNVEx6TYAc0m9eRxuH0sLPy_pzpAac')
        #account 1 api key AIzaSyAns9sLJaIPkyKwcDxWiOCwAgOVCmvn7yw 
        routes = gmaps.directions(n, n, mode="driving")
        if(len(routes)>0):
            output_coords = [routes[0].get('legs')[0].get("start_location").get('lat'), routes[0].get('legs')[0].get("start_location").get('lng')]
            if output_coords not in output_list:
                output_list.append(output_coords)
    return output_list


if __name__ == '__main__':
    #read in file
    with open('test.csv', 'r') as f:
         coord_list = f.read().splitlines()
         print(coord_list)
    coor_list = directions(coord_list)
    #write to file
    file = open('output2', 'w')
    for item in coor_list:
        file.write("%s\n" % item[0] + ", " + item[1])
    f.close() 

    # print(directions(["48.850079, -124.667307623"]))

