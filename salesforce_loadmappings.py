mapping_file = 'salesforce_mapping.txt'

mapping_data = {}
lines = []
with open(mapping_file, 'r') as myfile:
    lines = myfile.readlines()

for line in lines:
    print(line)