import win32com.client
import win32com
import os
import sys

outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
accounts= win32com.client.Dispatch("Outlook.Application").Session.Accounts;

for account in accounts:
    print(account.DisplayName)

"""
get outlook
get accounts
for each account
    process folders

process folders
    for each folder
        process folder

process folder
    get each objects
        process type



"""