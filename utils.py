from json import load, dump, dumps
import pickle
from os import path
import csv
import logging
from logging.config import fileConfig

fileConfig('logging_config.ini')
logger = logging.getLogger(__name__)

def load_pickle(pickleName):
    data = {}
    if os.path.exists(pickleName):
        logger.info('Loading Saved Data... [%s]' % pickleName)
        with open(pickleName, 'rb') as handle:
            data = pickle.load(handle)
    return data

def save_pickle(data, pickleName):
    logger.info('Saving Data... [%s]' % pickleName)
    with open(pickleName, 'wb') as handle:
        pickle.dump(data, handle)

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
