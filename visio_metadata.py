from getFiles import scanFiles, get_info, get_pickle_data, save_pickle_data
import sys
import os
import json
import logging
from logging.config import fileConfig
import csv
import uuid
import node_models as nm
from utils import load_settings, save_settings, read_file
from neomodel import (config, StructuredRel, StructuredNode, StringProperty, IntegerProperty,
    UniqueIdProperty, UniqueProperty, RelationshipTo, RelationshipFrom, DoesNotExist)

fileConfig('logging_config.ini')
logger = logging.getLogger(__name__)

neo_connect_file = "neo4j_settings.json"

settings = load_settings(neo_connect_file)
config.DATABASE_URL = settings['neo4j']['database_url']

def summarize_data(data):
    '''This will scan the log file and produce stats in the data found'''
    if not isinstance(data, dict):
        return None
    
    object_types = {}
    file_index = 1000
    if 'files' in data:
        print('Files scanned{}'.format(len(data['files'])))

        for dwg_file in data['files']:
            file_name = dwg_file['file']
            if not 'GUID' in dwg_file:
                dwg_file['GUID'] = uuid.uuid4()            
            file_guid = str(dwg_file['GUID'])
            file_name = dwg_file['name']
            file_title = dwg_file['title']
            file_creator = dwg_file['creator']
            file_folder = dwg_file['folder']

            logger.info('{}'.format(file_name))

            file_index += 1
            try:
                file_node = nm.FileNode.nodes.get(id=file_guid)
            except DoesNotExist as e:
                file_node = nm.FileNode(id=file_guid, local_id=file_index, name=file_name, path=file_folder).save()

            page_index = 1000

            for dwg_page in dwg_file['pages']:
                logger.info('{}'.format('\t{}'.format(dwg_page['name'])))

                if not 'GUID' in dwg_page:
                    dwg_page['GUID'] = uuid.uuid4()
                page_guid = str(dwg_page['GUID'])
                page_name = dwg_page['name']
                page_index += 1

                try:
                    page_node = nm.PageNode.nodes.get(id=page_guid)
                except DoesNotExist as e:
                    page_node = nm.PageNode(id=page_guid, local_id=page_index, name=page_name)

                try:
                    file_node.contains.connect(page_node)
                except Exception as e:
                    print('ERROR: \n\t{}\n\t{}\n===\t{}'.format(file_node, page_node, e))

                if 'objects' in dwg_page:
                    for objectype in dwg_page['objects']:
                        if not objectype in object_types:
                            object_types[objectype] = []

                        for s in dwg_page['objects'][objectype]:   
                            s_data = dwg_page['objects'][objectype][s]
                            o_data = {}

                            # file data
                            o_data['fileGUID'] = file_guid
                            o_data['filename'] = file_name
                            o_data['title'] = file_title
                            o_data['creator'] = file_creator
                            
                            # page data                                
                            o_data['pageGUID'] = page_guid
                            o_data['pagename'] = page_name

                            #shape_data
                            o_data['objectype'] = objectype
                            if not 'GUID' in s_data:
                                s_data['GUID'] = uuid.uuid4()

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

def export_csv(fields, data):
    shape_count = 0

    keys = fields.keys()
    logger.info(keys)

    filename = 'shape.csv'
    with open(filename, 'w', encoding='utf-8-sig', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()

        for objectype in data:
            shape_count += len(data[objectype])
            logger.info('{}'.format('\t\t{}:{}'.format(objectype, len(data[objectype]))))

            dict_writer.writerows(data[objectype])

    logger.info('\tProcessed {} shapes'.format(shape_count))

pickle_file = 'visio_data.pickle'
data = get_pickle_data( pickle_file)
object_types = summarize_data(data)
obj_model = {
"fileGUID":None, "filename":None, "title":None, "creator":None, "pageGUID":None, "pagename":None, "objectype":None, "shapeGUID":None, "shapeID":None, "shapeName":None, "shapeType":None, "shapeText":None, "shapeCallouts":None, "shapeConnects":None, "shapeConnected":None, "shapeContain":None
}

logger.info('Found {} object types'.format(len(object_types)))

export_csv(obj_model, object_types)
