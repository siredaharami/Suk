import asyncio
import importlib
import requests  # Make sure to import requests
import time  # Import time for sleep
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

async def start_bot():
    await app.start()
    print("LOG: Found Bot token Booting Zeus.")
    
    # Start all clients
    clients = [userbot, BABY]
    ids = []
    for cli in clients:
        try:
            await cli.start()
            ex = await cli.get_me()
            print(f"Started {ex.first_name} 🔥")
            ids.append(ex.id)
        except Exception as e:
            print(f"Error starting client {cli}: {e}")

    await idle()

async def init():
    if (
        not config.STRING1
    ):
        LOGGER(__name__).error("𝐒𝐭𝐫𝐢𝐧𝐠 𝐒𝐞𝐬𝐬𝐢𝐨𝐧 𝐍𝐨𝐭 𝐅𝐢𝐥𝐥𝐞𝐝, 𝐏𝐥𝐞𝐚𝐬𝐞 𝐅𝐢𝐥𝐥 𝐀 𝐏𝐲𝐫𝐨𝐠𝐫𝐚𝐦 𝐒𝐞𝐬𝐬𝐢𝐨𝐧")
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
    for all_module in ALL_MODULES:
        importlib.import_module("BABYMUSIC.plugins" + all_module)
    
    LOGGER("BABYMUSIC.plugins").info("𝐀𝐥𝐥 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬 𝐋𝐨𝐚𝐝𝐞𝐝 𝐁𝐚𝐛𝐲🥳...")
    await userbot.start()
    await BABY.start()
    
    try:
        await BABY.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("BABYMUSIC").error(
            "𝗣𝗹𝗭 𝗦𝗧𝗔𝗥𝗧 𝗬𝗢𝗨𝗥 𝗟𝗢𝗚 𝗚𝗥𝗢𝗨𝗣 𝗩𝗢𝗜𝗖𝗘𝗖𝗛𝗔𝗧\𝗖𝗛𝗔𝗡𝗡𝗘𝗟\n\n𝗕𝗔𝗕𝗬𝗠𝗨𝗦𝗜𝗖 𝗕𝗢𝗧 𝗦𝗧𝗢𝗣........"
        )
        exit()
    except Exception as e:
        LOGGER(__name__).error(f"Error during stream call: {e}")
    
    await BABY.decorators()
    LOGGER("BABYMUSIC").info(
        "╔═════ஜ۩۞۩ஜ════╗\n  ☠︎︎𝗠𝗔𝗗𝗘 𝗕𝗬 𝗠𝗥 𝗨𝗧𝗧𝗔𝗠★𝗥𝗔𝗧𝗛𝗢𝗥𝗘\n╚═════ஜ۩۞۩ஜ════╝"
    )
    await idle()
    
    await app.stop()
    await userbot.stop()
    LOGGER("BABYMUSIC").info("𝗦𝗧𝗢𝗣 𝗕𝗔𝗕𝗬 𝗠𝗨𝗦𝗜𝗖🎻 𝗕𝗢𝗧..")

def run_flask():
    flask_app.run(host='0.0.0.0', port=8000)

if __name__ == "__main__":
    # Start Flask in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()
    
    # Run the bot initialization
    asyncio.run(init())  # Updated to use asyncio.run() for better compatibility
