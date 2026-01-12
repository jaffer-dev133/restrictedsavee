# Don't Remove Credit Tg - @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ

import pyromod # <--- YE SABSE ZAROORI HAI: Iske bina login/logout work nahi karega
import asyncio
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN, STRING_SESSION, LOGIN_SYSTEM
from TechVJ.broadcast import send_restart_notification 
from threading import Thread
from app import run_web # app.py se function import kiya

if STRING_SESSION is not None and LOGIN_SYSTEM == False:
    TechVJUser = Client("TechVJ", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)
    TechVJUser.start()
else:
    TechVJUser = None

class Bot(Client):

    def __init__(self):
        super().__init__(
            "techvj login",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="TechVJ"),
            workers=150,
            sleep_threshold=5
        )

    async def start(self):
        await super().start()
        print('Bot Started Powered By @VJ_Bots')
        
        # Notification ko background task mein daala taaki bot hang na ho
        try:
            asyncio.create_task(send_restart_notification(self))
            print("Restart notification background mein bhej di gayi hai!")
        except Exception as e:
            print(f"Notification Error: {e}")

    async def stop(self, *args):
        await super().stop()
        print('Bot Stopped Bye')

if __name__ == "__main__":
    # 1. Flask server ko alag thread mein start karein (Render Health Check ke liye)
    print("Starting Web Server on Port 8080...")
    t = Thread(target=run_web)
    t.daemon = True
    t.start()
    
    # 2. Pyrogram Bot ko start karein
    bot = Bot()
    bot.run()
