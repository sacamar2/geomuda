from general_functions.funcs_aux import build_all_layer_data
from geo_transformers.funcs_geodata_formating import (build_standard_geodataframe,
                                                      build_standard_geojson, do_write_geojson)
from data_visualizers.funcs_eda import do_show_geolayer
from geo_transformers.funcs_geotransformation import build_polygon_mask_geodataframe, build_aggregated_geodataframe
from general_functions.variables import def_rent_distr_name

def do_tableau_rent_distr_geojson(filename:str=def_rent_distr_name,write_geojson:bool=True,plot_geojson:bool=True,
                                  layer_name:str='rent'):
    
    # FROM ANY SOURCE TO DATAFRAME FORMAT
    all_layer_data=build_all_layer_data(layer_name)
    
    # GEODATAFRAME + DATA AGGREGATION + DATA VISUALIZATION
    rent_geodataframe=build_standard_geodataframe(all_layer_data)
    rent_polygon_geodataframe=build_polygon_mask_geodataframe(rent_geodataframe)
    if plot_geojson: do_show_geolayer(rent_polygon_geodataframe)
    
    # GEOJSON + DATA EXPORTATION on a format for Tableau
    if write_geojson:
        rent_aggregated_geodataframe=build_aggregated_geodataframe(rent_polygon_geodataframe)
        rent_geojson=build_standard_geojson(rent_aggregated_geodataframe)
        do_write_geojson(layer_name,rent_geojson,filename)

