from dataclasses import dataclass
from typing import List

from geolayer import MultiGeoLayer
from transformer import from_geodata_to_multigeolayer
from conf_reader import read_custom_conf
from exporter import check_source_data_format, read_source_data
from pandas import DataFrame
from numpy import number
import json
import logging
from transformer import from_geodata_to_geolayer

@dataclass
class GeoData:
    data: DataFrame = None
    _source_data_extension: str = 'csv'
    name: str
    fpath: str
    conf_file: str = ""
    _conf_data: dict = {}
    _has_custom_conf: bool = False
    property_fields: List[str] = None
    common_properties: List[str] = None
    _status: str = "raw" #raw, checked, standard, cleaned
    multigeolayer: MultiGeoLayer = None

    def __post_init__(self):
        if self.data is None:
            try:
                self.data=read_source_data()
            except Exception as e:
                logging.error(f'It wasnt possible to read the data from {self.fpath}')
                exit(1)
        try:
            check_source_data_format(self.data)
        except Exception as e:
            logging.error('It wasnt possible to know if the source data is valid')
            exit(1)
        
        if self.conf_file!="":
            try:
                self._conf_data=json.load(self.conf_file)
                self._has_custom_conf=True
                self._conf_data=read_custom_conf(self._conf_data)
            except Exception as e:
                logging.warning(f'The file {self.conf_file} wasnt able to read')

        #try:
        #    self.geolayer=from_geodata_to_multigeolayer(self)
        #except Exception as e:
        #    logging.error('It wasnt possible to transform your data into aggregated geolayers')
            
    def to_multigeolayer(self):
        # GET THE FIELDS WHICH DEFINES AN INDIVIDUAL LAYER
        if self._status not in ('standard','cleaned'):
            logging.warning('The geodata is not clean enough still, try again when it is cleaned')
            return 1
        
        if self.property_fields is None:
            self.property_fields=[c for c in self.data.select_dtypes(number).columns.tolist()
                                  if c not in ('lat','lon')]
            
            self.common_properties=[c for c in self.data.columns
                                    if c not in self.property_fields+['lat','lon']]

        aux_multigeolayer=[]
        for f in self.property_fields:
              aux_multigeolayer.append(from_geodata_to_geolayer(self, f))
        
        self.multigeolayer=MultiGeoLayer(aux_multigeolayer)
        

    def to_geojson(self):
        for glayer in self.multigeolayer:
            glayer.to_geojson()


@dataclass
class GeoData1D:
    name: str
    data: DataFrame
    property_name: str
    common_properties: List[str]

    def __post_init__(self):
        accepted_fields=self.common_properties+[self.property_name]
        non_common_properties=[f for f in self.data
                                     if f not in accepted_fields]
        
        self.data=self.data.drop(non_common_properties)
