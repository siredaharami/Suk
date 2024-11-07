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

# Hugging Face API Key (Apna API key yahaan likhein)
API_KEY = "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"

# Function to call Hugging Face API with retry logic
def get_answer_from_hugging_face(question, context, retries=3, wait_time=20):
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    payload = {
        "inputs": {
            "question": question,
            "context": context
        }
    }
    
    for attempt in range(retries):
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            
            # Check if the response is successful
            if response.status_code == 200:
                result = response.json()
                # Checking if the 'answer' key is present
                if 'answer' in result:
                    return result['answer']
                else:
                    print("Unexpected response format:", result)
                    return "Unexpected response format. Please check the API response."
            
            elif response.status_code == 503:
                # Model loading; retry after waiting
                print(f"Model loading, retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                # Return error message for other status codes
                print(f"API returned error: {response.status_code}, {response.text}")
                return f"Error: {response.status_code}, {response.text}"
        
        except Exception as e:
            # Log and return error for exception
            print("Exception occurred:", e)
            return f"An error occurred: {e}"
    
    return "Model is still loading. Please try again later."

@app.on_message(
    filters.command(
        ["chatgpt", "ai", "ask", "gpt", "solve"],
        prefixes=["+", ".", "/", "-", "", "$", "#", "&"],
    )
)
async def chat_gpt(bot, message):
    try:
        # Show typing action to indicate bot is processing
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        
        if len(message.command) < 2:
            # Reply if no question provided
            await message.reply_text(
                "❍ ᴇxᴀᴍᴘʟᴇ:**\n\n/chatgpt ᴡʜᴏ ɪs ᴛʜᴇ ᴏᴡɴᴇʀ ᴏғ ˹ ʙʙʏ-ᴍᴜsɪᴄ ™˼𓅂?"
            )
        else:
            question = message.text.split(' ', 1)[1]  # Extract user question
            
            # Define the context for the model
            context = """
            ˹ ʙʙʏ-ᴍᴜsɪᴄ ™˼𓅂 is a community platform for music lovers and people who enjoy lively discussions about various topics.
            """
            
            # Get answer from Hugging Face with retry logic
            answer = get_answer_from_hugging_face(question, context)
            
            # Send the response to the user
            await message.reply_text(
                f"**Answer from AI:**\n\n{answer}\n\n❍ᴘᴏᴡᴇʀᴇᴅ ʙʏ➛[ʙʧʙʏ-ᴍᴜsɪᴄ™](https://t.me/BABY09_WORLD)", 
                parse_mode=ParseMode.MARKDOWN
            )
    
    except Exception as e:
        # Inform the user about the error
        await message.reply_text(f"**❍ ᴇʀʀᴏʀ: {e}**")
