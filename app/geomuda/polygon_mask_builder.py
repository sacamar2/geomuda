'''
This module is aim to exclude or add metrics in an already existing GeoJson or DataFrame.
Any method from here must not modify the data format of the input data.
'''
from typing import List
import logging

from pandas import DataFrame
from numpy import ceil

from geopandas import GeoDataFrame
from geopy.distance import distance
from shapely.geometry import Polygon as sh_Polygon

from general_functions.variables import def_square_size
from geocalculations import move_coord

def build_polygon_mask_grid(layer_data:DataFrame,
                            square_size:int=def_square_size) -> GeoDataFrame:
    """
    This method will create the needed polygons to cluster the points on them. On that way, we can calculate stats
    by each polygon and then homogenesise the data.

    Args:
        coords (list): It is a list of coordinates (lon, lat)

    Returns:
        GeoDataFrame: Table with a single column: geometry, filled by shapely Polygons
    """
    try:
        lan_lon_polygons=get_lan_lon_polygons(layer_data,square_size)
    except Exception as e:
        logging.error('It wasnt possible to build the polygon mask')
        exit(1)
    
    polygon_mask=GeoDataFrame({'geometry':[sh_Polygon(p_coords) for p_coords
                                           in lan_lon_polygons]},crs="EPSG:4326")
    return polygon_mask

def get_lan_lon_polygons(layer_data:DataFrame,
                         square_size:int=def_square_size,
                         geodistr:str='square') -> List[tuple]:
    '''layer_data_data must be a DataFrame with latitude and longitude with WSG84 projection 
        Each square is defined by its (0,0) and (1,1) points (min lat/lon & max lat/lon)'''
    
    lan_lon_polygons=[]
    
    # From the whole dataset, we get the most left and lowest point as well as the righest and highest
    min_lat,max_lat=min(layer_data['latitude']),max(layer_data['latitude'])
    min_lon,max_lon=min(layer_data['longitude']),max(layer_data['longitude'])
    

    # Given a certain size of each square, we get the needed amount of squares for latitude and longitude to get all clusterized.
    lan_num=int(ceil(distance((min_lat,min_lon),
                                 (max_lat,min_lon)).meters/square_size))
    lon_num=int(ceil(distance((min_lat,min_lon),
                                 (min_lat,max_lon)).meters/square_size))

    # We calculate the coordinates of each expected point
    aux_next_coord=(min_lat,min_lon) # it is lan,lon becaue geopy use that standard
    
    # Depending on how the polygon distribution is wanted, the calculation migh differ.
    if geodistr=='square':
        lan_range,lon_range=build_square_lan_lon_ranges(aux_next_coord,square_size)
    
    if geodistr=='rect':
        lan_range,lon_range=build_square_lan_lon_ranges(aux_next_coord,square_size)
    
    if geodistr=='circular':
        lan_range,lon_range=build_square_lan_lon_ranges(aux_next_coord,square_size)

    # We loop for each latitude and longitude intersection to build the square around.
    # If there is no point on the left/right up/down, then it will pass.
    for lan in range(len(lan_range)):
        for lon in range(len(lon_range)):
            try:
                '''
                lan_lon_polygons.append(((lan_range[lan],lon_range[lon]),
                                     (lan_range[lan],lon_range[lon+1]),
                                     (lan_range[lan+1],lon_range[lon+1]),
                                     (lan_range[lan+1],lon_range[lon]))) 
                '''
                # it is lon lan because geojson use that standard
                lan_lon_polygons.append(((lon_range[lon],lan_range[lan]),
                                     (lon_range[lon+1],lan_range[lan]),
                                     (lon_range[lon+1],lan_range[lan+1]),
                                     (lon_range[lon],lan_range[lan+1]))) 
            except:
                continue
    
    return lan_lon_polygons


def build_square_lan_lon_ranges(aux_next_coord,square_size,
                                lan_num,lon_num) -> (tuple, tuple):
    lan_range=[]
    lon_range=[]

    for _ in range(lan_num):
        aux_next_coord=move_coord(direction='north',step_size=square_size,
                                  aux_coord=aux_next_coord)
        lan_range.append(aux_next_coord[0])
    
    for _ in range(lon_num):
        aux_next_coord=move_coord(direction='east',step_size=square_size,
                                  aux_coord=aux_next_coord)
        lon_range.append(aux_next_coord[1])
    
    return lan_range, lon_range

