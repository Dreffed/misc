import os
import sys
import stat
import time
import pickle
import hashlib
import json
from datetime import datetime
from utils import load_pickle, save_pickle
import logging
from logging.config import fileConfig

fileConfig('logging_config.ini')
logger = logging.getLogger(__name__)

def get_info(filepath):
    """ Scans the file and returns the access, mod and create time in a YYYY-MM-DD HH:MM:SS format"""
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
            _, ext = os.path.splitext(filename)
            try:
                m_time, a_time, f_size = get_info(filepath)
                # save the format
                data = {
                    "folder" : dirpath, 
                    "file" : filename, 
                    "ext": ext,
                    "modified" : m_time, 
                    "accessed" : a_time, 
                    "size" : f_size
                }
                yield data

            except Exception as e:
                logger.error("Error: scanning file stats - {}".format(e))

def make_hash(file_path):
    """ Will hash the files for both MD5 and SHA1 and return a dict of the hashes"""
    hashes = {}
    #print('[{}]'.format(file_path))

    # BUF_SIZE is totally arbitrary, change for your app!
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    try:
        if os.path.exists(file_path):
            logger.debug('{}'.format(file_path))
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
        logger.error('ERROR: [{}]\n{}'.format(file_path,e))
        
        hashes['MD5'] = 'ERROR'
        hashes['SHA1'] = 'ERROR'

    return hashes

def scan_folders(folder, root_name):
    """ will take the supplied path, use scanFiles to get a yeild of files
    It will check to see if the file is already scanned, if it is not or 
    it is updated it will get the hash
    """
    data = {}
    picklename = '{}.pickle'.format(root_name)
    data = load_pickle(picklename=picklename)

    file_list = data.get('files',[])
    file_details = data.get('biblo',{})
    file_hashes = data.get('file_hashes',{})
    file_scans = data.get('scans',[])

    new_file_list = []
    for file_item in scanFiles(folder):
        # check if we have the file?
        filename = file_item.get("file")
        if filename in file_details:
            # do we have the current file here too
            found = False
            for f in file_details.get(filename, {}).get("files",[]):
                # compare file data....
                if f.get("folder") == file_item.get("folder") \
                    and f.get("file") == file_item.get("file") \
                    and f.get("size") == file_item.get("size"):
                    found = True
                    break

            if found:
                if len(new_file_list) % 1000 ==0:
                    logger.debug("found: {} new / updated files".format(len(new_file_list)))

                file_list.append(file_item)    
                new_file_list.append(file_item)    

        else:
            file_list.append(file_item)    
            new_file_list.append(file_item)    

    if len(new_file_list) > 0:
        file_scans.append({
            "scan":datetime.now().strftime("%Y-%m-%d %H:%M%S"),
            "files":new_file_list
        })

    data['scans'] = file_scans 
    data['files'] = file_list    
    save_pickle(data=data, picklename=picklename)

    logger.info('Found {} files'.format(len(new_file_list)))

    # sort the files...
    for file_item in new_file_list:
        file_name = file_item['file']
        if file_name not in file_details:
            file_details[file_name] = {}
            file_details[file_name]['paths'] = []
            file_details[file_name]['files'] = []

        file_details[file_name]['paths'].append(file_item['folder'])
        file_details[file_name]['files'].append(file_item)

    data['biblo'] = file_details
    save_pickle(data=data, picklename=picklename)

    logger.info('Found {} unique files.'.format(len(file_details)))

    duplicates = 0
    completed = 0
    zeros = 0
    start_time = time.time()
    snap_time = time.time()

    # calc SHA Hassh on file...
    for file_name in file_details:
        file_item = file_details[file_name]
        for f in file_item.get('files',[]):
            if f['size'] == 0:
                zeros += 1
                continue
            
            if f.get("hashes"):
                # we have the hash alreqady saved skipp
                continue

            f_path = os.path.join(f['folder'], f['file'])
            hashes = make_hash(f_path)
            f["hashes"] = hashes

            sha_hash = '{}'.format(hashes['SHA1'])
        
            completed += 1
            elapsed_time = time.time() - start_time
            if sha_hash not in file_hashes:
                file_hashes[sha_hash] = []
            else:
                duplicates += 1
            
            if completed % 1000 == 0 or (time.time() - snap_time) > 300:
                snap_time = time.time()
                logger.info('\t{} ({} Dups {} Zeros) of {} over {}'.format(completed, duplicates, zeros, len(file_list), elapsed_time))

            file_hashes[sha_hash].append(f)

        data['file_hashes'] = file_hashes
        save_pickle(data=data, picklename=picklename)

    logger.info('Found {} unique hashes, {} duplicates'.format(len(file_hashes), duplicates))
    return data

if __name__ == '__main__':
    config_path = 'getfiles_settings.json'
    folder_cnf_data = {}

    if os.path.exists(config_path):
        folder_cnf_data = json.load(open(config_path))

    else:
        folder_cnf_data['folders'] = [
            {
                'root_name': 'root', 
                'folder':'/'
            }
        ]
        with open(config_path, 'w') as outfile:
            json.dump(folder_cnf_data, outfile)
    folders = folder_cnf_data.get('folders')

    data = load_pickle(picklename=folder_cnf_data.get('picklename','get_files.pickle'))
    for item in folders:
        logger.info('Scanning...\n\t{} -> {}'.format(item.get('root_name'), item.get('folder')))
        data[item.get('root_name')]= scan_folders(item.get('folder'), item.get('root_name'))
    save_pickle(data=data, picklename=folder_cnf_data.get('picklename','get_files.pickle'))
