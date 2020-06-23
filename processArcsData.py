from json import load, dump, dumps
import os
import logging
import re
import pandas as pd 

from logging.config import fileConfig
import openpyxl

fileConfig('logging_config.ini')
logger = logging.getLogger(__name__)


config = {
    "files": [
        {
            "purpose": "input",
            "name": "arcsdata",
            "ext": "json"
        },
        {
            "purpose": "output",
            "name": "DeliverableNotesDocManagement",
            "ext": "xlsx",
            "folders": ["Google Drive (david.gloyn-cox@thoughtswinsystems.com)", "BCFSA"],
            "root": "~",
            "config":{
                "ARCS":{
                    "Primary": {
                        "sheet": "ARCS - Primaries",
                        "range": "TBL_ARCS_P",
                        "cols": [
                            {
                                "name": "IDX",
                                "src": {
                                    "field": "title",
                                    "regex": r"^[\d]+"
                                }
                            },
                            {
                                "name": "Business Function",
                                "src": {}
                            },
                            {
                                "name": "Primary",
                                "src": {
                                    "field": "title",
                                    "regex": "^[\d]+[ -](.*) - Province of British Columbia"
                                }
                            },
                            {
                                "name": "Notes",
                                "src": {
                                    "field": "text"
                                }
                            }
                        ]
                    }
                }
            }
        }
    ]
}

def load_json(filepath):
    """Will load the file and return a data object
    if file is missing it will return a None"""
    data = None
    logger.info("Found {} \n\t{}".format(filepath, os.path.exists(filepath)))

    if os.path.exists(filepath):
        logger.info("loading file...")
        # Load credentials from json file

        with open(filepath, encoding="utf-8") as f:  
            data = load(f)

    return data

def main():

    sources = config.get("files")

    if len(sources) > 0:
        for f in sources:
            root = f.get("root", os.getcwd() )
            folders = f.get("folders", [])
            name = f.get("name")
            ext = f.get("ext")

            if f.get("purpose") == "input":
                input_file = os.path.expanduser(os.path.join(root, *folders, "{}.{}".format(name, ext)))
                input_config = f.get("config", {})
            
            if f.get("purpose") == "output":
                output_file = os.path.expanduser(os.path.join(root, *folders, "{}.{}".format(name, ext)))
                output_config = f.get("config", {})

        logger.info("input file: {}".format(input_file))
        logger.info("output file: {}".format(output_file))

        src_data = load_json(input_file)

    # process the data
    regex = re.compile(r'(\d+)[ -]+(.*) -')
    if src_data:
        primaries = []
        secondaries = []
        for item in src_data:
            logger.info("\t{}".format(item.get("title")))
            header = item.get("title")
            m = regex.match(header)
            if m:
                idx = m.group(1)
                title = m.group(2)
                primaries.append(
                    {
                        "idx": int(idx),
                        "primary": title,
                        "notes": item.get("text")
                    }
                )

            # process the data elements
            for row in item.get('data', []):
                text = row.get("text")
                notes = row.get("text")
                lines = text.splitlines()
                if len(lines) > 0:
                    text = lines[0]

                    notes = "\n".join(lines[1:])

                secondaries.append({
                    "idx": row.get("series"),
                    "pidx": int(idx),
                    "primary": title,
                    "Secondary": text,
                    "a": row.get("a"),
                    "sa": row.get("sa"),
                    "fd": row.get("fd"),
                    "notes": notes
                })

        logger.info("added {} primaries".format(len(primaries)))
        logger.info("added {} secondaries".format(len(secondaries)))
        df_prim = pd.DataFrame.from_dict(primaries)
        df_sec = pd.DataFrame.from_dict(secondaries)

        df_prim.to_excel("primaries.xlsx")
        df_sec.to_excel("secondaries.xlsx")

if __name__ == "__main__":
    main()