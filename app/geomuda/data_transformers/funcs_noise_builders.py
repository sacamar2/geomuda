import pandas as pd
from datetime import date

from general_functions.variables import (def_root_path, def_noise_data_folder,
                                            def_noise_raw_data_file, def_noise_distr_name,
                                            def_noise_stations_data_file)

def build_all_noise_data(root_path=def_root_path):
    '''This method builds the csv data used to create the noise layer'''
    
    # GET RAW DATA
    raw_noise_data=build_raw_noise_data()

    # CLEAN RAW DATA
    cleaned_noise_data=build_cleaned_noise_data(raw_noise_data)

    # TRANSFORM IT USING THE METADATA EXPLANATION
    
    # 1. Build a layer per each data period: day, evening, night, total.
    trans_noise_data=build_trans_noise_data(cleaned_noise_data)
    
    # LOCATE EACH STATION
    located_noise_data=build_located_noise_data(trans_noise_data)
    
    all_noise_data=located_noise_data.copy()

    all_noise_data.to_csv(f'{def_noise_data_folder}/{def_noise_distr_name}.csv',index=False)
    return all_noise_data

def build_located_noise_data(trans_noise_data):
    located_noise_data=trans_noise_data.copy()
    station_location=pd.read_csv(def_noise_stations_data_file,sep=';',decimal='.',encoding='ANSI')
    lat_coords=[]
    lon_coords=[]
    for _,d in located_noise_data.iterrows():
        aux_station_id=d['NMT']
        aux_coords=station_location[station_location['Nº']==aux_station_id][['LATITUD_WGS84',
                                                                            'LONGITUD_WGS84']].values[0]
        aux_lat_coord=aux_coords[0]
        aux_lon_coord=aux_coords[1]
        
        lat_coords.append(aux_lat_coord)
        lon_coords.append(aux_lon_coord)

    located_noise_data['latitude']=lat_coords
    located_noise_data['longitude']=lon_coords

    return located_noise_data



def build_trans_noise_data(cleaned_noise_data):
    # SELECT WANTED COLUMNS
    # We will keep the LAEQ metric as it is more understandable. It is the potency which a sound must
    # have for the whole day to represent all the energy captured during the day on that station.
    # If the value is 60, it means that living there would mean a constant noise of 60dbA. 
    trans_noise_data=cleaned_noise_data.drop(['anio','mes','dia','LAS01','LAS10','LAS50'],axis=1)
    trans_noise_data=cleaned_noise_data[['datetime','tipo','LAEQ','NMT']]

    trans_noise_data=trans_noise_data.groupby(by=['NMT','tipo'],as_index=False).mean()

    return trans_noise_data


def build_cleaned_noise_data(raw_noise_data):
    cleaned_noise_data=raw_noise_data[raw_noise_data['anio']!=2020]
    return cleaned_noise_data

def build_raw_noise_data(filename=def_noise_raw_data_file):
    noise_data_from_file=pd.read_csv(filename,delimiter=';',decimal=',')

    # ADD DATETIME
    raw_noise_data=noise_data_from_file.copy()
    raw_noise_data['datetime']=[date(day=r['dia'],month=r['mes'],year=r['anio']) for _,r in raw_noise_data.iterrows()]

    return raw_noise_data
