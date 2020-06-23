from atlassian import Confluence
from atlassian import Jira
import json

def process_jira(item, fields=None):
    if not fields:
        fields = ['description']

    data = {}
    data['id'] = item.get('id')
    data['key'] = item.get('key')

    for f in fields:
        data[f] = item.get('fields',{}).get(f)
    
    print(json.dumps(data,indent=4))
    return data    

url = 'https://rockym.atlassian.net'
username='dgloyncox@rockymountaineer.com'
apikey='gpZgK6O6WC8Cnitgif6q0D08'

space = 'Ops Fulfillment'

switch = False

if switch:
    confluence = Confluence(url=url, username=username, password=apikey)

    status = confluence.create_page(
        space=space,
        title='This is the title',
        body='This is the body. You can use <strong>HTML tags</strong>!')

    print(status)
else:
    jira = Jira(url=url, username=username, password=apikey)

    JQL = 'project = "OF" AND text ~ Event ORDER BY created DESC'.format(space)
    data = jira.jql(JQL)

    #print(json.dumps(data, indent=4, sort_keys=True))


    issues = data.get('issues', [])
    for item in issues:
        process_jira(item)
