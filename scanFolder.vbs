' VBS script to enumerate folder and files and extract data
' @author: David Gloyn-Cox
' Operation: set the folders to scan in the Line 21 - 22, remember to update tthe array length
' Run the script, output a file called filelist.csv
on error resume next

' global objects - gah
Dim objFSO, stdOut, stdErr
Set objFSO = CreateObject("Scripting.FileSystemObject")
Set stdOut = objFSO.GetStandardStream (1)
Set stdErr = objFSO.GetStandardStream (2)

Dim objFolder
Dim idx
idx = CLng(0)

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
' VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV
' SET THE LIST OF FOLDER TO SCAN HERE
' change the number (n-1) to reflect the number of base folders to scan recursively
Dim varFolders(1) ' n-1, if 'n' folders the length is (n-1)
varFolders(0) = "O:\"
varFolders(1) = "P:\"
' ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
' what fields to export to CSV file
Dim arrFieldFolder(3)
Dim arrFieldFile(5)
arrFieldFolder(0) = "Path"
arrFieldFolder(1) = "Name"
arrFieldFolder(2) = "Type"
arrFieldFolder(3) = "Created"

arrFieldFile(0) = "Name"
arrFieldFile(1) = "Size"
arrFieldFile(2) = "Created"
arrFieldFile(3) = "Modified"
arrFieldFile(4) = "Type"
arrFieldFile(5) = "Ext"

Dim OUTPUT_FILE
OUTPUT_FILE = "filelist.csv"
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
' init the csv file
initCSVFile OUTPUT_FILE

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
' launch and load the script
for each strFolder in varFolders
    Set objFolder = objFSO.GetFolder(strFolder)
    if Not objFolder is Nothing then
        scanFiles (objFolder)
    else
        stdOut.writeLine strFolder + " could not be found!"
    end if
next

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
' Scan the specified folder for folders and files
Sub scanFiles(objFolder)
    Dim objFolderDict, objFile
    
    ' outpuit location... 
    Set objFolderDict = getSysDataFolder(objFolder)

    ' walk the child folders
    for each objSubFolder in objFolder.SubFolders
        scanFiles (objSubFolder)
    next

    ' enumerate the files
    Set objFiiles  = objFolder.files

    for each objFile in objFiiles
        ' get the file details 
        Set objFileDict = getSysDataFile(objFile)

        ' dump the row out
        writeCSVRow OUTPUT_FILE, objFolderDict, objFileDict

    next
end Sub

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
' returns the folders properties
Function getSysDataFolder(objFolder)
    Dim objDict
    Set objDict = CreateObject("Scripting.Dictionary")

    ' add the folder detaisl to this doct
    objDict.add "Path", objFolder.Path
    objDict.add "Name", objFolder.Name
    objDict.add "Attributes", objFolder.Attributes
    objDict.add "Created", objFolder.DateCreated
    objDict.add "Modified", objFolder.DateLastModified
    objDict.add "Drive", objFolder.Drive
    objDict.add "ShortName", objFolder.ShortName
    objDict.add "ShortPath", objFolder.ShortPath
    objDict.add "Type", objFolder.Type

    ' return the object
    Set getSysDataFolder = objDict
end Function

' returns the files properties
Function getSysDataFile(objFile)
    Dim objDict
    Set objDict = CreateObject("Scripting.Dictionary")

    ' now to set the dict with the corrent values...
    objDict.add "Path", objFile.Path
    objDict.add "Name", objFile.Name
    objDict.add "Ext", objFSO.getExtensionName(objFile)
    objDict.add "Attributes", objFile.Attributes
    objDict.add "Created", objFile.DateCreated
    objDict.add "Modified", objFile.DateLastModified
    objDict.add "Drive", objFile.Drive
    objDict.add "ShortName", objFile.ShortName
    objDict.add "ShortPath", objFile.ShortPath
    objDict.add "Size", objFile.Size
    objDict.add "Type", objFile.Type

    ' return the object
    Set getSysDataFile = objDict
end function

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
' csv tools
sub initCSVFile(filename)
    Dim objCSVFile
    Set objCSVFile = objFSO.OpenTextFile(filename, 8, True)

    objCSVFile.write "idx"
    for each strField in arrFieldFolder
        objCSVFile.write ",folder_" & strField
    next

    for each strField in arrFieldFile
        objCSVFile.write ",file_" & strField
    next
    objCSVFile.write vbCrLf

    objCSVFile.Close
    Set objCSVFile = Nothing
end sub

sub writeCSVRow(filename, ByRef objFolderDict, ByRef objFileDict)
    Dim objCSVFile
    Set objCSVFile = objFSO.OpenTextFile(filename, 8, True)

    idx = idx+1
    objCSVFile.write idx
    for each strField in arrFieldFolder
        objCSVFile.write ",""" & objFolderDict(strField) & """"
    next

    for each strField in arrFieldFile
        objCSVFile.write ",""" & objFILEDict(strField) & """"
    next
    objCSVFile.write vbCrLf

    ' close and save
    objCSVFile.Close
    Set objCSVFile = Nothing
end sub