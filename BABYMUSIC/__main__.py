import asyncio
import importlib
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

async def ping():
    while True:
        LOGGER(__name__).info("Bot is alive and pinging...")
        await asyncio.sleep(60)

async def init():
    if not config.STRING1:
        LOGGER(__name__).error("Session string not filled. Please fill a Pyrogram session.")
        exit()
    
    await sudo()
    
    try:
        users = await get_gbanned()
        BANNED_USERS.update(users)
        
        users = await get_banned_users()
        BANNED_USERS.update(users)
    except Exception as e:
        LOGGER(__name__).error(f"Error fetching banned users: {e}")

    await app.start()
    
    for module in ALL_MODULES:
        importlib.import_module("BABYMUSIC.plugins" + module)

    LOGGER("BABYMUSIC.plugins").info("All features loaded.")
    
    await userbot.start()
    await BABY.start()
    
    try:
        await BABY.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("BABYMUSIC").error("Please start your log group voice chat.")
        exit()
    except Exception as e:
        LOGGER(__name__).error(f"Error during stream call: {e}")

    await BABY.decorators()
    LOGGER("BABYMUSIC").info("Bot initialized successfully.")

    # Start the ping task
    asyncio.create_task(ping())
    await idle()

    await app.stop()
    await userbot.stop()
    LOGGER("BABYMUSIC").info("Stopped BABY MUSIC BOT.")

def run_flask():
    flask_app.run(host='0.0.0.0', port=8000)

if __name__ == "__main__":
    # Run Flask app in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()
    
    # Run the bot initialization in the main thread
    asyncio.run(init())
