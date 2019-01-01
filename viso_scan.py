from getFiles import scanFiles, get_info, get_pickle_data, save_pickle_data
import sys
import win32com.client
import os
import json
from datetime import datetime
from dateutil.parser import parse

def load_config(config_path):
    if os.path.exists(config_path):
        cnf_data = json.load(open(config_path))
    else:
        cnf_data = {}
        cnf_data['folders'] = [os.path.curdir]
        cnf_data['filter'] = '*.vsdx'

        with open(config_path, 'w') as outfile:
            json.dump(cnf_data, outfile)
    return cnf_data

def process_shape(shape):
    shape_data = {}
    shape_data['id'] = shape.ID 

    shape_data['name'] = str(shape.Name)
    shape_data['type'] = str(shape.Type)
    shape_data['Text'] = shape.Text

    shape_dets = str(shape.Name).split(".")
    shape_data['name_type'] = shape_dets[0]
    if len(shape_dets) <= 1:
        shape_data['subid'] = '0'
    else:
        shape_data['subid'] = shape_dets[1]

    shape_data['callouts'] = shape.CalloutsAssociated
    if not shape_data['name_type'] == 'Dynamic connector':
        shape_data['connected_shapes'] = shape.ConnectedShapes(0, "")
    #else:
    connected_shapes = shape.connects
    if len(connected_shapes) > 0:
        shape_data['connects'] = []
        for connector in connected_shapes:
            if connector.FromSheet.Id == shape_data['id']:
                shape_data['connects'].append({"type": "from", "id": connector.ToSheet.Id})
            else:
                shape_data['connects'].append({"type": "to", "id": connector.FromSheet.Id})
        print('{} -> {}'.format(shape_data['id'], shape_data['connects']))

    contained_in = shape.ContainingShape
    shape_data['containing_shape'] = contained_in.Name

    shape_members = shape.ContainerProperties
    if shape_members is not None:
        shape_data['contained_shapes'] = shape_members.GetMemberShapes(16)

    return shape_data

def process_visiofile(filepath):
    dwg_file = {}
    try:
        visio = win32com.client.Dispatch("Visio.Application")
        visio.Visible = 0
        dwg = visio.Documents.Open(filepath)

        try:
            pages = dwg.Pages
            dwg_file['name'] = dwg.Name
            dwg_file['title'] = dwg.Title  
            dwg_file['creator'] = dwg.Creator  
            dwg_file['description'] = dwg.Description  
            dwg_file['keywords'] = dwg.Keywords  
            dwg_file['subject'] = dwg.Subject  
            dwg_file['manager'] = dwg.Manager  
            dwg_file['category'] = dwg.Category 
            dwg_file['pagecount'] = len(pages)
            dwg_file['creator'] = dwg.Creator
            dwg_file['created'] = parse(str(dwg.TimeCreated))
            dwg_file['Saved'] = parse(str(dwg.TimeSaved))
            dwg_file['pages'] = []

            for pg in pages:
                shapes = pg.Shapes
                page_data = {}
                page_data['name'] = pg.Name
                
                page_data['shape_count'] = len(shapes)
                page_data['objects'] = {}

                for shape in shapes:
                    try:
                        shape_data = process_shape(shape)
                        shape_type = shape_data['name_type']
                        
                        if not shape_type in page_data['objects']:
                            page_data['objects'][shape_type] = {}
                        page_data['objects'][shape_type][shape.Name] = shape_data

                    except Exception as ex:
                        print("\t{} [{}]\n\t\tError {}".format(shape.Name, shape.Type, ex))

                dwg_file['pages'].append(page_data)
                
        except Exception as e:
            print("Error {}".format(e))

        dwg.Close()

    except Exception as e:
        print("Error opening file {}".format(e))
    finally:
        visio.Quit()

    return dwg_file

config_path = 'visio_settings.json'
pickle_file = 'visio_data.pickle'
cnf_data = load_config(config_path)

path = cnf_data['folders']
filepath = os.path.join(*path)
filepath = os.path.expanduser(filepath)
print(filepath)

if not os.path.exists(filepath):
    raise 'missing path'

data = {}
data['folders'] = path
data['files'] = []

for f in scanFiles(filepath):
    filename, file_extension = os.path.splitext(f['file']) 
    if file_extension == cnf_data['filter']:
        print(f, filename, file_extension)
        f_path = os.path.join(f['folder'], f['file'])
        dwg_file = process_visiofile(f_path)

        # add the file details...
        dwg_file['folder'] = f['folder']
        dwg_file['file'] = f['file']
        dwg_file['modified'] = parse(f['modified'])
        dwg_file['accessed'] = parse(f['accessed'])
        dwg_file['size'] = f['size']

        data['files'].append(dwg_file)

save_pickle_data(data, pickle_file)
