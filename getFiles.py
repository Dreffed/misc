import os
import sys
import stat
import time
import pickle
import hashlib

def get_pickle_data(pickleName):
    data = {}
    if os.path.exists(pickleName):
        print('Loading Saved Data... [%s]' % pickleName)
        with open(pickleName, 'rb') as handle:
            data = pickle.load(handle)
    return data

def save_pickle_data(data, pickleName):
    print('Saving Data... [%s]' % pickleName)
    with open(pickleName, 'wb') as handle:
        pickle.dump(data, handle)
        
def get_info(filepath):
    time_format = "%Y-%m-%d %H:%M:%S"
    try:
        file_stats = os.stat(filepath)
        modification_time = time.strftime(time_format,time.localtime(file_stats[stat.ST_MTIME]))
        access_time = time.strftime(time_format,time.localtime(file_stats[stat.ST_ATIME]))
        file_size = file_stats[stat.ST_SIZE]

    except:
        modification_time, access_time, file_size = ["","",0]

    return modification_time, access_time, file_size

def scanFiles(folder):
    """ This method will recursively scan the specified folder and add records if neccessary"""
 
    for dirpath, _, filenames in os.walk(folder):
        for filename in filenames:
            filepath = os.path.join(dirpath,filename)

            try:
                mTime, aTime, fSize = get_info(filepath)
                # save the format
                data = {
                    "folder" : dirpath, 
                    "file" : filename, 
                    "modified" : mTime, 
                    "accessed" : aTime, 
                    "size" : fSize
                }
                yield data

            except Exception as e:
                print("Error: scanning file stats - {}".format(e))

def make_hash(file_path):
    hashes = {}
    #print('[{}]'.format(file_path))

    # BUF_SIZE is totally arbitrary, change for your app!
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    try:
        if os.path.exists(file_path):
            #print('{}'.format(file_path))
            with open(file_path, 'rb') as f:
                while True:
                    d = f.read(BUF_SIZE)
                    if not d:
                        break
                    md5.update(d)
                    sha1.update(d)

            hashes['MD5'] = md5.hexdigest()
            hashes['SHA1'] = sha1.hexdigest()
        else:
            hashes['MD5'] = 'Missing file'
            hashes['SHA1'] = 'Missing file'
    except Exception as e:
        print('ERROR: [{}]\n{}'.format(file_path,e))
        
        hashes['MD5'] = 'ERROR'
        hashes['SHA1'] = 'ERROR'

    return hashes

def scan_folders(folder, root_name):
    data = {}
    picklename = '{}.pickle'.format(root_name)
    data = get_pickle_data(picklename)

    file_list = []
    if 'files' in data:
        file_list = data['files']
    else:
        for file_item in scanFiles(folder):
            file_list.append(file_item)

        data['files'] = file_list    
        save_pickle_data(data, picklename)

    print('Found {} files'.format(len(data['files'])))

    # sort the files...
    file_details = {}
    if 'biblo' in data:
        file_details = data['biblo']
    else:
        for file_item in file_list:
            file_name = file_item['file']
            if file_name not in file_details:
                file_details[file_name] = {}
                file_details[file_name]['paths'] = []
                file_details[file_name]['files'] = []

            file_details[file_name]['paths'].append(file_item['folder'])
            file_details[file_name]['files'].append(file_item)

        data['biblo'] = file_details
        save_pickle_data(data, picklename)

    print('Found {} unique files.'.format(len(file_details)))

    file_hashes = {}
    duplicates = 0
    completed = 0
    zeros = 0
    start_time = time.time()
    snap_time = time.time()

    # calc SHA Hassh on file...
    if 'file_hashes' in data:
        file_hashes = data['file_hashes']
    else:
        for file_name in file_details:
            file_item = file_details[file_name]
            for f in file_item['files']:
                if f['size'] == 0:
                    zeros += 1
                    continue
                
                f_path = os.path.join(f['folder'], f['file'])
                hashes = make_hash(f_path)
                sha_hash = '{}'.format(hashes['SHA1'])
            
                completed += 1
                elapsed_time = time.time() - start_time
                if sha_hash not in file_hashes:
                    file_hashes[sha_hash] = []
                else:
                    duplicates += 1
                
                if completed % 1000 == 0 or (time.time() - snap_time) > 300:
                    snap_time = time.time()
                    print('\t{} ({} Dups {} Zeros) of {} over {}'.format(completed, duplicates, zeros, len(file_list), elapsed_time))

                file_hashes[sha_hash].append(f)

        data['file_hashes'] = file_hashes
        save_pickle_data(data, picklename)

    print('Found {} unique hashes, {} duplicates'.format(len(file_hashes), duplicates))

if __name__ == '__main__':
    folders = [
        {
            'root_name': 'TB_1', 
            'folder':'/'
        }
    ]

    for item in folders:
        print('Scanning...\n\t{} -> {}'.format(item['root_name'], item['folder']))
        scan_folders(item['folder'], item['root_name'])
