import pyodbc
import json

# Load credentials from json file
with open("azure_db._settings.json", "r") as file:  
    creds = json.load(file)
    
server = creds['server']
database = creds['database']
username = creds['username']
password = creds['password']
port = creds['port']
driver = creds['driver']

conn_str = "'DRIVER='{}';SERVER='{}';PORT='{}';DATABASE='{}';UID='{}';PWD='{}'".format(driver, server, port, database, username, password)
print(conn_str)

cnxn = pyodbc.connect(conn_str)
cursor = cnxn.cursor()
cursor.execute("SELECT * FROM INFORMATION_SCHEMA.tables")
row = cursor.fetchone()
while row:
    print (str(row[0]) + " " + str(row[1]))
    row = cursor.fetchone()