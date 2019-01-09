from simple_salesforce import Salesforce, SFType, SalesforceResourceNotFound
import json
import os
from datetime import datetime
import logging
from logging.config import fileConfig
from getFiles import get_pickle_data, save_pickle_data

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

config_path = r'sf.secrets.json'
instance = 'KaptioStaging'
config_data = get_config(config_path, instance)

pickle_file = 'salesforce_data.pickle'
data = get_pickle_data( pickle_file)
if not instance in data:
    data[instance] = {}

sf = connect_sf(config_data)
all_describe = sf.describe()
s_objs = all_describe['sobjects']

# save the runtime details
obj_list = []

if not 'objects' in data[instance]:
    data[instance]['objects'] = {}

# scan the objects and save to a list...
for obj in s_objs:
    #logger.debug(obj)
    logger.info('\t{}\t-> {}'.format(obj['label'], obj['name']))
    obj_list.append(obj['name'])
    if not obj['name'] in data[instance]['objects']:
        data[instance]['objects'][obj['name']] = {}

# now to store the metadata... 
for sf_name in obj_list:
    obj_data = get_object(sf, sf_name)
    logger.info(json.dumps(obj_data, indent=4))
    
    data[instance]['objects'][sf_name] = obj_data
    break

save_pickle_data(data, pickle_file)

