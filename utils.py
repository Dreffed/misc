from json import load, dump
from os import path
import csv

def load_settings(file_name=r"settings.json"):
    if not path.exists(file_name):
        settings = {
            'neo4j': {
                'database_url':r'bolt://neo4j:test@localhost:7687'
            }
        }

        save_settings(settings, file_name)
        return settings
        
    # Load credentials from json file
    with open(file_name, "r") as file:  
        settings = load(file)
    return settings

def save_settings(settings = {}, file_name=r"settings.json"):
    # Save the credentials object to file
    with open(file_name, "w") as file:  
        dump(settings, file)    

def read_file(file_name):
    if not path.exists(file_name):
         print('File does not exist: {}'.format(file_name))
         return None
    with open(file_name) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            line_count += 1
            yield row

    print(line_count)