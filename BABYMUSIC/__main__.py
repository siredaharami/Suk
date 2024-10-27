import asyncio
import importlib
import requests
import time
from flask import Flask
from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall
from threading import Thread

import config
from BABYMUSIC import LOGGER, app, userbot
from BABYMUSIC.core.call import BABY
from BABYMUSIC.misc import sudo
from BABYMUSIC.plugins import ALL_MODULES
from BABYMUSIC.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS

# Create a Flask app
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "BABY MUSIC BOT is running!"

def keep_alive():
    while True:
        try:
            requests.get("https://spotify-music-uryj.onrender.com")
        except Exception as e:
            print(f"Ping error: {e}")
        time.sleep(300)  # Ping every 5 minutes

async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("Session strings not filled. Please fill a Pyrogram session.")
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
        LOGGER(__name__).error(f"Error fetching banned users: {e}")

    await app.start()
    
    print("Flask app started successfully. Loading modules...")

    for all_module in ALL_MODULES:
        importlib.import_module(f"BABYMUSIC.plugins.{all_module}")

    print("Modules loaded. Starting userbot and BABY...")
    
    await userbot.start()
    await BABY.start()
    
    print("Userbot and BABY started. Attempting to stream...")
    
    try:
        await BABY.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("BABYMUSIC").error("Please start your group voice chat.")
        exit()
    except Exception as e:
        LOGGER(__name__).error(f"Error during stream call: {e}")

    await BABY.decorators()
    print("Bot initialized successfully!")
    await idle()
    
    await app.stop()
    await userbot.stop()
    LOGGER("BABYMUSIC").info("Stopped BABY MUSIC BOT.")

def run_flask():
    flask_app.run(host='0.0.0.0', port=8000)

if __name__ == "__main__":
    # Start the keep_alive function in a separate thread
    keep_alive_thread = Thread(target=keep_alive)
    keep_alive_thread.start()
    
    # Run the bot initialization
    asyncio.run(init())
