from simple_salesforce import Salesforce, SFType, SalesforceResourceNotFound
import json
import os
from datetime import datetime

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

        print('Created empty config file [{}], please update and run again!'.format(config_path))

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
    print('Config loaded... {}'.format(datetime.now()))
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
        
    return result

config_path = r'sf.secrets.json'
instance = 'KaptioStaging'
config_data = get_config(config_path, instance)

sf = connect_sf(config_data)
all_describe = sf.describe()
s_objs = all_describe['sobjects']

data = dict()   
data[instance] = {}

# save the runtime details


obj_list = []

for obj in s_objs:
    #print(obj)
    print('\t{}\t-> {}'.format(obj['label'], obj['name']))
    obj_list.append(obj['name'])

for sf_name in obj_list:
    sf_obj = get_object(sf, sf_name)
    print(json.dumps(sf_obj, indent=4))