import asyncio
import importlib
from flask import Flask
from threading import Thread
from pyrogram import Client, idle
from pytgcalls.exceptions import NoActiveGroupCall
import requests
import time

import config
from BABYMUSIC import LOGGER, app, userbot
from BABYMUSIC.core.call import BABY
from BABYMUSIC.misc import sudo
from BABYMUSIC.plugins import ALL_MODULES
from BABYMUSIC.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS

# Flask app setup
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Hello, this is BABYMUSIC server!"

def run_flask():
    flask_app.run(host='0.0.0.0', port=8000)

# Keep-alive function to ping the server at regular intervals
def keep_alive():
    while True:
        try:
            # You can modify this to your preferred URL for keep-alive
            requests.get("https://<app_name>.onrender.com")
        except Exception as e:
            print(f"Ping error: {e}")
        time.sleep(300)  # Ping every 5 minutes 

# Async bot initialization
async def init():
    if all(not getattr(config, f'STRING{i}', None) for i in range(1, 6)):
        LOGGER(__name__).error("𝐒𝐭𝐫𝐢𝐧𝐠 𝐒𝐞𝐬𝐬𝐢𝐨𝐧 𝐍𝐨𝐭 𝐅𝐢𝐥𝐥𝐞𝐝, 𝐏𝐥𝐞𝐚𝐬𝐞 𝐅𝐢𝐥𝐥 𝐀 𝐏𝐲𝐫𝐨𝐠𝐫𝐚𝐦 𝐒𝐞𝐬𝐬𝐢𝐨𝐧")
        exit()
    
    await sudo()
    try:
        banned_users = await get_gbanned() + await get_banned_users()
        for user_id in banned_users:
            BANNED_USERS.add(user_id)
    except Exception as e:
        LOGGER(__name__).error(f"Error fetching banned users: {e}")

    await app.start()
    
    for module in ALL_MODULES:
        importlib.import_module(f"BABYMUSIC.plugins{module}")
    
    LOGGER("BABYMUSIC.plugins").info("𝐀𝐥𝐥 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬 𝐋𝐨𝐚𝐝𝐞𝐝 𝐁𝐚𝐛𝐲🥳...")
    await userbot.start()
    await BABY.start()

    try:
        await BABY.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("BABYMUSIC").error("𝗣𝗹𝗭 𝗦𝗧𝗔𝗥𝗧 𝗬𝗢𝗨𝗥 𝗟𝗢𝗚 𝗚𝗥𝗢𝗨𝗣 𝗩𝗢𝗜𝗖𝗘𝗖𝗛𝗔𝗧\𝗖𝗛𝗔𝗡𝗡𝗘𝗟\n\n𝗕𝗔𝗕𝗬𝗠𝗨𝗦𝗜𝗖 𝗕𝗢𝗧 𝗦𝗧𝗢𝗣........")
        exit()
    except Exception as e:
        LOGGER("BABYMUSIC").error(f"Error during stream call: {e}")

    await BABY.decorators()
    LOGGER("BABYMUSIC").info("╔═════ஜ۩۞۩ஜ════╗\n  ☠︎︎𝗠𝗔𝗗𝗘 𝗕𝗬 𝗠𝗥 𝗨𝗧𝗧𝗔𝗠★𝗥𝗔𝗧𝗛𝗢𝗥𝗘\n╚═════ஜ۩۞۩ஜ════╝")
    
    while True:
        await asyncio.sleep(3600)  # Keep the event loop alive


if __name__ == "__main__":
    # Start the Flask server in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True  # This ensures the thread ends when the main program exits
    flask_thread.start()

    # Start the keep-alive function in a separate thread
    keep_alive_thread = Thread(target=keep_alive)
    keep_alive_thread.daemon = True
    keep_alive_thread.start()

    # Start the bot in the main thread using asyncio
    bot_loop = asyncio.get_event_loop()

    # Run bot initialization in a thread
    bot_thread = Thread(target=lambda: bot_loop.run_until_complete(init()))
    bot_thread.daemon = True  # This ensures the thread ends when the main program exits
    bot_thread.start()

    # Keep the main thread alive so the bot, Flask, and keep-alive functions can run
    bot_loop.run_forever()
