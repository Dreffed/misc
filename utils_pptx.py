import pptx

def get_pptx_info(path):
    """This will return the doc info infomation from the 
    Named file."""
    data = {}
    doc = pptx.Presentation(path)
    
    # get the core properties from the file...
    # https://python-docx.readthedocs.io/en/latest/api/document.html#coreproperties-objects
    cp = doc.core_properties
    
    data['author'] = cp.author
    data['category'] = cp.category
    data['comments'] = cp.comments
    data['content_status'] = cp.content_status
    data['created'] = cp.created
    data['identifier'] = cp.identifier
    data['keywords'] = cp.keywords
    data['language'] = cp.language
    data['last_modified_by'] = cp.last_modified_by
    data['last_printed'] = cp.last_printed
    data['modified'] = cp.modified
    data['revision'] = cp.revision
    data['subject'] = cp.subject
    data['title'] = cp.title
    data['version'] = cp.version
    
    return data
