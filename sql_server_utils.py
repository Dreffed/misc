import json
import os

class SSDatatypes():
    def __init__(self, data_file_name = None):
        # load in the json file with the conversions...
        if not data_file_name:
            data_file_name = 'datatypes.json'

        data = {}
        if not os.path.exists(data_file_name):
            data['meta'] = {}
            data['meta']['classifiers'] = {}
            data['meta']['classifiers']['Numeric Exact'] = {'fields': ['min', 'max']}
            data['meta']['classifiers']['Numeric Aprox'] = {'fields': ['min', 'max', 'presicion']}
            data['meta']['classifiers']['Date'] = {'fields': ['precision']}
            data['meta']['classifiers']['Character'] = {'fields':['length', 'default', 'max']}
            data['meta']['classifiers']['Unicode'] = {'fields':['length', 'default', 'max']}
            data['meta']['classifiers']['Binary'] = {'fields':['length', 'max']}
            data['meta']['classifiers']['Other'] = {'fields':[]}

            types = []
            for t in data['meta']['classifiers']:
                row = {}
                row["classifier"] = t
                row["datatype"] = "<<please enter data type name>>"
                r = data['meta']['classifiers'][t]
                for f in r['fields']:
                    row[f] = ''

                types.append(row)

            data['types'] = types

            with open(data_file_name, 'w') as outfile:
                outfile.write(json.dumps(data, indent = 4))
        else:
            with open(data_file_name) as infile:
                data = json.loads(infile)
        
        print(json.dumps(data, indent=4))


class DB_Columns():
    def __init__(self, name = None, data_type = None, 
            length = None, source = 'SQLServer'
        ):
        """this will store the relevant column information, the class will
        convert to other types, and try to apply naming convention for the
        source"""

        self.name = name
        self.data_type = data_type
        self.length = length
        self.source = source

class SSTableSize():
    def __init__(self, num_rows = 1000,
            columns = []
        ):
        """"""
        pass
    
if __name__ == "__main__":
    obj = SSDatatypes()
