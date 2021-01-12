from telethon import TelegramClient, events
from datetime import datetime
from telethon.tl.types import MessageMediaDocument,MessageMediaPhoto
import logging
import os , sys
import asyncio
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
import json
import threading
from Activate import userpassGetter
import datetime
client = ''

def getInt(l):
    new = [int(x.split(" : ")[0]) for x in l]
    return new

def get_data():
    f = open('data.json')
    data = json.load(f)
    api_id = data['API ID']
    api_hash = data['API Hash']
    input1,output1 = getInt(data['Input1']),getInt(data['Output1'])
    input2,output2 = getInt(data['Input2']),getInt(data['Output2'])
    input3,output3 = getInt(data['Input3']),getInt(data['Output3'])
    input4,output4 = getInt(data['Input4']),getInt(data['Output4'])
    input5,output5 = getInt(data['Input5']),getInt(data['Output5'])
    input6,output6 = getInt(data['Input6']),getInt(data['Output6'])
    f.close()
    return api_id,api_hash,input1 , output1 , input2 , output2 , input3 , output3 , input4 , output4 , input5 , output5 , input6 , output6

async def keyValidator():
    while True:
        flag,key = userpassGetter()
        await asyncio.sleep(20)      #change time for checking validation key here (time is in seconds)
        if flag==True:
            print("Key registered!")
        if flag==False:
            print("Please Activate the software!")
            sys.exit(1)
async def run():


    global client
    api_id, api_hash,input_id1 , output_id1 , input_id2 , output_id2 , input_id3 , output_id3 , input_id4 , output_id4 , input_id5 , output_id5 ,input_id6 , output_id6 = get_data()
    print("Main Started")
    # if os.path.isfile('info.log'):
    #     os.remove('info.log')
    # if os.path.isfile('debug.log'):
    #     os.remove('debug.log')
    """
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='debug.log', )

    new_handler = logging.FileHandler('info.log')
    formatter = logging.Formatter('%(asctime)s ' + ' %(message)s', '%H:%M:%S')
    new_handler.setFormatter(formatter)
    new_handler.setLevel(logging.INFO)
    logging.getLogger().addHandler(new_handler) 
    """
    client = TelegramClient('session', api_id, api_hash , loop = loop )
    async def get_entity(entity_id):
        try:
            entity = await client.get_entity(entity_id)
            return entity
        except:
            async for dialog in await client.get_dialogs():
                if dialog.entity.id == entity_id:
                    return dialog.entity
            return None
    async def showInBox(text):
        await sys.stdout.write(text)
    @client.on(events.NewMessage)
    async def my_event_handler(event):
        if 'hello' in event.raw_text:
            await event.reply('hi!')
            await showInBox("Sent Hi!")

    # @client.on(events.NewMessage(func=lambda u: u.is_channel))
    # async def channel_handler(update):
    #     chat = await update.get_chat()
    #     if chat.id in input_id1:
    #         for entity_id in output_id1:
    #             entity = await get_entity(entity_id)
    #             await client.send_message(entity, update.message)
    #             s = f'{time()} Message {chat.id} => {entity.id}'
    #             mainTextBox.appendPlainText(s+'\n')
    #             showInBox(f'{time()} Message {chat.id} => {entity.id}')

    # @client.on(events.NewMessage(func=lambda u: u.is_channel))
    # async def channel_handler(update):
    #     chat = await update.get_chat()
    #     if chat.id in input_id2:
    #         for entity_id in output_id2:
    #             entity = await get_entity(entity_id)
    #             await client.send_message(entity, update.message)
    #             print(f'{time()} Message {chat.id} => {entity.id}')

    # @client.on(events.NewMessage(func=lambda u: u.is_channel))
    # async def channel_handler(update):
    #     chat = await update.get_chat()
    #     if chat.id in input_id3:
    #         for entity_id in output_id3:
    #             entity = await get_entity(entity_id)
    #             await client.send_message(entity, update.message)
    #             print(f'{time()} Message {chat.id} => {entity.id}')

    # @client.on(events.NewMessage(func=lambda u: u.is_channel))
    # async def channel_handler(update):
    #     chat = await update.get_chat()
    #     if chat.id in input_id4:
    #         for entity_id in output_id4:
    #             entity = await get_entity(entity_id)
    #             await client.send_message(entity, update.message)
    #             print(f'{time()} Message{chat.id} => {entity.id}')
                
    # @client.on(events.NewMessage(func=lambda u: u.is_channel))
    # async def channel_handler(update):
    #     chat = await update.get_chat()
    #     if chat.id in input_id5:
    #         for entity_id in output_id5:
    #             entity = await get_entity(entity_id)
    #             await client.send_message(entity, update.message)
    #             print(f'{time()} Message {chat.id} => {entity.id}')

    # @client.on(events.NewMessage(func=lambda u: u.is_channel))
    # async def channel_handler(update):
    #     chat = await update.get_chat()
    #     if chat.id in input_id6:
    #         for entity_id in output_id6:
    #             entity = await get_entity(entity_id)
    #             await client.send_message(entity, update.message)
    #             print(f'{time()} Message {chat.id} => {entity.id}')            

    await client.start()
    await client.run_until_disconnected()

async def main():
    await run()
    await periodic()

def time():
    now = datetime.now()
    return now.strftime('[%H:%M:%S]')   

def temp():
    loop = asyncio.new_event_loop()
    task1 = loop.create_task(run())
    task2 = loop.create_task(keyValidator())
    loop.run_until_complete(asyncio.wait([task1,task2]))
def disconnect():
    print("Disconnecting")
    asyncio.run(client.disconnect())
def startMain():
    import pytesseract as tess
    tess.pytesseract.tesseract_cmd = "Hello/Path"
    _thread = threading.Thread(target=temp)
    _thread.start()
if __name__=="__main__":
    temp()
