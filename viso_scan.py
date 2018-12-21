from getFiles import scanFiles, get_info, get_pickle_data, save_pickle_data
import sys
import win32com.client
import os
import json

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

def process_visiofile(filepath):
    dwg_file = {}
    try:
        visio = win32com.client.Dispatch("Visio.Application")
        visio.Visible = 0
        dwg = visio.Documents.Open(filepath)

        try:
            pages = dwg.Pages
            dwg_file['name'] = dwg.Name
            dwg_file['pages'] = len(pages)
            dwg_file['creator'] = dwg.Creator
            #dwg_file['created'] = dwg.TimeCreated
            #dwg_file['Saved'] = dwg.TimeSaved

            for pg in pages:
                shapes = pg.Shapes
                page_data = {}
                page_data['name'] = pg.Name
                page_data['shape_count'] = len(shapes)
                page_data['objects'] = {}

                for shape in shapes:
                    try:
                        shape_name = str(shape.Name)
                        shape_dets = shape_name.split(".")
                        contained_in = shape.ContainingShape
                        
                        if not shape_dets[0] in page_data['objects']:
                            page_data['objects'][shape_dets[0]] = {}

                        if len(shape_dets) > 1:
                            page_data['objects'][shape_dets[0]][shape_dets[1]] = {}
                            page_data['objects'][shape_dets[0]][shape_dets[1]]['Text'] = shape.Text
                            page_data['objects'][shape_dets[0]]['Containedin'] = contained_in.Name
                        else:
                            page_data['objects'][shape_dets[0]]['0'] = {}
                            page_data['objects'][shape_dets[0]]['0']['Text'] = shape.Text
                            page_data['objects'][shape_dets[0]]['0']['Containedin'] = contained_in.Name
                    except Exception as ex:
                        print("\t\t\tError {}".format(ex))

                dwg_file[pg.Name] = page_data
                
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
        #dwg_file['modified'] = f['modified']
        #dwg_file['accessed'] = f['accessed']
        dwg_file['size'] = f['size']

        data['files'].append(dwg_file)

save_pickle_data(data, pickle_file)
