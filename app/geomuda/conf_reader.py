''' This module is responsible to get the data from the conf files
and make it available to other modules '''

from dataclasses import dataclass

@dataclass
class ConfReader():
    conf_file: str
    _conf_data: dict
    
def read_custom_conf(conf_data:str) -> dict:
    custom_conf={}
    return custom_conf

