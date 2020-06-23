from PyPDF2 import PdfFileReader

def get_pdf_info(path):
    """This will return the doc info infomation from the 
    Named file."""
    data = {}
    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)
        cp = pdf.getDocumentInfo()
    
    if cp:
        # get the core properties from the file...
        data['author'] = cp.author
        data['creator'] = cp.creator
        data['producer'] = cp.producer
        data['subject'] = cp.subject
        data['title'] = cp.title
    
    return data
