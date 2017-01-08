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

def reverse_geo(coordinates):
    output_list = []
    for n in coordinates:
        gmaps = googlemaps.Client(key='AIzaSyAns9sLJaIPkyKwcDxWiOCwAgOVCmvn7yw')
        reverse_geocode_result = gmaps.reverse_geocode(n)
        if(len(reverse_geocode_result)>0):
            output_list.append([reverse_geocode_result[0].get('geometry').get('location').get("lat"), reverse_geocode_result[0].get('geometry').get('location').get("lng")])
    return output_list

if __name__ == '__main__':
    #read in file
    with open('daypart1.csv', 'r') as f:
         coord_list = f.read().splitlines()
    coor_list = reverse_geo(coord_list)
    #write to file
    file = open('output_part1', 'w')
    for item in coor_list:
        file.write("%s\n" % item)
    f.close() 
