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

