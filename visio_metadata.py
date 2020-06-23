from getFiles import scanFiles, get_info, get_pickle_data, save_pickle_data
import os
import json
import logging
from logging.config import fileConfig
import csv
import uuid
<<<<<<< HEAD
#import node_models as nm
from utils import load_settings, save_settings, read_file, export_csv, print_items, display_object
#from neomodel import db, config, StructuredRel, StructuredNode, StringProperty, IntegerProperty, \
#    UniqueIdProperty, UniqueProperty, RelationshipTo, RelationshipFrom, DoesNotExist
=======
import node_models as nm
from utils import load_json, save_json, read_file, export_csv
from neomodel import db, config, StructuredRel, StructuredNode, StringProperty, IntegerProperty, \
    UniqueIdProperty, UniqueProperty, RelationshipTo, RelationshipFrom, DoesNotExist
>>>>>>> 280c838948e17c71f4725a758b0f92c92741577f

fileConfig('logging_config.ini')
logger = logging.getLogger(__name__)

def connect():
    neo_connect_file = "neo4j_settings.json"

<<<<<<< HEAD
    settings = load_settings(neo_connect_file)
    uname = settings['neo4j']['user']
    token = settings['neo4j']['token']
    db_url = settings['neo4j']['database_url'].format(uname, token)
    print(db_url)
    config.DATABASE_URL = db_url
    db.set_connection(db_url)
=======
settings = load_json(neo_connect_file)
config.DATABASE_URL = settings['neo4j']['database_url']
db.set_connection(settings['neo4j']['database_url'])
>>>>>>> 280c838948e17c71f4725a758b0f92c92741577f

