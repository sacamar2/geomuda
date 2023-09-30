
# DEFAULT DIRECTORIES ABOUT INPUT DATA
def_root_path="D:/PROJECTS/IT/GIT REPO/geomuda/app/geomuda"

def_data_folder=f"{def_root_path}/data"

def_renting_data_folder=f"{def_data_folder}/rent_data"
def_noise_data_folder=f"{def_data_folder}/noise_data"

def_noise_raw_data_file=f"{def_noise_data_folder}/madrid_noise.csv"
def_noise_stations_data_file=f"{def_noise_data_folder}/madrid_stations.csv"

# OUTPUT FILENAME FOR EACH LAYER TYPE
def_output_geojsons=f'{def_root_path}/geojsons'

# PARAMETERS FOR GEOLOCATION and GEOTRANSFORMATIONS METHODS
max_retries=3
def_geooutliers_perc=90
def_square_size=1000 # meters
movement_mapping={'north':0,'south':180,'east':90,'west':270}
