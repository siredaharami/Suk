import random
import time
from BABYMUSIC import app
import requests
from pyrogram.types import Message
from pyrogram.types import InputMediaPhoto
from teambabyAPI import api
from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters
import openai
from config import OPENAI_API_KEY  # Importing the API key from config.py

# Set the OpenAI API key from the config file
openai.api_key = OPENAI_API_KEY

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
                "❍ ᴇxᴀᴍᴘʟᴇ:**\n\n/chatgpt ᴡʜᴏ ɪs ᴛʜᴇ ᴏᴡɴᴇʀ ᴏғ ˹ ʙᴀʙʏ-ᴍᴜsɪᴄ ™˼𓅂?"
            )
        else:
            question = message.text.split(' ', 1)[1]  # Extracting the question
            response = openai.Completion.create(
                engine="text-davinci-003",  # You can choose the latest available model
                prompt=question,
                max_tokens=150
            )
            answer = response.choices[0].text.strip()  # Extracting the answer from GPT
            
            await message.reply_text(
                f"**Answer from ChatGPT:**\n\n{answer}\n\n❍ᴘᴏᴡᴇʀᴇᴅ ʙʏ➛[ʙʧʙʏ-ᴍᴜsɪᴄ™](https://t.me/BABY09_WORLD)", 
                parse_mode=ParseMode.MARKDOWN
            )
    
    except Exception as e:
        await message.reply_text(f"**❍ ᴇʀʀᴏʀ: {e}**")
