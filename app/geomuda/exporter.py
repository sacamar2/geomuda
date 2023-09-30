'''This module is responsible of reading the given data, check the format, and standarise it'''
from pandas import DataFrame, read_csv
from numpy import number, source
from sys import exit

from glob import glob
import logging


def read_source_data(fpath:str, fextension:str='csv') -> DataFrame:
    # GET FILE EXTENSION
    fextension='csv' # TODO: Parse the fpath to get the file extension
    # READ FILE
    try:
        if fextension=='csv':
            source_data=read_csv(fpath)
        logging.info(f'File from {fpath} was got!')
        return source_data
    
    except Exception as e:
        logging.error(f'It wasnt possible to get the file from this address: {fpath}')
        exit(1)

def check_source_data_format(source_data: DataFrame) -> (bool, str):
    check=False
    
    # IF DATA HAS LATITUDE AND LONGITUDE
    data_fields=[c.lower() for c in source_data]
    check=('latitude' in data_fields) and ('longitude' in data_fields)
    if not check:
        logging.error('Data has no proper latitude and longitude fields')
        exit(1)
    
    # IF DATA HAS AT LEAST A NUMERICAL COLUMN
    check=len(source_data.select_dtypes(include=number).columns.tolist())>0
    if not check:
        logging.error('Data has no numerical field')
        exit(1)

    return check

def standarise_source_data(source_data:DataFrame) -> DataFrame:
    std_data=source_data.copy()
    # FIND LATITUDE AND LONGITUDE COLUMNS
    latitude_fname=[fname for fname in
                    source_data if fname=='latitude'.casefold()]

    longitude_fname=[fname for fname in
                    source_data if fname=='longitude'.casefold()]
    
    # RENAME DATAFRAME to lat/lon
    std_data.rename(columns={latitude_fname:'lat',
                     longitude_fname:'lon'},inplace=True)
    
    # add the Point geometry, ...
    #std_data['geometry']=...
    
    return std_data

