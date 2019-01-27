#!/usr/bin/python3
import telepot
import time
from telepot.loop import MessageLoop
import json
from pathlib import Path
import os
from configparser import ConfigParser

if not os.path.isfile("config.ini"):
    print("Il file di configurazione non è presente. Rinomina il file 'config-sample.ini' in 'config.ini' e inserisci il token.")
    exit()

script_path = os.path.dirname(os.path.realpath(__file__))
config_parser = ConfigParser()
config_parser.read(os.path.join(script_path,"config.ini"))

TOKEN=config_parser.get("access","token")

if TOKEN == "":
    print("Token non presente.")
    exit()

versione="1.0.4"
ultimoAggiornamento="27-01-2019"

print("Versione: "+versione+" - Aggiornamento: "+ultimoAggiornamento)

def risposte(msg):
    type_msg="NO"
    if "text" in msg and "entities" in msg:
        text=str(msg['text'])
        if text=="/start" or text=="/myuserid":
            type_msg="OK"
    else:
        type_msg="NO"

    user_id=msg['from']['id']
    if not "chat" in msg:
        msg=msg["message"]
    chat_id=msg['chat']['id']

    if type_msg=="OK":
        userid=[]
        userid_path="userid_list.json"
        chatid=[]
        chatid_path="chatid_list.json"
        if Path(userid_path).exists():
            userid = json.loads(open(userid_path).read())
        if Path(chatid_path).exists():
            chatid = json.loads(open(chatid_path).read())
        bot.sendMessage(chat_id, "Il tuo userid è: "+str(user_id))
        print("Il tuo userid è: "+user_id)
        if not int(user_id) in userid:
            userid.append(int(user_id))
            bot.sendMessage(240188083, "Nuovo userid: "+str(user_id))
        if not int(chat_id) in chatid:
            chatid.append(int(chat_id))
            bot.sendMessage(240188083, "Nuova chatid: "+str(chat_id))
        try:
            with open(userid_path, "wb") as f:
                f.write(json.dumps(userid).encode("utf-8"))
        except Exception as e:
            print("Excep:01 -> "+str(e))
        try:
            with open(chatid_path, "wb") as f:
                f.write(json.dumps(chatid).encode("utf-8"))
        except Exception as e:
            print("Excep:02 -> "+str(e))

bot=telepot.Bot(TOKEN)
MessageLoop(bot, {'chat': risposte, 'callback_query': risposte}).run_as_thread()

while 1:
    time.sleep(1)