import pyodbc
#import pymssql
import json
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print(s.getsockname()[0])
s.close()

# Load credentials from json file
with open("azure_db_settings.json", "r") as file:  
    creds = json.load(file)
    
server = creds['server']
database = creds['database']
username = creds['username']
password = creds['password']
port = creds['port']
driver = creds['driver']

conn_str = "DRIVER={};SERVER={},{};DATABASE={};UID={};PWD={}".format(driver, server, port, database, username, password)\
#conn_str = "DRIVER={};SERVER={},{};".format(driver, server, port)
print(conn_str)

#cnxn = pyodbc.connect(conn_str, user=username, password=password, database=database)
cnxn = pyodbc.connect(conn_str)
cursor = cnxn.cursor()
cursor.execute("SELECT * FROM INFORMATION_SCHEMA.tables")
row = cursor.fetchone()
while row:
    print (str(row[0]) + " " + str(row[1]))
    row = cursor.fetchone()