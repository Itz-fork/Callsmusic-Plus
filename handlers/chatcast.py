# Credits Daisyxmusic
# Copyright (C) 2021  Inukaasith | Bruh_0x

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
    if message.from_user.id not in SUDO_USERS:
        await message.reply("Go away! This is not for you 😂!")
        return
    else:
        wtf = await message.reply("`Starting a Chatcast...`")
        if not message.reply_to_message:
            await wtf.edit("Please Reply to a Message to Chatcast it 🥺!")
            return
        lmao = message.reply_to_message.text
        async for dialog in Client.iter_dialogs():
            try:
                await Client.send_message(dialog.chat.id, lmao)
                sent = sent+1
                await wtf.edit(f"`ChatCasting...` \n\n**Sent to:** `{sent}` Chats \n**Failed in:** {failed} Chats")
            except:
                failed=failed+1
                await wtf.edit(f"`ChatCasting...` \n\n**Sent to:** `{sent}` Chats \n**Failed in:** {failed} Chats")
            await asyncio.sleep(3)
        await message.reply_text(f"`ChatCasting Finished 😌` \n\n**Sent to:** `{sent}` Chats \n**Failed in:** {failed} Chats")
