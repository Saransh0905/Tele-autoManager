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
# filters to show only certain types of dialogs
users = False
channels = True
chats = True
import os

def GetAPIInfo():
    #Chromedriver path
    chromeDriverPath = "chromedriver"
    driver = webdriver.Chrome(chromeDriverPath)
    time = 120                    #this is in seconds you can change it.
    print("STARTING CHROME DRIVER YOU HAVE: ",time)
    driver.get("https://my.telegram.org/apps")
    wait = WebDriverWait(driver,time)
    visible = EC.visibility_of_element_located
    try:
        wait.until(visible((By.ID, "app_edit_form")))
        api_id = driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "col-md-7", " " ))]//strong').text
        api_hash = driver.find_elements_by_class_name('uneditable-input')[1].text
        driver.close()
    except:
        f = open('data.json')
        data = json.load(f)
        api_id = data['API ID']
        api_hash = data['API Hash']
        print("CLOSED!")
        f.close()
    return api_id, api_hash

