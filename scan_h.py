import os
from getFiles import scan_folders
from utils import export_csv

folders = ['H:\\', 'IT', 'Projects', '2018', 'IT2018051 HRIS']
folder = os.path.join(*folders)

print('Scanning...\n\t{} -> {}'.format(folder, folders[-1]))
data = scan_folders(folder, folders[-1])

if len(data.get('files', [])) > 0:
    export_csv(data=data.get('files', []), filename ='filelist.csv')