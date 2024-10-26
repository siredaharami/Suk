import asyncio
import importlib
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

# Flask app initialize
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "BabyMusic bot is running!"

async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("String Session Not Filled. Please provide a Pyrogram Session.")
        return

    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
        LOGGER(__name__).info("Banned users loaded successfully.")
    except Exception as e:
        LOGGER(__name__).error(f"Error loading banned users: {e}")

    try:
        await app.start()
        LOGGER(__name__).info("App started successfully.")

        for all_module in ALL_MODULES:
            importlib.import_module("BABYMUSIC.plugins" + all_module)
        LOGGER("BABYMUSIC.plugins").info("All Features Loaded Successfully.")

        await userbot.start()
        await BABY.start()

        try:
            await BABY.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
        except NoActiveGroupCall:
            LOGGER("BABYMUSIC").error("Please start your log group voice chat or channel.")
            return
        except Exception as e:
            LOGGER("BABYMUSIC").error(f"Error starting stream call: {e}")

        await BABY.decorators()
        LOGGER("BABYMUSIC").info("Bot started successfully.")

        # Keep the bot running
        await idle()  
        
    except Exception as e:
        LOGGER(__name__).error(f"Error during bot initialization: {e}")
    finally:
        await shutdown()

async def shutdown():
    LOGGER("BABYMUSIC").info("Shutting down the bot...")
    await app.stop()
    await userbot.stop()
    await BABY.stop()
    LOGGER("BABYMUSIC").info("BabyMusic bot stopped.")

    # Ensure client session is closed properly
    if hasattr(app, 'client') and app.client is not None:
        await app.client.close()

async def start_flask():
    flask_app.run(host="0.0.0.0", port=8000)

async def main():
    await asyncio.gather(init(), start_flask())

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except Exception as e:
        LOGGER(__name__).error(f"Error in main execution: {e}")
    finally:
        # Allow pending tasks to finish
        pending = asyncio.all_tasks(loop)
        for task in pending:
            task.cancel()
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