def summarize_data(data):
    '''This will scan the log file and produce stats in the data found'''
    if not isinstance(data, dict):
        return None
    
    idx = 0

    object_types = {}
    relationships = {}

    file_index = 1000
    if 'files' in data:
        print('Files scanned{}'.format(len(data['files'])))

        for dwg_file in data['files']:
            idx += 1
            file_name = dwg_file['file']
            if not 'GUID' in dwg_file:
                dwg_file['GUID'] = uuid.uuid4()

            file_guid = str(dwg_file['GUID'])
            file_name = dwg_file.get('name','M-{}'.format(idx))
            file_title = dwg_file.get('title')
            file_creator = dwg_file.get('creator')
            file_folder = dwg_file.get('folder')
            file_wbs = '{}'.format(file_index)

            if not file_wbs in relationships:
                relationships[file_wbs] = {}
                relationships[file_wbs]['pages'] = {}
                relationships[file_wbs]['file'] = file_name
                relationships[file_wbs]['title'] = file_title
                relationships[file_wbs]['creator'] = file_creator

            logger.info('{}'.format(file_name))

            file_index += 1
            try:
                file_node = nm.FileNode.nodes.get(id=file_guid)
            except DoesNotExist:
                file_node = nm.FileNode(id=file_guid, name=file_name, path=file_folder, wbs=file_wbs).save()

            relationships[file_wbs]['guid'] = file_guid

            page_index = 1000

            for dwg_page in dwg_file.get('pages',[]):
                page_data = {}

                logger.info('{}'.format('\t{}'.format(dwg_page['name'])))
                #print('{}'.format('=====\n{}'.format(dwg_page['name'])))

                if not 'GUID' in dwg_page:
                    dwg_page['GUID'] = uuid.uuid4()

                page_guid = str(dwg_page['GUID'])
                page_name = dwg_page['name']
                page_index += 1
                page_wbs = '{}.{}'.format(file_wbs, page_index)

                page_data['name'] = page_name
                page_data['guid'] = page_guid

                try:
                    page_node = nm.PageNode.nodes.get(id=page_guid)
                except DoesNotExist:
                    page_node = nm.PageNode(id=page_guid, name=page_name, wbs=page_wbs).save()
                    
                if 'objects' in dwg_page:
                    pool = {}
                    swimlanes = {}
                    process_nodes = {}
                    dyn_connector = {}
                    callouts = {}

                    process_type = 'CFF Container'
                    if process_type in dwg_page['objects']:
                        for s in dwg_page['objects'][process_type]:
                            s_data = dwg_page['objects'][process_type][s]
                            obj_wbs = '{}.{}'.format(page_wbs, s_data['id'])
                            swimlanes = {}
                            if 'contained_shapes' in s_data:
                                for sub_obj in s_data['contained_shapes']:
                                    sub_wbs = '{}.{}'.format(page_wbs, sub_obj)
                                    swimlanes[sub_wbs] = {}

                            pool[obj_wbs] = {}
                            pool[obj_wbs]['swimlanes'] = swimlanes

                    process_type = 'Swimlane'
                    if process_type in dwg_page['objects']:
                        for s in dwg_page['objects'][process_type]:
                            s_data = dwg_page['objects'][process_type][s]
                            obj_wbs = '{}.{}'.format(page_wbs, s_data['id'])
                            processes = {}
                            if 'contained_shapes' in s_data:
                                for sub_obj in s_data['contained_shapes']:
                                    sub_wbs = '{}.{}'.format(page_wbs, sub_obj)
                                    processes[sub_wbs] = {}

                            swimlanes[obj_wbs] = {}
                            swimlanes[obj_wbs]['processes'] = processes

                    process_type = "Dynamic connector"
                    if process_type in dwg_page['objects']:
                        for s in dwg_page['objects'][process_type]:
                            s_data = dwg_page['objects'][process_type][s]
                            obj_wbs = '{}.{}'.format(page_wbs, s_data['id'])

                            o_data = {}
                            o_data['shapeGUID'] = s_data['GUID']
                            o_data['shapeText'] = s_data['Text']

                            if 'connected_shapes' in s_data:
                                for cell in s_data['connected_shapes']:
                                   o_data[cell['type']] = cell['id'] 

                            if not obj_wbs in dyn_connector:
                                dyn_connector[obj_wbs] = o_data

                    process_type = "Orthogonal"
                    if process_type in dwg_page['objects']:
                        for s in dwg_page['objects'][process_type]:
                            s_data = dwg_page['objects'][process_type][s]
                            obj_wbs = '{}.{}'.format(page_wbs, s_data['id'])

                            o_data = {}
                            o_data['shapeGUID'] = s_data['GUID']
                            o_data['shapeText'] = s_data['Text']

                            if 'connected_shapes' in s_data:
                                for cell in s_data['connected_shapes']:
                                   o_data[cell['type']] = cell['id'] 

                            if not obj_wbs in dyn_connector:
                                dyn_connector[obj_wbs] = o_data


                    for objectype in dwg_page['objects']:
                        obj = {}

                        if not objectype in object_types:
                            object_types[objectype] = []

                        for s in dwg_page['objects'][objectype]:   
                            s_data = dwg_page['objects'][objectype][s]
                            o_data = {}

                            obj_wbs = '{}.{}'.format(page_wbs, s_data['id'])

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
                            o_data['shapeContain'] = []
                            if 'contained_shapes' in s_data:
                                o_data['shapeContain'] = s_data['contained_shapes']

                            # store
                            object_types[objectype].append(o_data)

                            #print('{1}:{2}\t{0}\t{3}'.format(obj_wbs, s_data['type'], objectype, o_data['shapeContain']))
                    
                    # update the swimlanes with the found swimlanes
                    for pool_id in pool:
                        for swim_id in pool[pool_id]['swimlanes']:
                            if swim_id in swimlanes:
                                pool[pool_id]['swimlanes'][swim_id] = swimlanes[swim_id]

                if not 'pool' in page_data:
                    page_data['pool'] = pool

                # add the page to the file...
                if not page_wbs in relationships[file_wbs]['pages']:
                    relationships[file_wbs]['pages'][page_wbs] = page_data

    else:
        print('no files found in saved data! \n\tPath: {}'.format(data['folders']))

    #print('{}'.format(json.dumps(relationships, indent=4)))   
    return object_types

pickle_file = 'visio_data.pickle'
data = get_pickle_data( pickle_file)
object_types = summarize_data(data)
#print(object_types)
obj_model = {
"fileGUID":None, "filename":None, "title":None, "creator":None, "pageGUID":None, "pagename":None, "objectype":None, "shapeGUID":None, "shapeID":None, "shapeName":None, "shapeType":None, "shapeText":None, "shapeCallouts":None, "shapeConnects":None, "shapeConnected":None, "shapeContain":None
}

#logger.info('Found {} object types'.format(len(object_types)))

#print_items(obj=object_types)

rows = []
for k,v in object_types.items():
    rows.extend(v)

export_csv(fields=obj_model, data=rows)
