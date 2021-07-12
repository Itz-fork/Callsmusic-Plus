# Copyright (c) 2021 @Bruh_0x (Itz-fork) <https://github.com/Itz-fork>
# Made with ❤️ for CallsMusic-Plus <https://github.com/Itz-fork/Callsmusic-Plus>
# Kanging without credits is strictly prohibited

import heroku3
import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Dialog, Chat, Message

from config import BOT_USERNAME, BOT_OWNER, cp_version, nexaub_version
from callsmusic.callsmusic import client as NEXAUB
from handlers.ownerstuff import _check_heroku

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
@NEXAUB.on_message(filters.command("unblock", [".", "/"]) & filters.me & ~filters.edited)
async def ubblock(_, message: Message):
  good_bro = int(message.command[1])
  gonna_unblock_u = await message.edit_text("`Unblocking User...`")
  try:
    await NEXAUB.unblock_user(good_bro)
    await gonna_unblock_u.edit(f"`Successfully Unblocked The User` \n**User ID:** `{good_bro}`")
  except Exception as lol:
    await gonna_unblock_u.edit(f"`Can't Unblock That Guy!, I think he is still dumb!` \n\n**Error:** `{lol}`")


# To Get How Many Chats that you are in (PM's also counted)
@NEXAUB.on_message(filters.private & filters.command("chats", [".", "/"]) & filters.me & ~filters.edited)
async def ubgetchats(_, message: Message):
  getting_chats = await message.edit_text("`Checking Your Chats, Hang On...`")
  async for dialog in NEXAUB.iter_dialogs():
    try:
      total = await NEXAUB.get_dialogs_count()
      await getting_chats.edit(f"**Total Dialogs Counted:** `{total}` \n\n**Not Stable Lol**")
    except Exception as lol:
      brokenmsg = await message.reply_text(f"`Never Gonna Give You Up!, but Something Went Wrong!`")
      await brokenmsg.edit(f"**Error:** `{lol}`")


# Leave From a Chat
@NEXAUB.on_message(filters.command("kickme", [".", "/"]) & filters.me & ~filters.edited)
async def ubkickme(_, message: Message):
  i_go_away = await message.edit_text("`Leaving This Chat...`")
  try:
    await NEXAUB.leave_chat(message.chat.id)
    await i_go_away.edit("`Successfully Leaved This Chat!`")
  except Exception as lol:
    await i_go_away.edit(f"`Can't Leave This Chat!, What a cruel world!` \n\n**Error:** `{lol}`")


# Alive Message
@NEXAUB.on_message(filters.command("alive", [".", "/"]) & filters.me & ~filters.edited)
async def ubalive(_, message: Message):
  alive_msg = await message.edit_text("`Processing...`")
  alive_pic = "cache/NexaUB.jpg"
  await message.reply_photo(alive_pic, caption=f"**🌀 Nexa Music Userbot is Alive 🌀** \n\n**🤖 Version** \n ↳**Bot Version:** `{cp_version}` \n ↳**Userbot Version:** `{nexaub_version}` \n\n**🐬 Info**\n ↳**Music Bot:** @{BOT_USERNAME} \n ↳**Owner:** [Click Here](tg://user?id={BOT_OWNER})")
  await alive_msg.delete()


# Get Streamer's Private Chat Messages in to a Private Group
PM_LOGS = os.environ.get("PM_LOGS", "")
PM_LOG_CHAT_ID = int(os.environ.get("PM_LOG_CHAT_ID", 12345678))

@NEXAUB.on_message(filters.private & filters.command("pmlogs", [".", "/"]) & filters.me & ~filters.edited)
@_check_heroku
async def getlogs(client: NEXAUB, message: Message, app_):
  if len(message.command) != 2:
        await message.edit_text("`Wait, What?` \n\n**To Turn On:** `.pmlogs on` \n**To Turn Off:** `.pmlogs off` ")
        return
  status = message.text.split(None, 1)[1].strip()
  status = status.lower()
  if status == "on":
    if PM_LOG_CHAT_ID != 12345678:
      await message.edit("`You already did this huh? Why again?`")
      return # Next level logic lol
    logmsg = await message.edit_text("`PM Message Logs Module is Starting Now...`")
    await asyncio.sleep(2) # Lmao
    chat_pic = "cache/NexaUB.jpg"
    try:
      await logmsg.edit("`Creating Private Group Now...`!")
      pmchat = await NEXAUB.create_group(f"Nexa Userbot's PM Logs", BOT_OWNER)
      chat_id = pmchat.id
      await NEXAUB.set_chat_photo(chat_id=chat_id, photo=chat_pic)
      await logmsg.edit(f"`Successfully Finished Step 1, To Enable This Feature Please Check Your Log Group That Created Now!!` \n\n ~ **@NexaBotsUpdates**")
      await client.send_message(chat_id, f"**Welcome to @{(await NEXAUB.get_me()).username}'s PM Log Group!** \nThis Chat will Contain All PM Messages Of **@{(await NEXAUB.get_me()).username}** ! \n\n\n`/setvar PM_LOG_CHAT_ID {chat_id}` \n\n ✪ **Please Copy and Send Above Command To Your @{BOT_USERNAME} Now**!")
    except Exception as lol:
      await logmsg.edit(f"`Can't Enable This Feature!, Something Wrong Happend!` \n\n**Error:** `{lol}`")
      return
  elif status == "off":
    if PM_LOG_CHAT_ID == 12345678:
      await message.edit("`First Enable This Feature!`")
    heroku_var = app_.config()
    _var = "PM_LOG_CHAT_ID"
    try:
      await message.edit_text("`Trying to Remove PM Logs Feature...`")
      await NEXAUB.leave_chat(PM_LOG_CHAT_ID, delete=True)
      await message.edit_text("`Leaved The PmLog Group! Hope this disabled...`")
      heroku_var[_var] = 12345678
    except Exception as lol:
      await message.edit_text(f"`Can't Remove This Feature! Maybe You Didn't Enabled It?` \n\n**Error:** {lol}")


@NEXAUB.on_message(filters.private)
async def sendpmlol(client: NEXAUB, message: Message):
  NEXAUB_ID = int((await NEXAUB.get_me()).id)
  if message.from_user.id == BOT_OWNER or message.from_user.id == NEXAUB_ID:
    return
  pmlogchat = PM_LOG_CHAT_ID
  userinfo = await NEXAUB.get_users(user_ids=message.from_user.id)
  nibba = int(message.chat.id)
  msg_txt = message.text
  if PM_LOG_CHAT_ID == 12345678:
    return
  else:
    try:
      forwardedmsg = await client.forward_messages(chat_id=pmlogchat, from_chat_id=message.chat.id, message_ids=message.message_id)
      await forwardedmsg.reply_text(f"**Incoming Message** \n\n**👤 User Info \n ⤷**User Name:** `{userinfo.first_name}` \n ⤷**Username:** @{userinfo.username} \n ⤷**User ID:** `{nibba}`", parse_mode="md")
    except Exception as lol:
      await client.send_message(chat_id=pmlogchat, text=f"`Something Wrong Happend While Sending Message!` \n\n**Error:** {lol}", parse_mode="md")
