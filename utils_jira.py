from atlassian import Jira
import re
import os
from datetime import datetime
from utils import load_json, save_json, load_pickle, save_pickle, export_csv
from nltk.tokenize import sent_tokenize
import logging
from logging.config import fileConfig

fileConfig('logging_config.ini')
logger = logging.getLogger(__name__)

def connect_jira():
    config_file = "creds.json"
    settings = load_json(config_file)

    url = settings.get("atlassian",{}).get("url")
    username = settings.get("atlassian",{}).get("username")
    token = settings.get("atlassian",{}).get("token")

    jira = Jira(
        url=url,
        username=username,
        password=token)
    return jira

def get_tickets(jira, jql):
    issues = []
    total = 0
    start = 0
    
    data = jira.jql(jql)
    try:
        while True:
            start = len(issues)
            data = jira.jql(jql, start=start, limit=100)

            total = int(data.get("total", 0))
            start = int(data.get("startAt", 0))
            results = int(data.get("maxResults", 0))
            issues.extend(data.get("issues", []))
            print(total, start, results)
            if len(issues) >= total:
                break

    except Exception as ex:
        print(ex)
    return issues

def process_ticket(item):
    """ Extract fields from JIRA Issue JSON
        => Key
        => id
        : fields
            => name
            => description
            => summary
            : issuetype
                +> name
                => subtask
            : project
                => name
                => key
            : status
                => name
    """
    data = {}
    data['key'] = item.get('key')
    data['id'] = item.get('id')
    data['name'] = item.get('fields', {}).get('name')
    data['summary'] = item.get('fields', {}).get('summary')
    data['description'] = item.get('fields', {}).get('description')

    data['type'] = item.get('fields', {}).get('issuetype', {}).get('name')
    data['subtask'] = item.get('fields', {}).get('issuetype', {}).get('subtask')

    data['project'] = item.get('fields', {}).get('project', {}).get('name')
    data['project key'] = item.get('fields', {}).get('project', {}).get('key')

    data['status'] = item.get('fields', {}).get('project', {}).get('status')
    return data

def parse_clause(sentences):
    data = {}
    data['pre'] = []
    data['condition'] = []
    data['result'] = []
    data['notes'] = []
    data['freq'] = []
    state = 'pre'

    for s in sentences:
        re_title = re.compile('h[\d]{0,1}\.')
        if '*IF*' in s:
            state = 'condition'

        if '*THEN*' in s:
            state = 'result'

        if re_title.search(s):
            continue

        if 'Triggering Condition' in s:
            state = 'condition'
            continue

        if 'Business Implication' in s:
            state = 'notes'
            continue

        if 'Frequency' in s:
            state = 'freq'
            continue

        data[state].append(s)

    return data

def extract_event(description):
    data = []
    # replace the newlines...
    phrases =  [p for p in description.split('\n') if p]
    for p in phrases:
        for s in sent_tokenize(p):
            data.append(s)
    return data

def filter_events(data, filename="events.csv"):
    # process the description text for information
    events = {}
    for k,v in data.get('tickets', {}).items():
        descr = v.get('description')
        if descr:
            sentences = extract_event(descr)
            event = parse_clause(sentences)
            if len(event.get('condition'))>0:
                for f in ['name','summary', 'type', 'subtask', 'project', 'project key', 'status']:
                    event[f] = v.get(f)

                events[k] = event

    # export the events to a csv
    rows = []
    for k,v in events.items():
        row = {}
        row['key'] = k

        for t, c in v.items():
            if isinstance(c, list):
                row[t] = '\n'.join(c)
            else:
                row[t] = c

        rows.append(row)

    export_csv(data=rows, filename=filename)
    logger.info('Exported {} events'.format(len(rows)))
    return events

def process_extract(config):
    """ this will run the query specified in the config extract array
    and save of the results to a pickle file
    """
    logging.info("Running {}".format(config.get("name")))

    folders = config.get("file", {}).get("location",{}).get("folders",[])
    root = config.get("file", {}).get("location",{}).get("root","~")
    folder = os.path.expanduser(os.path.join(root, *folders))
    name = config.get("file", {}).get("location",{}).get("name","jira_utils")

    pickle_name = os.path.join(folder, "{}.{}".format(name, config.get("file", {}).get("type","pickle")))

    data = load_pickle(picklename=pickle_name)
    if "tickets" not in data:
        data['tickets'] = {}

    jql = config.get("jql")

    if not 'jql' in data:
        data['jql'] = jql

    logger.info("JQL: {}".format(jql))

    # query jira and pull down the issues
    runtime = datetime.now().strftime("%Y-%m-%d %H:%M%S")
    file_name = os.path.join(folder, "{}_issues.json".format(name))
    issues = load_json(file_name)

    reload = True
    if issues and issues.get("jql") == jql and len(issues.get('tickets',[])) > 0:
        # we have a version of this query run already...
        reload = False

    if reload:
        issues = {}
        jira = connect_jira()
        issues['jql'] = jql
        issues['runtime'] = runtime
        issues['tickets'] = get_tickets(jira, jql)
        save_json(data=issues, file_name=file_name)
        data['jql'] = jql
        
    for ticket in issues.get("tickets"):
        item = process_ticket(ticket)
        key = item.get("key")

        old_ticket = data.get("tickets",{}).get(key, None)
        
        if old_ticket:
            # check this ticket is current
            # curently alway update
            update_ticket = True
        else:
            update_ticket = True

        if update_ticket:
            data['tickets'][key] = item

    logger.info("Processed {} tickets".format(len(data['tickets'])))
    save_pickle(data=data, picklename=pickle_name)

    if config.get("filter"):
        filter_name = config.get("filter",{}).get("name","filter")
        csv_name = os.path.join(folder, "{}.{}.csv".format(name, filter_name))
        data[filter_name] = filter_events(data=data, filename=csv_name)

def main():
    """ performs the defualt run of the program
    """
    config_file = "utils_jira_config.json"
    config = load_json(config_file)

    for e in config.get("extracts", []):
        process_extract(e)


if __name__ == "__main__":
    main()
