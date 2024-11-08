import requests
from BABYMUSIC import app
from pyrogram.types import Message
from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters

# Define your AIML API Key
API_KEY = "e4de6eec07ad405390a630ddb65c6c38"  # Replace with your actual API key from aimlapi.com

# API Base URL (as given in the documentation)
BASE_URL = "https://api.aimlapi.com"

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

            # Define the headers and payload as per the API's documentation
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }

            # Define the payload (messages) as required by the API
            payload = {
                "model": "mistralai/Mistral-7B-Instruct-v0.2",  # You can change the model name if needed
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an AI assistant who knows everything."
                    },
                    {
                        "role": "user",
                        "content": query  # User's query from the message
                    }
                ]
            }

            # Make the POST request to the AIML API
            response = requests.post(f"{BASE_URL}/v1/chat/completions", json=payload, headers=headers)

            # Debugging: print raw response
            print("API Response Text:", response.text)  # Print raw response
            print("Status Code:", response.status_code)  # Check the status code

            # If the response is empty or not successful, handle the error
            if response.status_code != 200:
                await message.reply_text(f"❍ ᴇʀʀᴏʀ: API request failed. Status code: {response.status_code}")
            elif not response.text.strip():
                await message.reply_text("❍ ᴇʀʀᴏʀ: API se koi valid data nahi mil raha hai. Response was empty.")
            else:
                # Attempt to parse the JSON response
                try:
                    response_data = response.json()
                    print("API Response JSON:", response_data)  # Debug response JSON

                    # Get the assistant's response from the JSON data
                    if "choices" in response_data and len(response_data["choices"]) > 0:
                        result = response_data["choices"][0]["message"]["content"]
                        await message.reply_text(
                            f"{result} \n\n❍ᴘᴏᴡᴇʀᴇᴅ ʙʏ➛[ʙʧʙʏ-ᴍᴜsɪᴄ™](https://t.me/BABY09_WORLD)",
                            parse_mode=ParseMode.MARKDOWN
                        )
                    else:
                        await message.reply_text("❍ ᴇʀʀᴏʀ: No response from API.")
                except ValueError:
                    await message.reply_text("❍ ᴇʀʀᴏʀ: Invalid response format.")
    except Exception as e:
        # Catch any other exceptions and send an error message
        await message.reply_text(f"**❍ ᴇʀʀᴏʀ: {e} ")
