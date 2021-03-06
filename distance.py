from math import sin, cos, sqrt, atan2, radians

def coord_distance(c1, c2):
    """Calculate the distance between two latitude-longtide points.
    This solution is pasted from 'Michael0x2a' answer at 
    https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
    
    This function should be handled when querying the database.
    """

    # approximate radius of earth in miles
    RAD = 3959.0
    lat1 = radians(c1[0])
    lon1 = radians(c1[1])
    lat2 = radians(c2[0])
    lon2 = radians(c2[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = RAD * c

    return distance