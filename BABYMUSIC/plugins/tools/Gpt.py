import re
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
API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"

# Hugging Face API Key (Apna API key yahaan likhein)
API_KEY = "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"

# Function to evaluate mathematical expressions
def evaluate_math_expression(expression):
    try:
        # Safe evaluation for simple arithmetic expressions
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return "Error: Unable to evaluate the expression."

# Function to call Hugging Face API for non-math questions
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
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, dict) and 'answer' in result:
                    answer = result['answer'].strip()
                    if answer and answer != "\n":
                        return answer
                    else:
                        return "I couldn't find a specific answer in the provided context."
                elif "error" in result:
                    return f"API Error: {result['error']}"
                else:
                    print("Unexpected response structure:", result)
                    return "Unexpected response format. Please check API response."
            
            elif response.status_code == 503:
                print(f"Model loading, retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"API returned error: {response.status_code}, {response.text}")
                return f"Error: {response.status_code}, {response.text}"
        
        except Exception as e:
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
            await message.reply_text(
                "❍ ᴇxᴀᴍᴘʟᴇ:**\n\n/chatgpt ᴡʜᴏ ɪs ᴛʜᴇ ᴏᴡɴᴇʀ ᴏғ ˹ ʙʙʏ-ᴍᴜsɪᴄ ™˼𓅂?"
            )
        else:
            question = message.text.split(' ', 1)[1]  # Extract user question
            
            # Check if question is a simple math expression
            if re.match(r'^[\d+\-*/.() ]+$', question):  # regex for basic math
                answer = evaluate_math_expression(question)
            else:
                # Non-math questions use context and Hugging Face API
                context = """
                Taj Mahal is a famous historical monument located in Agra, India. It was built by the Mughal Emperor Shah Jahan in memory of his beloved wife Mumtaz Mahal.
                """
                answer = get_answer_from_hugging_face(question, context)
            
            # Send the response to the user
            await message.reply_text(
                f"**Answer from AI:**\n\n{answer}\n\n❍ᴘᴏᴡᴇʀᴇᴅ ʙʏ➛[ʙʧʙʏ-ᴍᴜsɪᴄ™](https://t.me/BABY09_WORLD)", 
                parse_mode=ParseMode.MARKDOWN
            )
    
    except Exception as e:
        await message.reply_text(f"**❍ ᴇʀʀᴏʀ: {e}**")
