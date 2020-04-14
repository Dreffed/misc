from json import load, dump, dumps
from os import path
import csv
import logging
from logging.config import fileConfig

fileConfig('logging_config.ini')
logger = logging.getLogger(__name__)

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

def export_csv(data, filename = 'export.csv', fields = None):
    if fields is None:
        keys = data[0].keys()        
    else:
        keys = fields.keys()

    logger.info(keys)

    with open(filename, 'w', encoding='utf-8-sig', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()

        dict_writer.writerows(data)

def display_object(data, depth=1):
    print_items(data, depth)

def print_items(obj, depth=0, max_depth=5):
    if depth > max_depth:
        return
    
    print('{}{}=>{}'.format('','\t'*depth, type(obj)))
    if isinstance(obj, dict):
        for k,v in obj.items():
            if not v is None:
                try:
                    print('{}{}:{} => {}'.format('\t'*(depth+1), k, type(v), len(v)))
                    
                except:
                    print('{}{}:{}'.format('\t'*(depth+1), k, type(v)))
                print_items(v, depth+1)
            else:
                print('{}{}'.format('\t'*(depth+1), k))
    elif isinstance(obj, list):
        print('{}List of {} items'.format('\t'*(depth+1), len(obj)))
        max = (5 if len(obj) > 5 else len(obj))
        for i in  range(0, max):
            print('{}--\t{}'.format('\t'*(depth+1), obj[i]))
        if len(obj) > 0:
            print_items(obj[0],depth+1)
    else:
        try:
            print('{}{}:{} items'.format('\t'*(depth+1), type(obj), len(obj)))
        except:
            print('{}[{}] items'.format('\t'*(depth+1), "ERROR"))