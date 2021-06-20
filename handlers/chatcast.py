# From Daisyxmusic
# Copyright (C) 2021  Inukaasith

import asyncio

from pyrogram import Client, filters
from pyrogram.types import Dialog, Chat, Message
from pyrogram.errors import UserAlreadyParticipant

from callsmusic import client as pakaya
from config import SUDO_USERS

@Client.on_message(filters.command(["chatcast"]))
async def chatcast(_, message: Message):
    sent=0
    failed=0
    if message.from_user.id in SUDO_USERS:
        lol = await message.reply("`Starting a Chatcast...`")
        if not message.reply_to_message:
            await lol.edit("Please Reply to a Message to Chatcast it 🥺!")
            return
        msg = message.reply_to_message
        async for dialog in pakaya.iter_dialogs():
            try:
                await pakaya.msg.send_message(dialog.chat.id, msg)
                sent = sent+1
                await lol.edit(f"`ChatCasting...` \n\n**Sent to:** `{sent}` Chats \n**Failed in:** {failed} Chats")
            except:
                failed=failed+1
                await lol.edit(f"`ChatCasting...` \n\n**Sent to:** `{sent}` Chats \n**Failed in:** {failed} Chats")
            await asyncio.sleep(3)
        await message.reply_text(f"`ChatCasting Finished 😌` \n\n**Sent to:** `{sent}` Chats \n**Failed in:** {failed} Chats")
