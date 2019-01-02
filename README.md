# Misc

Miscellaneous files for various file operations

## Getting Started

set up the configuration files for each file...
* __init__.py
    * sets up the default logging for the module

* visio_scan.py
    * uses 
        * logging_config.ini
        * visio_setting.json
    * produces
        * visio_data.pickle
    * imports
        * from getFiles import scanFiles, get_info, get_pickle_data, save_pickle_data, make_hash
        * import sys
        * import win32com.client
        * import os
        * import json
        * from datetime import datetime
        * from dateutil.parser import parse
        * import logging
        * from logging.config import fileConfig
    * gotchas
        * will ponly run on machine able to run win32com
        
### Prerequisites

setting up *setting.json files

visio_setting.json
```
{
    "folders": [
        "~", <<folder names>>, <<...>>
        ], 
    "filter": "<<file extension include the period>>"
}
```

for logging.ini template see
https://docs.python-guide.org/writing/logging/

## Pickle file object

* structure of the viso_data.pickle file
```
{
	"folders": ["<<str>>","<<...>>"],
	"filter": ".<<file ext>>",
	"hashes": {
		"<<file sha1 hash>>": ["<<normalized file path>>","<<...>>"]
	},
	"archive": [{<<file obj>>},{...}],
	"files": [{<<file obj>>},{...}]
}
```

File Object
```
{
	"name": "<<name of the file>>",
	"title": "<<doc info title>>",
	"description": "<<doc info description>>",
	"keywords": "<<doc info keywords>>",
	"subject": "<<doc info subject>>",
	"manager": "<<doc info manager>>",
	"category": "<<doc info category of the file>>",
	"pagecount": "<<the number of pages in the file>>",
	"creator": "<<the name of the creator of the file>>",
	"created": "<<the date the file was created>>",
	"saved": "<<the save date of the file>>",
	"pages": [{"<<page object>>"}],
	"folder": "<<the folder the file is stored in>>",
	"file": "<<the file name>>",
	"modified": "<<OS date tge file was last modified>>",
	"accessed": "<<OS date the file was last accessed>>",
	"size": "<<fiel size in bytes>>",
	"hash": {
		"SHA1": "<<sha1 hash of the file>>",
		"MD5": "<<md5 hash of the file>>"
	}
}
```

Page object
```
{
	"name":	"<<the name of the page>>", 
	"shape_count":	<<the number of shapes on the page>>,
	"objects": {
		"<<shape type>>":{
			<<shape name>>: {<<shape object>>}
		}
	}
}
```

Shape object
```
{
	"id": <<shape id>>,
	"name": "<<name>>",
	"type": <<type constant>>,
	"text": "<<body>>",
	"name_type": "<<name prefix>>",
	"subid": "<<name suffix>>",
	"callouts": [<<shape ids>>, <<...>>],
	"connected_shapes": [<<shape ids>>, <<...>>],
	"connects": [<<shape ids>>, <<...>>],
	"containing_shape": <<shape id>>,
	"contained_shapes": [<<shape ids>>, <<...>>]
}
```
