import csv
mydict = {}
with open('../models/placesCNN_upgraded/categoryIndex_places205.csv', mode='r') as infile:
    reader = csv.reader(infile)
    for rows in reader:
        mydict[rows[0]] = rows[1]
        	
print(mydict['/a/abbey 0'])