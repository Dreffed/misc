from getFiles import scanFiles, get_info, get_pickle_data, save_pickle_data
import os

for f in scanFiles('./'):

    filename, file_extension = os.path.splitext(f['file']) 
    if file_extension == '.pickle':
        print(f, filename, file_extension)
        data = get_pickle_data(f['file'])
        for item in data:
            print(item, len(data[item]))

        step = 1
        interval = len(data['files']) // 10
        for f in data['files']:
            step += 1
            #if step % interval == 0:
            #if 'thunderbird' in f['folder'].lower():
            if '.zip' in f['file'].lower():
                print(f)

