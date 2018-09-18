import json
import getpass

# Enter your keys/secrets as strings in the following fields
credentials = {}  
credentials['CONSUMER_KEY'] = None
credentials['CONSUMER_SECRET'] = None  
credentials['ACCESS_TOKEN'] = None
credentials['ACCESS_SECRET'] = None

for item in credentials:
    try:
        v = getpass.getpass(prompt="Enter {}:".format(item))
    except Exception as error:
        print('ERROR: {}'.format(error))
    else:
        credentials[item] = v
        
# Save the credentials object to file
with open("twitter_credentials.json", "w") as file:  
    json.dump(credentials, file)