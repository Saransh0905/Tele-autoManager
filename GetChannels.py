from telethon.sync import TelegramClient
from telethon.tl.types import User, Channel, Chat
import sys
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.request import Request, urlopen
import asyncio
# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)

# filters to show only certain types of dialogs
users = False
channels = True
chats = True
import os


def GetChannels (write = False):
    f = open("data.json","r")
    data = json.load(f)
    api_id = data["API ID"]
    api_hash = data["API Hash"]
    try :
        channelList = []
        if not write :
            with TelegramClient('name', api_id, api_hash) as client:
                
                print(f"Logged in as: {client.get_me().first_name}\n")
                for dialog in client.get_dialogs():
                    ent = dialog.entity
                    if type(ent) == User:
                        if not users:
                            continue
                        x = f"{ent.id} : {ent.first_name}"
                        print(x.encode('utf8'))
                        channelList.append(x)
                    elif type(ent) == Channel:
                        if not channels:
                            continue
                        x = f"{ent.id} : {ent.title}"
                        print(x.encode('utf8'))
                        channelList.append(x)
                    elif type(ent) == Chat:
                        if not chats:
                            continue
                        x = f"{ent.id} : {ent.title}"
                        print(x.encode('utf8'))
                        channelList.append(x)
                    else:
                        pass
                    data["Channels"] = channelList
                    with open("data.json", "w") as outfile: 
                        json.dump(data, outfile)
                    
         
        else :
            with open ( "getIDOut.txt" , "wb"  )  as f :
                with TelegramClient('name', api_id, api_hash) as client:
                    x = f"Logged in as: {client.get_me().first_name}\n"
                   
                    print(x)
                    f.write(bytes ( x  ,encoding = "utf-8" ) +
                            bytes ( "\n" , encoding = "utf-8" ))
                    
                    for dialog in client.get_dialogs():
                        ent = dialog.entity
                        if type(ent) == User:
                            if not users:
                                continue
                            channelDict[ent.id] = ent.first_name
                            x = f"{ent.id} : {ent.first_name}"
                           
                            print(x)
                            f.write(bytes ( x  ,encoding = "utf-8" )+
                                    bytes ( "\n" , encoding = "utf-8" ))
                            
                        elif type(ent) == Channel:
                            if not channels:
                                continue
                            channelDict[ent.id] = ent.title
                            x = f"{ent.id} : {ent.title}"
                            
                            print(x)
                            f.write(bytes ( x  ,encoding = "utf-8" ) +
                                    bytes ( "\n" , encoding = "utf-8" ))
                            
                        elif type(ent) == Chat:
                            if not chats:
                                continue
                            channelDict[ent.id] = ent.title
                            x = f"{ent.id} : {ent.title}"
                           
                            print(x)
                            f.write(bytes ( x  ,encoding = "utf-8" ) +
                                    bytes ( "\n" , encoding = "utf-8" ))
                        else:
                            pass
    except Exception as e:
        print (e)
        
        client.session.close()
        print("Sesions closed by normal excepetion ")
        if os.path.isfile( "name.session") :
            os.remove("name.session")
    
    client.session.close()
    print("Sesions closed by normal ")
    if os.path.isfile("name.session") :
        os.remove( "name.session")
    return channelList

if __name__ == "__main__" :
    try :
        print("Getting Channels..")
        GetChannels()
    except KeyboardInterrupt:
        sys.exit(1)