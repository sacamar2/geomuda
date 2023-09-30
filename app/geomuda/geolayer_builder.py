from geopandas import sjoin
from geodata import GeoData
from cleaner import clean_geolayer
from polygon_mask import PolygonMask
from shapely import Point as sh_Point

def merge_geodata_mask(polygon_mask:PolygonMask, geodata:GeoData):
    
    layer_data=geodata.data
    gdf_polygons=polygon_mask.data

    # Cluster the points which are in any Polygon
    raw_polygon_mask_data=sjoin(layer_data,gdf_polygons,op='within')
    raw_polygon_mask_data_gjson_standard=raw_polygon_mask_data.copy()
    raw_polygon_mask_data_gjson_standard['geometry']=[sh_Point(p.y,p.x) for p in
                                                      raw_polygon_mask_data['geometry']]
    
    geolayer_data=clean_geolayer(raw_polygon_mask_data_gjson_standard)

    return geolayer_data
