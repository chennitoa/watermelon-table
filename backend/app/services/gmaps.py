import googlemaps
import os
from math import radians, cos, sin, asin, sqrt


MAP_KEY = os.getenv('GMAPS_APIKEY')
gmaps_api = googlemaps.Client(key=MAP_KEY)


def distance(loc1: tuple[float, float], loc2: tuple[float, float]):
    """Calculate the distance between two coordinates using the Haversine formula.

    Args:
        loc1: A tuple of a latitude and longitude coordinate.
        loc2: A tuple of a latitude and longitude coordinate.

    Returns:
        A float representing the distance between the two coordinates in miles.
    """
    lat1, long1 = loc1
    lat2, long2 = loc2

    lat1, long1 = radians(lat1), radians(long1)
    lat2, long2 = radians(lat2), radians(long2)

    # Haversine formula from https://www.geeksforgeeks.org/program-distance-two-points-earth/
    dlong = long2 - long1
    dlat = lat2 - lat1
    a = sin(dlat/2) * sin(dlat/2) + cos(lat1) * cos(lat2) * sin(dlong/2) * sin(dlong/2)

    c = 2 * asin(sqrt(a))

    # Radius of Earth is 3956 miles
    # Return the distance in miles
    return c * 3956
