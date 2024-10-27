import asyncio
import importlib
import struct
from sqlite3 import connect, OperationalError
from quart import Quart
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

# Create a Quart app
quart_app = Quart(__name__)

@quart_app.route("/")
async def home():
    return "BABY MUSIC BOT is running!"

async def get_db_connection():
    try:
        conn = connect("your_database.db")  # Replace with your actual database path
        return conn
    except OperationalError as e:
        LOGGER(__name__).error(f"Database connection error: {e}")
        return None

async def update_peers(parsed_peers):
    conn = await get_db_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.executemany("INSERT INTO peers (user_id) VALUES (?)", parsed_peers)
        conn.commit()
    except OperationalError as e:
        LOGGER(__name__).error(f"Error updating peers: {e}")
    finally:
        conn.close()

async def fetch_and_unpack_data():
    try:
        # Simulated data fetch; replace with actual data fetching logic
        data = await get_data()  # Update this line as needed
        
        # Log the size and content of the incoming data
        LOGGER(__name__).info(f"Received data size: {len(data)}")
        if len(data) < 271:
            LOGGER(__name__).warning("Received data is too short, expected at least 271 bytes.")
            return None  # Handle this case accordingly

        # Example unpacking; adjust format as needed
        unpacked_data = struct.unpack('271s', data)  # Adjust format as required
        return unpacked_data

    except struct.error as e:
        LOGGER(__name__).error(f"Unpacking error: {e}")
    except Exception as e:
        LOGGER(__name__).error(f"An error occurred while fetching or unpacking data: {e}")

async def init():
    if not any([config.STRING1, config.STRING2, config.STRING3, config.STRING4, config.STRING5]):
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
    
    while True:
        try:
            await BABY.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
            break
        except NoActiveGroupCall:
            LOGGER("BABYMUSIC").error("𝗣𝗹𝗭 𝗦𝗧𝗔𝗥𝗧 𝗬𝗢𝗨𝗥 𝗟𝗢𝗚 𝗚𝗥𝗢𝗨𝗣 𝗩𝗢𝗜𝗖𝗘𝗖𝗛𝗔𝗧\𝗖𝗛𝗔𝗡𝗡𝗘𝗟\n\n𝗕𝗔𝗕𝗬𝗠𝗨𝗦𝗜𝗖 𝗕𝗢𝗧 𝗦𝗧𝗢𝗣........")
            await asyncio.sleep(10)
        except Exception as e:
            LOGGER(__name__).error(f"Error during stream call: {e}")
            await asyncio.sleep(10)

    await BABY.decorators()
    LOGGER("BABYMUSIC").info("╔═════ஜ۩۞۩ஜ════╗\n  ☠︎︎𝗠𝗔𝗗𝗘 𝗕𝗬 𝗠𝗥 𝗨𝗧𝗧𝗔𝗠★𝗥𝗔𝗧𝗛𝗢𝗥𝗘\n╚═════ஜ۩۞۩ஜ════╝")

    # Keeping the bot alive with a heartbeat
    while True:
        await asyncio.sleep(60)

async def shutdown():
    await app.stop()
    await userbot.stop()
    LOGGER("BABYMUSIC").info("𝗦𝗧𝗢𝗣 𝗕𝗔𝗕𝗬 𝗠𝗨𝗦𝗜𝗖🎻 𝗕𝗢𝗧..")

async def run_quart():
    await quart_app.run_task(host='0.0.0.0', port=8000)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    # Run both the asyncio bot and the Quart app
    try:
        loop.run_until_complete(asyncio.gather(init(), run_quart()))
    except KeyboardInterrupt:
        loop.run_until_complete(shutdown())
    except Exception as e:
        LOGGER(__name__).error(f"An error occurred: {e}")
        loop.run_until_complete(shutdown())
