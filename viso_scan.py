import sys, win32com.client

doc = r"C:\opt\rm\Process Design\1. Cornelius Business Process Diagrams\Sales and Marketing\Sales and Marketing - Cornelius Business Process Design.vsdx"
try:
    visio = win32com.client.Dispatch("Visio.Application")
    visio.Visible = 0
    try:
        dwg = visio.Documents.Open(doc)
        print('\t{} -> {}'.format(dwg.TimeCreated, dwg.TimeSaved))
    except Exception as e:
        print("Error {}".format(e))
    dwg.Close()
    visio.Quit()
except Exception as e:
    print("Error opening file".format(e))