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

async def init():
    try:
        if not any([config.STRING1, config.STRING2, config.STRING3, config.STRING4, config.STRING5]):
            LOGGER(__name__).error("𝐒𝐭𝐫𝐢𝐧𝐠 𝐒𝐞𝐬𝐬𝐢𝐨𝐧 𝐍𝐨𝐭 𝐅𝐢𝐥𝐥𝐞𝐝, 𝐏𝐥𝐞𝐚𝐬𝐞 𝐅𝐢𝐥𝐥 𝐀 𝐏𝐲𝐫𝐨𝐠𝐫𝐚𝐦 𝐒𝐞𝐬𝐬𝐢𝐨𝐧")
            exit()

        await sudo()
        LOGGER(__name__).info("Fetching banned users...")
        
        gbanned_users = await get_gbanned()
        for user_id in gbanned_users:
            BANNED_USERS.add(user_id)
        
        banned_users = await get_banned_users()
        for user_id in banned_users:
            BANNED_USERS.add(user_id)
        
        LOGGER(__name__).info("Banned users fetched successfully.")

        await app.start()
        LOGGER(__name__).info("App started successfully.")

        for module in ALL_MODULES:
            importlib.import_module("BABYMUSIC.plugins" + module)

        LOGGER("BABYMUSIC.plugins").info("𝐀𝐥𝐥 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬 𝐋𝐨𝐚𝐝𝐞𝐝 𝐁𝐚𝐛𝐲🥳...")
        
        await userbot.start()
        LOGGER(__name__).info("Userbot started successfully.")

        await BABY.start()
        LOGGER(__name__).info("Baby call started successfully.")

        try:
            await BABY.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
        except NoActiveGroupCall:
            LOGGER("BABYMUSIC").error("𝗣𝗹𝗭 𝗦𝗧𝗔𝗥𝗧 𝗬𝗢𝗨𝗥 𝗟𝗢𝗚 𝗚𝗥𝗢𝗨𝗣 𝗩𝗢𝗜𝗖𝗘𝗖𝗛𝗔𝗧\𝗖𝗛𝗔𝗡𝗡𝗘𝗟\n\n𝗕𝗔𝗕𝗬𝗠𝗨𝗦𝗜𝗖 𝗕𝗢𝗧 𝗦𝗧𝗢𝗣........")
            exit()
        except Exception as e:
            LOGGER(__name__).error(f"Error during stream call: {e}")

        await BABY.decorators()
        LOGGER("BABYMUSIC").info("╔═════ஜ۩۞۩ஜ════╗\n  ☠︎︎𝗠𝗔𝗗𝗘 𝗕𝗬 𝗠𝗥 𝗨𝗧𝗧𝗔𝗠★𝗥𝗔𝗧𝗛𝗢𝗥𝗘\n╚═════ஜ۩۞۩ஜ════╝")
        
        await idle()

    except Exception as e:
        LOGGER(__name__).error(f"An error occurred: {e}")
    finally:
        await app.stop()
        await userbot.stop()
        LOGGER("BABYMUSIC").info("𝗦𝗧𝗢𝗣 𝗕𝗔𝗕𝗬 𝗠𝗨𝗦𝗜𝗖🎻 𝗕𝗢𝗧..")

def run_flask():
    flask_app.run(host='0.0.0.0', port=8000, use_reloader=False)

if __name__ == "__main__":
    # Run Flask app in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()
    
    # Run the bot initialization
    asyncio.run(init())
