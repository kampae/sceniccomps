source: http://stackoverflow.com/questions/4656802/midpoint-between-two-latitude-and-longitude

def find_center(start_point, end_point):

    Ax = start_point[0]
    Ay = start_point[1]
    Bx = end_point[0]
    By = end_point[1]
    
    distance = math.radians(By-Ay)
    
    //convert to radians
    lat1 = math.radians(Ax)
    lat2 = math.radians(Bx)
    lon1 = math.radians(Ay)
    lon2 = math.radians(By)

    x_distance = math.cos(lat2) * math.cos(distance)
    y_distance = math.cos(lat2) * math.sin(distance)
    c_lat = math.atan2(math.sin(lat1) + math.sin(lat2), math.sqrt((math.cos(lat2) + x_distance) * (math.cos(lat1) + x_distance) + y_distance*y_distance
    c_lng = lon1 + math.atan2(y_distance, math.cos(lat1) + x_distance)

    center_lat = math.degrees(c_lat)
    center_lng = math.degree(c_lng)
    center = (center_lat, center_lng)
    return center

def find_distance_between_pts(point1, point2):
    distance = vincencty(point1, point2).km
    return distance
