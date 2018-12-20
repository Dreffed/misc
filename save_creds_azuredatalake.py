import json
import getpass

# Enter your keys/secrets as strings in the following fields
credentials = {}  
credentials['subscription_id'] = None
credentials['tenant_id'] = None  

paths = {}
paths['datalake_store_name'] = None
paths['source'] = None
paths['archive'] = None
paths['datalake_path'] = None

settings = {}
settings['credentials'] = credentials
settings['paths'] = paths

for item in settings['credentials']:
    try:
        v = getpass.getpass(prompt="Enter {}:".format(item))
    except Exception as error:
        print('ERROR: {}'.format(error))
    else:
        settings['credentials'][item] = v

for item in settings['paths']:
    try:
        v = getpass.getpass(prompt="Enter {}:".format(item))
    except Exception as error:
        print('ERROR: {}'.format(error))
    else:
        settings['paths'][item] = v

# Save the credentials object to file
with open("datalake_settings.json", "w") as file:  
    json.dump(settings, file)