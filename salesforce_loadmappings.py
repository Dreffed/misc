import json
from getFiles import get_pickle_data, save_pickle_data

mapping_file = 'salesforce_mapping.txt'
pickle_file = 'salesforce_data.pickle'
data = get_pickle_data( pickle_file)

mapping_data = {}
lines = []

with open(mapping_file, 'r') as myfile:
    lines = [line.rstrip() for line in myfile]

keys = [x.strip().lower().replace('/','_').replace(' ','_') for x in lines[0].split('\t')]

for line in lines[1:]:
    values = [x.strip().lower().replace('/','_') for x in line.split('\t')]
    if not values[0] in mapping_data:
        row = dict(zip(keys, values))
        mapping_data[values[0]] = row

if not 'mapping' in data:
    data['mapping'] = {}

data['mapping']['types'] = mapping_data
data['mapping']['fields'] = {'name': 'name', 'type': 'type', 'length': 'length'}
save_pickle_data(data, pickle_file)