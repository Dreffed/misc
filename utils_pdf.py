from PyPDF2 import PdfFileReader
import pdfplumber

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
"""
def get_pdf_text(path):
    data = []
    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)
        
        try:
            for i in range(0,pdf.getNumPages()):
                pdf_page = pdf.getPage(0)
                strs = pdf_page.extractText()
                if strs:
                    data.append(strs)
        except Exception as ex:
            print("ERROR: {}\n\t{}".format(path, ex))
        
    return data

"""
def get_pdf_text(path):
    data = []
    with pdfplumber.open(path) as pdf:
        for p in pdf.pages:
            data.append(p.extract_text())
    return data