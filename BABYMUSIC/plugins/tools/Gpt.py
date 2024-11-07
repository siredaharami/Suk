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

# Hugging Face API Key (Replace with your actual API key)
API_KEY = "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"  # Your provided API key

# Function to query Hugging Face API for question answering
def get_answer_from_hugging_face(question, context):
    headers = {
        "Authorization": f"Bearer {API_KEY}"  # Use Bearer token for authorization
    }
    payload = {
        "inputs": {
            "question": question,
            "context": context
        }
    }
    try:
        # Sending POST request to Hugging Face API
        response = requests.post(API_URL, headers=headers, json=payload)
        # Check if the request was successful
        if response.status_code == 200:
            result = response.json()
            return result['answer']
        else:
            return f"Error: {response.status_code}, {response.text}"
    except Exception as e:
        return f"An error occurred: {e}"

@app.on_message(
    filters.command(
        ["chatgpt", "ai", "ask", "gpt", "solve"],
        prefixes=["+", ".", "/", "-", "", "$", "#", "&"],
    )
)
async def chat_gpt(bot, message):
    try:
        # Typing action to indicate that bot is processing the request
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        
        if len(message.command) < 2:
            # If no question is provided
            await message.reply_text(
                "❍ ᴇxᴀᴍᴘʟᴇ:**\n\n/chatgpt ᴡʜᴏ ɪs ᴛʜᴇ ᴏᴡɴᴇʀ ᴏғ ˹ ʙʙʏ-ᴍᴜsɪᴄ ™˼𓅂?"
            )
        else:
            question = message.text.split(' ', 1)[1]  # Extracting the question
            
            # Context for the question-answering model (can be static or dynamic)
            context = """
            ˹ ʙʙʏ-ᴍᴜsɪᴄ ™˼𓅂 is a community platform for music lovers and people who enjoy lively discussions about various topics.
            """
            
            # Get the answer from Hugging Face API
            answer = get_answer_from_hugging_face(question, context)
            
            # Send the response back to the user
            await message.reply_text(
                f"**Answer from AI:**\n\n{answer}\n\n❍ᴘᴏᴡᴇʀᴇᴅ ʙʏ➛[ʙʧʙʏ-ᴍᴜsɪᴄ™](https://t.me/BABY09_WORLD)", 
                parse_mode=ParseMode.MARKDOWN
            )
    
    except Exception as e:
        # In case of any error
        await message.reply_text(f"**❍ ᴇʀʀᴏʀ: {e}**")
