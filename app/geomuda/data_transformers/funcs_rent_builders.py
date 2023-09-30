import os
from glob import glob
from pandas import DataFrame, concat
from bs4 import BeautifulSoup as bs

from general_functions.variables import def_renting_data_folder, def_rent_distr_website,def_rent_distr_name
from data_exporters.funcs_web_reading import get_wanted_properties
from geo_transformers.funcs_geotransformation import build_remove_geooutliers

def build_all_rent_data(max_pages:int=None,root_path=def_renting_data_folder,website=def_rent_distr_website)->DataFrame:
    '''This method builds the csv data used to create the geojson about houses'''
    # GET RAW DATA
    all_web_pages=get_all_web_pages(root_path)
    list_all_rent_data=[]
    pages_count=0
    for web_page in all_web_pages[:max_pages]:
        print(f'Starting with the web page: \
              {pages_count}/{len(all_web_pages)}')
        
        list_all_rent_data.append(build_rent_data(web_page))
        pages_count+=1
    
    # CLEAN RAW DATA
    # Avoid having multiple points in the same coordinates, cleaning table
    cleaned_all_rent_data=concat(list_all_rent_data).dropna().drop_duplicates(subset=['latitude','longitude'])
    
    # Remove outliers points which might be misgeolocated
    cleaned_all_rent_data=build_remove_geooutliers(cleaned_all_rent_data)

    all_rent_data=cleaned_all_rent_data.copy()
    all_rent_data.to_csv(f'{def_renting_data_folder}/{def_rent_distr_name}.csv')
    
    return all_rent_data

def get_all_web_pages(root_path:str):
    current_dir=os.getcwd()
    os.chdir(root_path+"/html_pages")
    all_web_pages=glob("*.html")
    all_web_pages=[root_path + "/" + i for i in all_web_pages]
    os.chdir(current_dir)
    return all_web_pages

def build_rent_data(filepath='html_pages/idealista.html'):
    '''For each webpage the data is extracted and formated as DataFrame'''
    raw_html=open(filepath,'r',encoding='utf-8').read()
    web_html=bs(raw_html,features='lxml')
    all_entries=web_html.find_all('div',class_="item-info-container")
    
    all_properties=[p for p in [get_wanted_properties(entry)
                                for entry in all_entries
                                ] if p is not None]

    rent_data=DataFrame(all_properties)
    return rent_data


