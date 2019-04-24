import win32com.client
import win32com
import os
import sys

def read_accounts(outlook):
    accounts= win32com.client.Dispatch("Outlook.Application").Session.Accounts
    for account in accounts:
        print(account.DisplayName)
        inbox = outlook.Folders(account.DeliveryStore.Displayname)
        yield inbox

def read_folders(inbox):
    for folder in inbox.folders:
        print(folder.name)
        yield folder

def get_email(recipient):
    try:
        props = recipient.PropertyAccessor
        emailaddress =  props.GetProperty("http://schemas.microsoft.com/mapi/proptag/0x39FE001E")
    except Exception as ex:
        emailaddress = ex
    return emailaddress

def process_folder(folder):
    messages = folder.Items
    for message in messages:
        item = {}

        try:
            item["subject"] = message.Subject
            item["body"] = message.Body

            try:
                item["sender"] = message.Sender
                item["senderaddress"] = message.SenderEmailAddress
                item["sendertype"] = message.SenderEmailType
                item["sendername"] = message.SenderName
                if message.SenderEmailType == "EX":
                    item["senderemail"] = get_email(message.Sender)
                else:
                    item["senderemail"] = message.SenderEmailAddress

            except:
                pass

            try:
                item["conversationindex"] = message.ConversationIndex
                item["conversationid"] = message.ConversationID
                item["conversationtopic"] = message.ConversationTopic
            except:
                pass

            item["actors"] = []
            for r in message.Recipients:
                actor = {}
                try:
                    actor["address"] = r.Address
                    actor["id"] = r.EntryID
                    actor["name"] = r.Name
                    actor["type"] = r.Type
                    actor['email'] = get_email(r)

                except Exception as ex:
                    actor["error"] = ex
                    
                item["actors"].append(actor)

            try:
                item['sent'] = message.SentOn
                item["to"] = message.To
                item["cc"] = message.CC
                item["bcc"] = message.BCC
            except:
                # not all objects have the to, cc and bcc attribs
                pass

        except Exception as ex:
            item["error"] = ex

        yield item

def print_item(item, item_keys):
    print("===")
    for key in item_keys:
        if key in item:
            print("\t{}:{}".format(key, item[key]))


outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

folder_names = ['Inbox'] 
item_keys = ['subject', 'sent', 'sendername', 'senderemail', 'sendertype', 'conversationtopic', 'conversationindex', 'conversationid', 'to', 'cc', 'bcc', 'actors', 'error', 'body']

item_count = 0
for inbox in read_accounts(outlook):
    for folder in read_folders(inbox):
        if folder.Name in folder_names:
            for item in process_folder(folder):
              item_count += 1
              print_item(item, item_keys)
              if item_count % 1000 == 0:
                  break

print("found {} items".format(item_count))
