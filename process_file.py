import os
import logging
from logging.config import fileConfig

fileConfig('logging_config.ini')
logger = logging.getLogger(__name__)

def process_line(line):
    print(len(line))

f_loc = ['~',
    'Google Drive',
    'Rocky Mountaineer',
    'SFDC',
    'day_20190912_091314-982b8a-700130.sql']
file_name = os.path.expanduser( os.path.join(*f_loc))

print(file_name)
with open(file_name) as f:
    for line in f:
        process_line(line)
