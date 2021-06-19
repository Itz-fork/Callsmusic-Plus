# From Daisyxmusic (Telegram bot project )
# Copyright (C) 2021  Inukaasith

from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
import asyncio
from config import SUDO_USERS

@Client.on_message(filters.command(["chatcast"]))
async def chatcast(client, message):
    sent=0
    failed=0
    if message.from_user.id in SUDO_USERS:
        lol = await message.reply("`Starting a Chatcast...`")
        if not message.reply_to_message:
            await lol.edit("Please Reply to a Message to Chatcast it 🥺!")
            return
        msg = message.reply_to_message.text
        async for dialog in Client.iter_dialogs():
            try:
                await Client.send_message(dialog.chat.id, msg)
                sent = sent+1
                await lol.edit(f"`ChatCasting...` /n/n**Sent to:** `{sent}` Chats /n**Failed in:** {failed} Chats")
            except:
                failed=failed+1
                await lol.edit(f"`ChatCasting...` /n/n**Sent to:** `{sent}` Chats /n**Failed in:** {failed} Chats")
            await asyncio.sleep(3)
        await message.reply_text(f"`ChatCasting Finished 😌` /n/n**Sent to:** `{sent}` Chats /n**Failed in:** {failed} Chats")
