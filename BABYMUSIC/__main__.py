import asyncio
import importlib
import requests
import time
import threading
from flask import Flask
from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from BABYMUSIC import LOGGER, app, userbot
from BABYMUSIC.core.call import BABY
from BABYMUSIC.misc import sudo
from BABYMUSIC.plugins import ALL_MODULES
from BABYMUSIC.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS

flask_app = Flask(__name__)

# Flask app basic route
@flask_app.route('/')
def home():
    return "Flask app running on port 8000"

# Keep-alive function to send regular pings
def keep_alive():
    while True:
        try:
            requests.get("https://spotify-music-uryj.onrender.com")
        except Exception as e:
            print(f"Ping error: {e}")
        time.sleep(300)  # Ping every 5 minutes

async def start_bot():
    await app.start()
    print("LOG: Found Bot token Booting Zeus.")
    
    # Start all clients
    clients = [userbot, BABY]  # Assuming userbot and BABY are your clients
    ids = []
    for cli in clients:
        try:
            await cli.start()
            ex = await cli.get_me()
            print(f"Started {ex.first_name} 🔥")
            ids.append(ex.id)
        except Exception as e:
            print(f"Error: {e}")

    await idle()

async def init():
    if not any([config.STRING1]):
        LOGGER(__name__).error("String Session Not Filled, Please Fill A Pyrogram Session")
        exit()
    
    await sudo()
    
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception as e:
        print(f"Error loading banned users: {e}")
    
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("BABYMUSIC.plugins." + all_module)
    
    LOGGER("BABYMUSIC.plugins").info("All Features Loaded Baby🥳...")
    await userbot.start()
    await BABY.start()
    
    try:
        await BABY.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("BABYMUSIC").error(
            "Please START YOUR LOG GROUP VOICECHAT CHANNEL\n\nBABYMUSIC BOT STOP........"
        )
        exit()
    except Exception as e:
        print(f"Stream call error: {e}")

    await BABY.decorators()
    LOGGER("BABYMUSIC").info(
        "╔═════ஜ۩۞۩ஜ════╗\n  ☠︎︎MADE BY MR UTTAM★RATHORE\n╚═════ஜ۩۞۩ஜ════╝"
    )
    
    # The app will not reach this if idle() is called first
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("BABYMUSIC").info("STOP BABY MUSIC🎻 BOT..")

def run_flask():
    flask_app.run(host='0.0.0.0', port=8000)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init())

    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Start keep-alive function in a separate thread
    keep_alive_thread = threading.Thread(target=keep_alive)
    keep_alive_thread.start()

    # Start the bot
    loop.run_until_complete(start_bot())
