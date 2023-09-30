'''
This module produce new geological data:
- Map coordinates to adress strings.
- Distance from point to point.
- Build square polygons.
- Check if a point is inside a polygon.
'''
from dataclasses import dataclass
from geopandas import GeoDataFrame
from pandas import DataFrame
from general_functions.variables import def_square_size, movement_mapping, max_retries
from shapely.geometry.polygon import Polygon as sh_Polygon
import numpy as np
from geopy.distance import distance
from geo_transformers.funcs_geotransformation import build_polygon_mask_geodataframe
from geocalculations import move_coord
from polygon_mask_builder import build_polygon_mask_grid
import logging

@dataclass
class PolygonMask:
    source_data: DataFrame
    grid: GeoDataFrame = None

    def __post_init__(self):
        if self.grid is None:
            try:
                self.grid=build_polygon_mask_grid()
            except Exception as e:
                logging.error(f'It wasnt possible to read the data from {self.fpath}')
                exit(1)

