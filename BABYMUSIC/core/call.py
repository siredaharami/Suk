import asyncio
import os
from datetime import datetime, timedelta
from typing import Union

from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.exceptions import AlreadyJoinedError, NoActiveGroupCall, TelegramServerError
from pytgcalls.types import Update
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.stream import StreamAudioEnded

import config
from BABYMUSIC import LOGGER, YouTube, app
from BABYMUSIC.utils.database import (
    add_active_chat,
    remove_active_chat,
    music_on,
)
from BABYMUSIC.utils.exceptions import AssistantErr
from BABYMUSIC.utils.stream.autoclear import auto_clean
from strings import get_string

class Call(PyTgCalls):
    def __init__(self):
        self.userbot1 = Client(
            name="BABYAss1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1),
        )
        self.one = PyTgCalls(self.userbot1)

    async def _clear_(self, chat_id):
        await remove_active_chat(chat_id)

    async def join_call(self, chat_id: int, link: str, video: bool = False):
        assistant = await group_assistant(self, chat_id)
        stream = AudioVideoPiped(link) if video else AudioPiped(link)
        try:
            await assistant.join_group_call(chat_id, stream)
            await add_active_chat(chat_id)
            await music_on(chat_id)
        except (NoActiveGroupCall, AlreadyJoinedError, TelegramServerError) as e:
            raise AssistantErr(str(e))

    async def stop_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await self._clear_(chat_id)
        await assistant.leave_group_call(chat_id)

    async def change_stream(self, client, chat_id):
        # Stream change logic here (simplified)
        check = db.get(chat_id)
        if not check:
            await self._clear_(chat_id)
            return await client.leave_group_call(chat_id)
        queued = check[0]["file"]
        stream = AudioVideoPiped(queued) if check[0]["streamtype"] == "video" else AudioPiped(queued)
        await client.change_stream(chat_id, stream)

    async def start(self):
        LOGGER(__name__).info("Starting PyTgCalls Client...")
        if config.STRING1:
            await self.one.start()

    async def decorators(self):
        @self.one.on_kicked()
        @self.one.on_closed_voice_chat()
        @self.one.on_left()
        async def stream_services_handler(_, chat_id: int):
            await self.stop_stream(chat_id)

        @self.one.on_stream_end()
        async def stream_end_handler(client, update: Update):
            if isinstance(update, StreamAudioEnded):
                await self.change_stream(client, update.chat_id)

BABY = Call()
