import random
import time
from BABYMUSIC import app
import requests
from pyrogram.types import Message
from pyrogram.types import InputMediaPhoto
from teambabyAPI import api
from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters

# Hugging Face API URL for question answering
API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-distilled-squad"

# Hugging Face API Key (Aapka API key yahaan likhein)
API_KEY = "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"  # Aapka Hugging Face API Key

# Function jo Hugging Face API ko call karegi aur retry karegi
def get_answer_from_hugging_face(question, context, retries=3, wait_time=20):
    headers = {
        "Authorization": f"Bearer {API_KEY}"  # Authorization header mein API key bhejna
    }
    payload = {
        "inputs": {
            "question": question,
            "context": context
        }
    }
    
    for attempt in range(retries):
        try:
            # Hugging Face API ko request bhejna
            response = requests.post(API_URL, headers=headers, json=payload)
            
            # Agar request successful hai
            if response.status_code == 200:
                result = response.json()
                return result['answer']
            elif response.status_code == 503:
                # Agar model load ho raha ho, toh retry karenge
                print(f"Model load ho raha hai, {wait_time} seconds baad try karenge...")
                time.sleep(wait_time)  # Wait karein specified time ke liye
            else:
                return f"Error: {response.status_code}, {response.text}"
        except Exception as e:
            # Agar koi aur error aaye toh handle karein
            return f"An error occurred: {e}"
    
    return "Model abhi bhi load ho raha hai. Kripya kuch der baad try karein."

@app.on_message(
    filters.command(
        ["chatgpt", "ai", "ask", "gpt", "solve"],
        prefixes=["+", ".", "/", "-", "", "$", "#", "&"],
    )
)
async def chat_gpt(bot, message):
    try:
        # Typing action bhejna, jisse user ko lage ki bot jawab de raha hai
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        
        if len(message.command) < 2:
            # Agar user ne question nahi diya
            await message.reply_text(
                "❍ ᴇxᴀᴍᴘʟᴇ:**\n\n/chatgpt ᴡʜᴏ ɪs ᴛʜᴇ ᴏᴡɴᴇʀ ᴏғ ˹ ʙʙʏ-ᴍᴜsɪᴄ ™˼𓅂?"
            )
        else:
            question = message.text.split(' ', 1)[1]  # User ka question nikalna
            
            # Model ke liye context (aap isse dynamic ya static bana sakte hain)
            context = """
            ˹ ʙʙʏ-ᴍᴜsɪᴄ ™˼𓅂 is a community platform for music lovers and people who enjoy lively discussions about various topics.
            """
            
            # Hugging Face se answer lena retry logic ke saath
            answer = get_answer_from_hugging_face(question, context)
            
            # User ko response bhejna
            await message.reply_text(
                f"**Answer from AI:**\n\n{answer}\n\n❍ᴘᴏᴡᴇʀᴇᴅ ʙʏ➛[ʙʧʙʏ-ᴍᴜsɪᴄ™](https://t.me/BABY09_WORLD)", 
                parse_mode=ParseMode.MARKDOWN
            )
    
    except Exception as e:
        # Agar koi error aaye toh user ko batayein
        await message.reply_text(f"**❍ ᴇʀʀᴏʀ: {e}**")
