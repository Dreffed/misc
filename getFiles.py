import os
import sys
import stat
import time
import pickle
import hashlib
import json
from datetime import datetime
from os import scandir
import logging
from logging.config import fileConfig

try:
    fileConfig('logging_config.ini')
except:
    print("No Logging config file found")

logger = logging.getLogger(__name__)

def load_pickle(picklename):
    data = {}
    if os.path.exists(picklename):
        logger.info('Loading Saved Data... [%s]' % picklename)
        with open(picklename, 'rb') as handle:
            data = pickle.load(handle)
    return data

def save_pickle(data, picklename):
    logger.info('Saving Data... [%s]' % picklename)
    with open(picklename, 'wb') as handle:
        pickle.dump(data, handle)

def open_json(file_name=r"settings.json"):
    # Load credentials from json file
    data = None
    if os.path.exists(file_name):
        logger.info('Loading Saved Data... [%s]' % file_name)
        with open(file_name, "r") as file:  
            data = json.load(file)
    return data

def save_json(data = {}, file_name=r"settings.json"):
    # Save the credentials object to file
    logger.info('Saving Data... [%s]' % file_name)
    with open(file_name, "w") as file:  
        file.write(json.dumps(data, indent = 4)) 

def export_file(copy_files, archive_path):
    import socket
    import shutil
    hostname = socket.gethostname()

    for filename in copy_files:
        name, ext = os.path.splitext(filename)
        newname = '{}.{}.{}'.format(name, hostname, ext)
        dstpath = os.path.join(archive_path, newname)
        i = 0
        while True:
            if not os.path.exists(dstpath):
                break

            i+=1
            newname = '{}.{}.({}).{}'.format(name, hostname, i, ext)
            dstpath = os.path.join(archive_path, newname)

        shutil.copy(filename, dstpath)

def get_stat(entry):
    time_format = "%Y-%m-%d %H:%M:%S"

    f = {
        "file":entry.name,
        "folder":os.path.split(os.path.abspath(entry.path))[0],
        "inode":entry.inode()
    }
    
    # get the stats
    # os.stat_result(
    #	st_mode=33206, 
    #	st_ino=0, 
    #	st_dev=0, 
    #	st_nlink=0, 
    #	st_uid=0, 
    #	st_gid=0, 
    #	st_size=92702, 
    #	st_atime=1543724526, 
    #	st_mtime=1523310306, 
    #	st_ctime=1523310474)
    f["accessed"] = time.strftime(time_format,time.localtime(entry.stat().st_atime))
    f["modified"] = time.strftime(time_format,time.localtime(entry.stat().st_mtime))
    f["created"] = time.strftime(time_format,time.localtime(entry.stat().st_ctime))
    f["size"] = entry.stat().st_size
    f["mode"] = entry.stat().st_mode
    return f
    
def scantree(path):
    """Recursively yield DirEntry objects for given directory."""
    
    for entry in scandir(path):
        try:
            if entry.is_dir(follow_symlinks=False):
                yield from scantree(entry.path)  # see below for Python 2.x
            else:
                yield get_stat(entry)
        
        except Exception as ex:
            logger.error(ex)

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

def scan_folders(folder, hash_list = None):
    """ will take the supplied path, use scanFiles to get a yeild of files
    It will check to see if the file is already scanned, if it is not or 
    it is updated it will get the hash
        folder is of the form:
            {
                "name": "...", 
                "root": "...", 
                "folders": ["...".."...",...]},
    """
    data = {}
    picklename = '{}.pickle'.format(folder.get("name","files"))
    data = load_pickle(picklename=picklename)

    file_details = data.get('biblo',{})
    file_scans = data.get('scans',[])

    # get the file list, check if files have been updated...
    new_file_list = []
    folder_path = os.path.expanduser(os.path.join(folder.get("root"), *folder.get("folders",[])))
    logger.debug(folder_path)

    for i, file_item in enumerate(scantree(folder_path)):
        # check if we have the file?
        filename = file_item.get("file")
        if filename in file_details:
            # do we have the current file here too
            found = False

            for f in file_details.get(filename, []):
                # compare file data....
                if f.get("folder") == file_item.get("folder") \
                    and f.get("file") == file_item.get("file"):
                    found = True

                    if f.get("size") != file_item.get("size") or \
                        f.get("modified") != file_item.get("modified"):
                        f = file_item
                        new_file_list.append(file_item) 

                    break

            if not found:
                new_file_list.append(file_item)
                file_details[filename].append(file_item)   

        else:
            file_details[filename] = []
            file_details[filename].append(file_item)  
            new_file_list.append(file_item)    

        if i % 1000 == 0:
            logger.info("Scanned {}: Found: {} new / updated files".format(i, len(new_file_list)))

    # add the scan with the new files...
    if len(new_file_list) > 0:
        file_scans.append({
            "scan":datetime.now().strftime("%Y-%m-%d %H:%M%S"),
            "files":new_file_list
        })

    data['scans'] = file_scans
    data['biblo'] = file_details

    logger.info('Found {} files'.format(len(new_file_list)))

    save_pickle(data=data, picklename=picklename)
    return data

def update_hashes(data, name, hash_list=None):
    """This is scan the biblo and generate the hashes if
    there are missing and if the ext is in the hash_list"""

    picklename = '{}.pickle'.format(name)
    
    duplicates = 0
    completed = 0
    zeros = 0
    start_time = time.time()
    snap_time = time.time()

    # calc SHA Hassh on file...
    if not hash_list:
        hash_list = []

    file_hashes = data.get('file_hashes',{})

    for k, v in  data.get('biblo',{}).items():
        _, ext = os.path.splitext(k)

        if len(hash_list) > 0 and ext not in hash_list:
            continue

        for f in v:
            if f['size'] == 0:
                zeros += 1
                continue

            if f.get("hashes"):
                # we have the hash already saved skip
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
                logger.info('\t{} ({} Dups {} Zeros) over {}'.format(completed, duplicates, zeros, elapsed_time))

            file_hashes[sha_hash].append(f)

    data['file_hashes'] = file_hashes
    save_pickle(data=data, picklename=picklename)

    logger.info('Found {} unique hashes, {} duplicates'.format(len(file_hashes), duplicates))
    return data

if __name__ == '__main__':
    config_path = 'getfiles_settings.json'
    config_data = {}

    if os.path.exists(config_path):
        config_data = json.load(open(config_path))

    else:
        config_data['folders'] = [
            {
                'name': 'root', 
                'root': '/',
                'folders':[]
            }
        ]
        with open(config_path, 'w') as outfile:
            json.dump(config_data, outfile)

    folders = config_data.get('folders')
    hash_list = config_data.get('hashlist', [])
    picklename = config_data.get('picklename','get_files.pickle')
    copy_files = []
    copy_files.append(picklename)

    data = load_pickle(picklename=picklename)
    for item in folders:
        logger.info('Scanning...\n\t{} -> {} : {} '.format(item.get('name'), item.get('root'), item.get('folders')))
        copy_files.append("{}.pickle".format(item.get('name')))

        data[item.get('name')] = scan_folders(folder=item, hash_list=hash_list)
        #data[item.get('name')] = update_hashes(data=data[item.get('name')], name=item.get('name'), hash_list=hash_list)
        file_name = "get_files_{}.json".format(item.get('name'))
        save_json(file_name=file_name, data=data[item.get('name')])

    save_pickle(data=data, picklename=picklename)