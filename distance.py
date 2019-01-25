from math import sin, cos, sqrt, atan2, radians

def _coord_distance(c1, c2):
    """Calculate the distance between two latitude-longtide points.
    This solution is pasted from 'Michael0x2a' answer at 
    https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude"""

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

def _is_in_range(origin, location, max_distance):
    return _coord_distance(origin, location) <= max_distance

def filter_by_distance(users, origin, max_distance):
    """Filter out users and users' locations that are not within the max distance of origin"""
    filtered_users = []
    for user in users:
        nearby_locations = []
        for location in user.locations:
            if _is_in_range(origin, location.coords(), max_distance):
                nearby_locations.append(location)
        if len(nearby_locations):
            user.locations = nearby_locations
            filtered_users.append(user)
    return filtered_users


