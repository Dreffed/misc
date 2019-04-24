from getFiles import scanFiles, get_info, get_pickle_data, save_pickle_data
from collections import defaultdict
import os
import logging
from logging.config import fileConfig

fileConfig('logging_config.ini')
logger = logging.getLogger(__name__)

files_found = 0
pickleName = "{}.pickle".format("scan_files")
data = get_pickle_data(pickleName=pickleName)

if not data.get("extension"):
    data_ext = defaultdict(list)
    data_files = defaultdict(list)

    for f in scanFiles('c:\\'):
        files_found += 1
        filename, file_extension = os.path.splitext(f['file']) 
        data_files[f['file']].append(f)
        data_ext[file_extension].append(f)

    logger.info("files scanned:{}".format(files_found))

    data = {}
    data['extension'] = data_ext
    data['files'] = data_files

    save_pickle_data(data=data, pickleName=pickleName)
    logger.info("Data Saved:{}".format(pickleName))

# display infor about the files...
for k,v in data.get("extension", {}).items():
    logger.info("\t{} => {}".format(k, len(v)))

