import numpy as np

GRADE_LATITUDE = 111000
GRADE_LONGITUDE = lambda lat: GRADE_LATITUDE * np.cos(lat)


def get_map_limits(latitude, longitude, radius):

    delta_lat = radius / GRADE_LATITUDE
    delta_long = radius / GRADE_LONGITUDE(latitude)

    northEast_lat = latitude + delta_lat
    northEast_long = longitude + delta_long
    southWest_lat = latitude - delta_lat
    southWest_long = longitude - delta_long

    return (('northEast', northEast_lat, northEast_long),
            ('southWest', southWest_lat, southWest_long))

