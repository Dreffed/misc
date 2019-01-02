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
    
    object_types = {}

    if 'files' in data:
        print('Files scanned{}'.format(len(data['files'])))

        for dwg_file in data['files']:
            file_name = dwg_file['file']
            logger.info('{}'.format(file_name))

            for dwg_page in dwg_file['pages']:
                logger.info('{}'.format('\t{}'.format(dwg_page['name'])))
                if 'objects' in dwg_page:
                    for objectype in dwg_page['objects']:
                        if not objectype in object_types:
                            object_types[objectype] = []

                        for s in dwg_page['objects'][objectype]:   
                            s_data = dwg_page['objects'][objectype][s]
                            o_data = {}

                            # file data
                            o_data['fileGUID'] = dwg_file['GUID']
                            o_data['filename'] = dwg_file['name']
                            o_data['title'] = dwg_file['title']
                            o_data['creator'] = dwg_file['creator']
                            
                            # page data
                            o_data['pageGUID'] = dwg_page['GUID']
                            o_data['pagename'] = dwg_page['name']

                            #shape_data
                            o_data['objectype'] = objectype
                            o_data['shapeGUID'] = s_data['GUID']
                            o_data['shapeID'] = s_data['id']
                            o_data['shapeName'] = s_data['name']
                            o_data['shapeType'] = s_data['type']
                            o_data['shapeText'] = s_data['Text']
                            if 'callouts' in s_data:
                                o_data['shapeCallouts'] = s_data['callouts']
                            if 'connects' in s_data:
                                o_data['shapeConnects'] = s_data['connects']
                            if 'connected_shapes' in s_data:
                                o_data['shapeConnected'] = s_data['connected_shapes']
                            if 'contained_shapes' in s_data:
                                o_data['shapeContain'] = s_data['contained_shapes']

                            # store
                            object_types[objectype].append(o_data)

                        

    else:
        print('no files found in saved data! \n\tPath: {}'.format(data['folders']))

    return object_types

pickle_file = 'visio_data.pickle'
data = get_pickle_data( pickle_file)
object_types = summarize_data(data)

for objectype in object_types:
    logger.info('{}'.format('\t\t{}:{}'.format(objectype, len(object_types[objectype]))))
