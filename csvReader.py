import csv
mydict = {}
with open('places205.csv', mode='r') as infile:
    reader = csv.reader(infile)
    with open('coors_new.csv', mode='w') as outfile:
        writer = csv.writer(outfile)
        for rows in reader:
        	mydict[rows[0]] = rows[1]
        	
print(mydict['/a/airport_terminal\''])