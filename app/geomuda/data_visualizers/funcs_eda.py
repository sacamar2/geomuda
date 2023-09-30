'''This module is meant to allocate all the methods which help to do an
early Exploratory Data Analysis about the geojsons produced by the code.

It is done because of the need to understand the behaviour of some part of the codes beyond the table result.
Some filters outputs are unexpected and we needed a faster way to check the output than add it into Tableau.
'''

from matplotlib import pyplot as plt
from geopandas import GeoDataFrame, read_file, GeoSeries

def do_show_geolayer(gdf_data:GeoDataFrame):
    
    madrid=read_file('./data/rent_data/map_barrios/barrios.shp')
    madrid.to_crs(epsg=4326,inplace=True)

    madrid['barrio_area']=[b.area for b in madrid.geometry]
    biggest_barrios=madrid.sort_values(by=['barrio_area']).iloc[:10]
    
    fig, ax = plt.subplots(figsize=(10, 8))
    for _,bb in biggest_barrios.iterrows():
        plt.text(x=bb.geometry.centroid.x,y=bb.geometry.centroid.y,s=bb.NOMDIS)

    # Plotting the WorldMap
    GeoSeries(madrid.boundary,crs='4326').plot(ax=ax, alpha=0.2, color="grey")

    # Plotting each selected polygon
    GeoSeries(gdf_data['polygon'],crs='4326').plot(ax=ax,alpha=0.3,color='red')
    
    # Plotting each centroid
    GeoSeries(gdf_data['polygon_centroids'],crs='4326').plot(ax=ax,)

    plt.show(block=False)

    return 0
