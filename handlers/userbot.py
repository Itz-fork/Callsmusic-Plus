# Copyright (c) @Bruh_0x (Itz-fork)
# Plugin To Handle Your Streamer Account

from callsmusic.callsmusic import client as NEXAUB
from pyrogram import Client, filters

# To Block a PM'ed User
@NEXAUB.on_message(filters.private & filters.command("block", [".", "/"]) & filters.me & ~filters.edited)
async def ubblock(_, message: Message):
  shit_id = message.chat.id
  gonna_block_u = await message.edit_text("`Blocking User...`")
  try:
    await NEXAUB.block_user(shit_id)
    await gonna_block_u.edit("`Successfully Blocked This User`")
  except Exception as lol:
    await gonna_block_u.edit(f"`Can't Block This Guy! May be this is durov?` \n\n**Error:** `{lol}`")


# To Unblock User That Already Blocked
# Feature Coming Soon with DB!

# To Get How Many Chats that you are in (PM's also counted)
@NEXAUB.on_message(filters.private & filters.command("chats", [".", "/"]) & filters.me & ~filters.edited)
async def ubgetchats(_, message: Message):
  getting_chats = await message.edit_text("`Checking Your Chats, Hang On...`")
  rick_astley = NEXAUB.get_dialogs_count()
  try:
    await getting_chats.edit(f"**Total Dialogs Counted:** `{rick_astley}`")
  except Exception as lol:
    await getting_chats.edit(f"`Never Gonna Give You Up!` \n\n**Error:** `{lol}`")
