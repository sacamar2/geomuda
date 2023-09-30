'''
This module is aim to exclude or add metrics in an already existing GeoJson or DataFrame.
Any method from here must not modify the data format of the input data.
'''

from pandas import DataFrame
import numpy as np

from geopandas import GeoDataFrame,sjoin
from shapely.geometry import Point as sh_Point

from general_functions.variables import def_geooutliers_perc, def_square_size
from geo_transformers.funcs_geolocation import build_accumulated_distance
from geo_transformers.funcs_geolocation import build_gdf_polygons

def build_aggregated_geodataframe(polygon_mask_geodataframe:GeoDataFrame) -> GeoDataFrame:
    aggregated_geodataframe=polygon_mask_geodataframe.drop(['polygon','Unnamed: 0'],axis=1)
    return aggregated_geodataframe