'''This module is responsible of clean the data:
        - Exclude outliers
        - Drop nulls
        - ...
'''
from geopandas import GeoDataFrame
from pandas import DataFrame
from sys import exit
from exporter import check_source_data_format
from general_functions.variables import def_geooutliers_perc
from geocalculations import build_accumulated_distance
import logging
import numpy as np

def clean_source_data(source_data: DataFrame) -> DataFrame:
    """
    source_clean This method is used to created a clean DataFrame used
    on the geo transformations and calculations afterwards

    Args:
        source_data (DataFrame): It is the data from the csv file.
    """
    
    try:
        clean_data=remove_geooutliers(
            source_data.dropna().drop_duplicates(
            subset=['latitude','longitude'],inplace=True))
        return clean_data
    
    except Exception as e:
        logging.error(f'It wasnt possible to clean the source data because of {e}')
        exit(1)
    
def clean_geolayer(data:GeoDataFrame,polygon_mask_data:GeoDataFrame)-> GeoDataFrame:
    # Aggregate all the points for each Polygon
    geolayer_data=data.groupby(by=['index_right'],as_index=False).mean().drop(['latitude','longitude'],axis=1)

    # Add the polygon objects
    geolayer_data['polygon']=polygon_mask_data.loc[geolayer_data['index_right']].values

    # This centroid calculation could be wrong because we are not projection the shapely polygon 
    # and we are using centroid method from shapely instead from geodataframe or so.
    geolayer_data['polygon_centroids']=[p.centroid for p in geolayer_data['polygon'].values]
    geolayer_data.drop(['index_right'],axis=1,inplace=True)
    
    return geolayer_data

def remove_geooutliers(source_data:DataFrame,perc:float=def_geooutliers_perc):
    """
    This method is used to delete the points which are too far from the rest.
    It is done because sometimes the searcher of location, Nomatim, miss the point big time.

    Args:
        input_data (DataFrame): This DataFrame must have latitude and longitude as columns and those columns must be floats.

        perc (float, optional): It is the percentile applied to exclude the outliers using the distance to the other points.
                                Defaults to def_geooutliers_perc.
    Returns:
        DataFrame: remove_geooutliers is the same DataFrame which came as input without the points which are further
                   from the rest of them.
    """
    coords=list(zip(source_data['latitude'],source_data['longitude']))
    accumulated_distance=build_accumulated_distance(coords)

    aux_percentile=np.percentile(accumulated_distance,perc)
    
    remove_geooutliers=source_data[accumulated_distance<=aux_percentile]
    return remove_geooutliers

