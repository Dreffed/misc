from simple_salesforce import Salesforce, SFType, SalesforceResourceNotFound
import json
import os
from datetime import datetime
import logging
from logging.config import fileConfig
from getFiles import get_pickle_data, save_pickle_data
from utils import read_file, export_csv

fileConfig('logging_config.ini')
logger = logging.getLogger(__name__)

def get_config(config_path, instance = "Staging"):
    # the secrets file contains the following:
    # username
    # password
    # token
    if not os.path.exists(config_path):
        sf_cnf_data = [{
            'label':instance,
            'username':'<<>>',
            'passwd': '<<>>',
            'token': '<<>>',
            'uri': '<<>>'
        }]
        
        with open(config_path, 'w') as outfile:
            json.dump(sf_cnf_data, outfile)

        logger.warn('Created empty config file [{}], please update and run again!'.format(config_path))

    sf_cnf = json.load(open(config_path))
    sf_cnf_data = None
    
    for cnf_data in sf_cnf:
        if cnf_data['instance'] == instance:
            sf_cnf_data = cnf_data
            break
    
    if sf_cnf_data is None:
        raise 'invalid label'
        
    if sf_cnf_data['passwd'] == '<<>>':
        import getpass
        sf_cnf_data['passwd'] = getpass.getpass(" Please enter you password:")
    logger.info('Config loaded... {}'.format(datetime.now()))
    return sf_cnf_data

def connect_sf(config_data):
    sf = Salesforce(username=config_data['username'], password=config_data['passwd'], security_token=config_data['token'], sandbox=True)
    return sf

def get_object(sf, obj_name):
    result = {}
    try:
        result['metadata'] = SFType(obj_name, sf.session_id, sf.sf_instance, sf.sf_version, sf.proxies).metadata()
        result['describe'] = SFType(obj_name, sf.session_id, sf.sf_instance, sf.sf_version, sf.proxies).describe()
    except SalesforceResourceNotFound:
        result['error'] = 'SalesforceResourceNotFound' 
        logger.error('{} not found!'.format(obj_name))
        
    return result

def get_metadata(sf):
    """This will get the object list from SF"""
    data = {}
    all_describe = sf.describe()

    s_objs = all_describe['sobjects']
    # scan the objects and save to a list...
    for obj in s_objs:
        row = {}
        row['name'] = obj['name']
        row['label'] = obj['label']
        row['custom'] = obj['custom']
        row['activateable'] = obj['activateable']
        row['keyPrefix'] = obj['keyPrefix']
        row['labelPlural'] = obj['labelPlural']

        row['raw'] = obj

        logger.info('\t{}\t-> {}'.format(obj['label'], obj['name']))
        data[row['name']] = row

    return data

def get_object_metadata(sf, name):
    """This will return the metadata for the selected objects.
    This will simplify the metadata to useful fields only"""
    data = {}
        
    result = get_object(sf, name)

    # now split out the result
    data['raw'] = result
    describe = result['describe']
    relationships = []
    for entry in describe['childRelationships']:
        row = {}
        row['table'] = entry['childSObject']
        row['field'] = entry['field']
        row['name'] = entry['relationshipName']

        relationships.append(row)
    data['relationships'] = relationships

    fields = []
    for entry in describe['fields']:
        row = {}
        row['name'] = entry['name']
        row['label'] = entry['label']
        row['type'] = entry['type']
        row['length'] = entry['length']
        row['byteLength'] = entry['byteLength']
        row['custom'] = entry['custom']
        row['scale'] = entry['scale']
        row['precision'] = entry['precision']
        row['calculated'] = entry['calculated']
        row['calculatedFormula'] = entry['calculatedFormula']
        row['soapType'] = entry['soapType']
        row['picklist'] = entry['picklistValues']
        if len(row['picklist']) > 0:
            p_rows = []
            for p in row['picklist']:
                p_row = {}
                p_row['active'] = p['active']
                p_row['defaultValue'] = p['defaultValue']
                p_row['label'] = p['label']
                p_row['validFor'] = p['validFor']
                p_row['value'] = p['value']

                p_rows.append(row)

        fields.append(row)
    
    data['fields'] = fields

    # get the record types
    rt_rows = []
    for rt in describe['recordTypeInfos']:
        rt_row = {}
        rt_row['available'] = rt['available']
        rt_row['default'] = rt['defaultRecordTypeMapping']
        rt_row['master'] = rt['master']
        rt_row['name'] = rt['name']
        rt_row['recordTypeId'] = rt['recordTypeId']

        rt_rows.append(rt_row)

    data['record_type'] = rt_rows

    return data

config_path = r'sf.secrets.json'
instance = 'KaptioStaging'
config_data = get_config(config_path, instance)

pickle_file = 'salesforce_data.pickle'
data = get_pickle_data( pickle_file)
if not instance in data:
    data[instance] = {}

sf = connect_sf(config_data)

# save the runtime details
data[instance] = get_metadata(sf)

for obj_name in data[instance]:
    row = data[instance][obj_name]
    result = get_object_metadata(sf, row['name'])

    data[instance][obj_name] = {**row, **result, 'scanned_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

save_pickle_data(data, pickle_file)
    
print(json.dumps(data, indent=4))




