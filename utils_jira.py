from atlassian import Jira
import re
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

def get_issues(jira, jql):
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

def process_issue(item):
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

def main():
    pickle_name = 'jira.pickle'
    data = load_pickle(picklename=pickle_name)

    if not 'jql' in data:
        jql = 'project = "OF" AND text ~ "events" ORDER BY created DESC'
        data['jql'] = jql

    jql = data.get('jql') 
    logger.info("JQL: {}".format(jql))

    file_name="issues.json"
    issues = load_json(file_name)
    if not issues or len(issues) == 0:
        jira = connect_jira()
        issues = get_issues(jira, jql)
        save_json(data=issues, file_name=file_name)
    
    if not 'issues' in data:
        data['issues'] = []
        for item in issues:
            data['issues'].append(process_issue(item))
        save_json(data=data['issues'], file_name='jira_tickets.json')
    
    logger.info("Processed {} tickets".format(len(data['issues'])))
    save_pickle(data=data, picklename=pickle_name)

    # process the description text for information
    events = {}
    for item in data.get('issues', []):
        descr = item.get('description')
        if descr:
            sentences = extract_event(descr)
            event = parse_clause(sentences)
            if len(event.get('condition'))>0:
                for k in ['name','summary', 'type', 'subtask', 'project', 'project key', 'status']:
                    event[k] = item.get(k)

                events[item.get('key')] = event

    data['events'] = events

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

    export_csv(data=rows, filename='of_events.csv')
    logger.info('Exported {} evetns'.format(len(rows)))

if __name__ == "__main__":
    main()
