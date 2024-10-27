import asyncio
import importlib
from aiohttp import web
from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from BABYMUSIC import LOGGER, app, userbot
from BABYMUSIC.core.call import BABY
from BABYMUSIC.misc import sudo
from BABYMUSIC.plugins import ALL_MODULES
from BABYMUSIC.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


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
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("BABYMUSIC").info("𝗦𝗧𝗢𝗣 𝗕𝗔𝗕𝗬 𝗠𝗨𝗦𝗜𝗖🎻 𝗕𝗢𝗧..")


async def start_server():
    web_app = web.Application()

    async def handle(request):
        return web.Response(text="Hello, this is BABYMUSIC server!")

    web_app.router.add_get('/', handle)

    runner = web.AppRunner(web_app)
    await runner.setup()
    try:
        site = web.TCPSite(runner, '0.0.0.0', 8000)  # Listen on all interfaces
        await site.start()
        LOGGER(__name__).info("Server started on http://0.0.0.0:8000")
    except Exception as e:
        LOGGER(__name__).error(f"Error starting server: {e}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init())
    loop.run_until_complete(start_server())
    loop.run_forever()
