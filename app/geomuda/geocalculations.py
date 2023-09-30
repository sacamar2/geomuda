''' This module is responsible for any complex calculation related to coordinates:
    - Multiple distances
    - Moving from one coordinate to another by given jumps
    - Matching point to Polygon area
    - ...

'''
from geopy.distance import distance
from general_functions.variables import movement_mapping, def_square_size

def build_accumulated_distance(coords:list):
    accumulated_distance=[]
    for coord in coords:
        aux_accumulated_distance=sum([distance(coord,c).meters for c in coords])
        accumulated_distance.append(aux_accumulated_distance)
    return accumulated_distance

def move_coord(aux_coord,direction,step_size=def_square_size) -> tuple:
    raw_next_coord=distance(
                        meters=step_size
                        ).destination(aux_coord,bearing=
                                      movement_mapping[direction])
    
    next_coord=(raw_next_coord.latitude,raw_next_coord.longitude)
    return next_coord

