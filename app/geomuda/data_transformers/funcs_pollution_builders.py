


def build_all_pollution_data():
    '''This method builds the csv data used to create the geojson about houses'''
    '''
    all_web_pages=get_all_web_pages(root_path)
    list_all_rent_data=[]
    pages_count=0
    for web_page in all_web_pages:
        print(f'Starting with the web page: \
              {pages_count}/{len(all_web_pages)}')
        
        list_all_rent_data.append(build_rent_data(web_page))
        pages_count+=1
    
    all_rent_data=pd.concat(list_all_rent_data).dropna(inplace=True)
    
    # Avoid having multiple points in the same coordinates
    all_rent_data.drop_duplicates(subset=['latitude','longitude'], inplace=True)

    all_rent_data.to_csv(f'{def_renting_data_folder}/{website}/{def_rent_distr_name}.csv')
    return all_rent_data
    '''
    print(1)