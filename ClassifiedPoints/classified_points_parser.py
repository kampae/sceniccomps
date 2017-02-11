def parse(filename):
    
    f = open(filename, 'r')
    
    classifications = {}
    
    classifications['water'] = 0
    classifications['nature and woods'] = 0
    classifications['mountain'] = 0
    classifications['fields'] = 0
    classifications['sightseeing'] = 0
    classifications['non-scenic'] = 0
    
    #counter = 0
    for line in f:
        line = line[2:len(line)-3]
        line = line.split('], [')
        line = line[1:]
        
        for c in line:
            c = c.split(',')
            scenery = c[0].strip("'")
            classifications[scenery] += 1
            
    f.close()
                    
    return classifications
        

counts = parse('all_classified_points.csv')

print("Mountain Points: ", counts["mountain"])
print("Water Points: ", counts["water"])
print("Nature and Woods Points: ", counts["nature and woods"])
print("Fields Points: ", counts["fields"])
print("Sightseeing Points: ", counts["sightseeing"])
print("Non-Scenic Points: ", counts["non-scenic"])