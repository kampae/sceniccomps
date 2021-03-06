import sys
#import simplejson
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
# Phoebe's API key 2: AIzaSyB1eAbxLePfsBKeszxFtc3g4wRNwnWwuzA
# Emily's API key: AIzaSyCS4cJEpYt-1u6xRkJmqsiBKV1LHnYB0Mg
# Allie API key 1: AIzaSyARnHNVEx6TYAc0m9eRxuH0sLPy_pzpAac
# Allie API key 2: AIzaSyAns9sLJaIPkyKwcDxWiOCwAgOVCmvn7yw
# Allie API key 3: AIzaSyBRamX0tFH2PitoYtFJQpzePC66a4Ijs4g
# Evie's API key: AIzaSyB6hGD2MtGOmQ8oo2dXta6SU8aZWL4-s24

def directions(coordinates, curr_key, write_file):
    output_list = []
    file = open(write_file, 'w')
    for n in coordinates:
        gmaps = googlemaps.Client(key=curr_key)
        routes = gmaps.directions(n, n, mode="driving")
        if(len(routes)>0):
            output_coords = [routes[0].get('legs')[0].get("start_location").get('lat'), routes[0].get('legs')[0].get("start_location").get('lng')]
            if output_coords not in output_list:
                output_list.append(output_coords)
                r = str(output_coords[0]) + ", " + str(output_coords[1])
                file.write("%s\n" % r)
                #r = str(output_coords[0]) + ", " + str(output_coords[1])
                #file.write("%s\n" % r)
    return output_list


if __name__ == '__main__':
    
    keys = ['AIzaSyB1eAbxLePfsBKeszxFtc3g4wRNwnWwuzA', 'AIzaSyCS4cJEpYt-1u6xRkJmqsiBKV1LHnYB0Mg', 'AIzaSyARnHNVEx6TYAc0m9eRxuH0sLPy_pzpAac', 'AIzaSyAns9sLJaIPkyKwcDxWiOCwAgOVCmvn7yw', 'AIzaSyBRamX0tFH2PitoYtFJQpzePC66a4Ijs4g']
    
    for i in range(0, len(keys)):
        file_num = 160800 + i*2400
        read_file = 'outputFileNum' + str(file_num)
        write_file = 'roadFile' + str(file_num)

        #read in file
        with open(read_file, 'r') as f:
             coord_list = f.read().splitlines()
        #test_list = ['48.715079, -120.308558422']
        coor_list = directions(coord_list, keys[i], write_file)
        #write to file
        f.close()
        
        print("Just completed writing to file", write_file)