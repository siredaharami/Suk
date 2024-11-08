import requests
from BABYMUSIC import app
from pyrogram.types import Message
from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters

# Your AIML API Key
API_KEY = "2ef61674b85143f8a54c7ab3e581d160"  # Replace with your actual API key from aimlapi.com

# Base URL for AIML API
API_URL = "https://aimlapi.com/api/v1/query"

@app.on_message(
    filters.command(
        ["chatgpt", "ai", "ask", "gpt", "solve"],
        prefixes=["+", ".", "/", "-", "", "$", "#", "&"],
    )
)
async def chat_gpt(bot, message):
    try:
        # Typing action when the bot is processing the message
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)

        if len(message.command) < 2:
            # If no question is asked, send an example message
            await message.reply_text(
                "❍ ᴇxᴀᴍᴘʟᴇ:**\n\n/chatgpt ᴡʜᴏ ɪs ᴛʜᴇ ᴏᴡɴᴇʀ ᴏғ ˹ ʙʙʏ-ᴍᴜsɪᴄ ™˼𓅂?"
            )
        else:
            # Extract the query from the user's message
            query = message.text.split(' ', 1)[1]
            print("Input query:", query)  # Debug input

            # Make a request to the AIML API
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }

            data = {
                "query": query
            }

            # Send the request to the AIML API
            response = requests.post(API_URL, json=data, headers=headers)

            # Debugging: print raw response
            print("API Response Text:", response.text)  # Print raw response
            print("Status Code:", response.status_code)  # Check the status code

            # If the response is empty or not successful, handle the error
            if response.status_code != 200 or not response.text.strip():
                await message.reply_text("❍ ᴇʀʀᴏʀ: API se koi valid data nahi mil raha hai.")
            else:
                # Attempt to parse the JSON response
                try:
                    response_data = response.json()
                    print("API Response JSON:", response_data)  # Debug response JSON

                    if "response" not in response_data:
                        await message.reply_text("❍ ᴇʀʀᴏʀ: API response mein 'response' key nahi mili.")
                    else:
                        result = response_data["response"]
                        await message.reply_text(
                            f"{result} \n\n❍ᴘᴏᴡᴇʀᴇᴅ ʙʏ➛[ʙʧʙʏ-ᴍᴜsɪᴄ™](https://t.me/BABY09_WORLD)",
                            parse_mode=ParseMode.MARKDOWN
                        )
                except ValueError:
                    await message.reply_text("❍ ᴇʀʀᴏʀ: Invalid response format.")
    except Exception as e:
        # Catch any other exceptions and send an error message
        await message.reply_text(f"**❍ ᴇʀʀᴏʀ: {e} ")
