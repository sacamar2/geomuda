'''This module is aim to change the data format from dataframe to geojson and to
geodataframe for the multiple purposes:

- Extract data (DataFrame)
- Manipulate it geolocally and export it (GeoJson)
- Plot it (GeoDataFrame)

'''

from geopandas import GeoDataFrame
from general_functions.variables import (def_rent_distr_name, def_geooutliers_perc,def_output_geojsons)
from geojson import FeatureCollection, dump
from shapely.geometry.point import Point as sh_Point
from pandas import DataFrame, concat
import numpy as np
import geojson 

from geo_transformers.funcs_geolocation import build_accumulated_distance


def build_standard_geodataframe(raw_data:DataFrame):
    # Lon lan is selected as it is the geojson standard and when the polygons are created and they are used on geojons
    # it is easier to flip the points for the distance as geopy use lat lon standard.
    raw_data['geometry']=[sh_Point((r['longitude'],r['latitude'])) for _,r in raw_data.iterrows()]
    standard_geodataframe=GeoDataFrame(raw_data,crs="EPSG:4326")
    return standard_geodataframe

def build_standard_geojson(gdf:GeoDataFrame):
    rent_geojson=geojson.loads(gdf.to_json())
    return rent_geojson

def do_write_geojson(layer_name:str, gj:FeatureCollection, gj_name:str=def_rent_distr_name):
    if not gj_name.endswith(".geojson"):
        gj_name+=".geojson"

    with open(f"{def_output_geojsons}/{layer_name}_layer/{gj_name}", 'w') as f:
        dump(gj, f)
