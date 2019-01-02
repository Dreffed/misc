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
---
* process
	* folders
		* the folder scanned as root
	* filter
		* the filter (file extension) to match
	* files
		* an array of files
	* hashes
		* a dict of files hashes

* hash
	* an array of filepath that have the same hash
	* filepath
		* the normalized filepath

* file
	* name
	* title
	* description
	* keywords
	* subject
	* manager
	* category
	* pagecount
	* creator
	* created
	* saved
	* pages
		* array of page objects
	* folder
	* file
	* modified
	* accessed
	* size
	* hash
		* a dict of sha1 and md5 hashes for the current file, used to check changes

* page

	* name
		*  	the name of the page 
	* shape_count
		* the number of shapes on the page
	* objects
		* a dict of object, index by <shape type>

* object
	* <shape type>	
		* a dict of shapes index by the shape type
		* <shape name>	
			* dict of shapes, index by name

* shape
	* id
	* name
	* type
	* text
	* name_type
	* subid
	* callouts
	* connected_shapes
	* connects
	* containing_shape
	* contained_shapes
---

