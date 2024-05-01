import googlemaps
import os
from math import radians, cos, sin, asin, sqrt, pi

MAP_KEY = os.getenv('GMAPS_APIKEY')

gmaps_api = googlemaps.Client(key=MAP_KEY)


def get_current_location():
    """Retrieve latitude and longitude coordinates for the current device using Google Maps Geolocation API.

    Returns:
        tuple: A tuple of two float values representing the latitude and longitude.
    """
    lat, long = gmaps_api.geolocate().get('location').values()

    return lat, long


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


def calculate_boundaries(loc: tuple[float, float], radius: int):
    """Calculate the boundary lines for a square around a coordinate using a specified radius.

    Args:
        loc: A tuple of a latitude and longitude coordinate.
        radius: The distance from the center of the square to the closest point on a side.

    Returns:
        A dictionary mapping each side of the square to its latitude and longitude values.
        Sides are labeled according to the cardinal direction they are in.
        N represents the top boundary of the square, S is the bottom boundary, etc..
    """
    lat, long = loc

    long_dist = radius / cos(radians(lat))

    lat_offset = (radius / 3956) * (180 / pi)
    long_offset = (long_dist / 3956) * (180 / pi)

    north_lat = lat + lat_offset
    south_lat = lat - lat_offset
    east_long = long + long_offset
    west_long = long - long_offset

    return {
        'S': south_lat,
        'N': north_lat,
        'W': west_long,
        'E': east_long
    }
