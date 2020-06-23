import openpyxl

def get_excel_info(path):
    """This will return the doc info infomation from the 
    Named file."""
    data = {}
    try:
        doc = openpyxl.load_workbook(path)

        # get the core properties from the file...
        # https://python-docx.readthedocs.io/en/latest/api/document.html#coreproperties-objects
        cp = doc.properties

        data['author'] = cp.creator
        data['category'] = cp.category
        data['comments'] = cp.description
        data['created'] = cp.created
        data['identifier'] = cp.identifier
        data['keywords'] = cp.keywords
        data['language'] = cp.language
        data['last_modified_by'] = cp.lastModifiedBy
        data['last_printed'] = cp.lastPrinted
        data['modified'] = cp.modified
        data['revision'] = cp.revision
        data['subject'] = cp.subject
        data['title'] = cp.title
        data['version'] = cp.version
    except Exception as ex:
        print("ERROR: {}\n\t>>>{}".format(path,ex))
    return data
