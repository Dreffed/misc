from utils_files import scan_files
import os

root = 'D:\\'
folders = ['Data']
folder_path = os.path.expanduser(os.path.join(root, *folders))

print(folder_path)

found_files = []

for f in scan_files(folder_path):
    if f.get('ext') == '.pbix':
        found_files.append(f)
        print(f)

print('Found: {}'.format(len(found_files)))


