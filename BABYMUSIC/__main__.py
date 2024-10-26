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

     
