import os
import random
import time
from SONALI import app
import requests
from pyrogram.types import Message
from pyrogram.types import InputMediaPhoto
from teambabyAPI import api
from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters


@app.on_message(
    filters.command(
        ["chatgpt", "ai", "ask", "gpt", "solve"],
        prefixes=["+", ".", "/", "-", "", "$", "#", "&"],
    )
)
async def chat_gpt(bot, message):
    
    try:
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        if len(message.command) < 2:
            await message.reply_text(
                "❍ ᴇxᴀᴍᴘʟᴇ:**\n\n/chatgpt ᴡʜᴏ ɪs ᴛʜᴇ ᴏᴡɴᴇʀ ᴏғ ˹ ʙʙʏ-ᴍᴜsɪᴄ ™˼𓅂?")
        else:
            a = message.text.split(' ', 1)[1]
            print("Input query:", a)  # Debug input

            response = api.gemini(a)
            print(response)  # Debug API response

            if not response:
                await message.reply_text("❍ ᴇʀʀᴏʀ: API se koi data nahi mil raha hai.")
            elif "results" not in response:
                await message.reply_text("❍ ᴇʀʀᴏʀ: API response mein results key nahi hai.")
            else:
                r = response["results"]
                await message.reply_text(f" {r} \n\n❍ᴘᴏᴡᴇʀᴇᴅ ʙʏ➛[ʙʧʙʏ-ᴍᴜsɪᴄ™](https://t.me/BABY09_WORLD)", parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        await message.reply_text(f"**❍ ᴇʀʀᴏʀ: {e} ")
