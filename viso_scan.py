import sys
import win32com.client
import os

path = ['~']
filename = '*.vsdx'

path.append(filename)

filepath = os.path.join(*path)
filepath = os.path.expanduser(filepath)
print(filepath)

try:
    visio = win32com.client.Dispatch("Visio.Application")
    visio.Visible = 0
    try:
        dwg = visio.Documents.Open(filepath)
        pages = dwg.Pages
        print("{}\t[{}]".format(dwg.Name, len(pages)))
        print('\t{}'.format(dwg.Creator))
        print('\t{} -> {}'.format(dwg.TimeCreated, dwg.TimeSaved))
        for pg in pages:
            shapes = pg.Shapes
            print("\t\t{} [{}]".format(pg.Name, len(shapes)))
            for shape in shapes:
                try:
                    m_shape = shape.Master
                    #print("\t\t\t[{} [{}]: {}\n\t\t\t\t|{} : {} <<<{}>>>]".format(shape.Name, shape.Type, m_shape, shape.Style, shape.TextStyle, shape.Text))
                    print("\t\t\t{} <<<{}>>>]".format(shape.Name, shape.Text))
                except Exception as ex:
                    print("\t\t\tError {}".format(ex))

    except Exception as e:
        print("Error {}".format(e))
    dwg.Close()
    visio.Quit()
except Exception as e:
    print("Error opening file {}".format(e))