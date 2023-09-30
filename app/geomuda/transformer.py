from geolayer import GeoLayer, MultiGeoLayer
from geodata import GeoData
from exporter import standarise_source_data
from cleaner import clean_source_data
from polygon_mask import PolygonMask
from numpy import number

def from_geodata_to_geolayer(geodata: GeoData) -> GeoLayer:
    # STANDARISE
    geodata.data=standarise_source_data(geodata.data)
    geodata._status='standard'
    
    # CLEAN DATA
    geodata.data=clean_source_data(geodata.data)
    geodata._status='cleaned'

    # POLYGON MASK GENERATOR
    polygon_mask=PolygonMask(geodata.data)
    
    # SOURCE DATA TO GEODATAFRAME

    # SJOIN POLYGONMASK + SOURCE DATA TO GEODATAFRAME

    # CLEAN SJOIN DATA

    # CREATE GeoLayer

    geolayer=...
    return geolayer
