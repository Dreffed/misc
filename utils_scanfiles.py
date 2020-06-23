# utils_files.py

try:
    from os import scandir
except ImportError:
    from scandir import scandir  # use scandir PyPI module on Python < 3.5
import stat
import time
import os
import logging

logger = logging.getLogger(__name__)

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

if __name__ == "__main__":
    for f in scantree("."):
        print(f)   