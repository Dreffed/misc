from getFiles import scanFiles, get_info, get_pickle_data, save_pickle_data
import sys
import os
import json
import logging
from logging.config import fileConfig

fileConfig('logging_config.ini')
logger = logging.getLogger(__name__)

def summarize_data(data):
    '''This will scan the log file and produce stats in the data found'''
    if not isinstance(data, dict):
        return None
    
    if 'files' in data:
        print('Files in older: {}\n\tFound:{}'.format(data['folders'], len(data['files'])))

        for dwg_file in data['files']:
            file_name = dwg_file['file']
            logger.info('{}'.format(file_name))
            for dwg_page in dwg_file['pages']:
                logger.info('{}'.format('\t{}'.format(dwg_page['name'])))
                if 'objects' in dwg_page:
                    for objectype in dwg_page['objects']:
                        logger.info('{}'.format('\t\t{}:{}'.format(objectype, len(dwg_page['objects'][objectype]))))

    else:
        print('no files found in saved data! \n\tPath: {}'.format(data['folders']))

pickle_file = 'visio_data.pickle'
data = get_pickle_data( pickle_file)
summarize_data(data)
