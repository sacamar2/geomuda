from dataclasses import dataclass
from typing import List

from geopandas import GeoDataFrame

@dataclass
class GeoLayer:
    data: GeoDataFrame
    name: str
    common_properties: List
    property_name: str

    def to_file(self):
        self.data.to_json(f'{self.name}_{self.property_name}.geojson')
    
    def to_geojson(self):
        self.data.to_json(f'{self.name}_{self.property_name}.geojson')

@dataclass
class MultiGeoLayer:
    geolayers: List[GeoLayer]
    