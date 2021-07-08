import traceback
import asyncio # Lol! Weird Import!

from asyncio import QueueEmpty

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery

from callsmusic import callsmusic, queues

from helpers.filters import command
from helpers.decorators import errors, authorized_users_only
from helpers.database import db, dcmdb, Database
from helpers.dbthings import handle_user_status, delcmd_is_on, delcmd_on, delcmd_off
from config import LOG_CHANNEL, BOT_OWNER, BOT_USERNAME
from . import que, admins as fuck


@Client.on_message()
async def _(bot: Client, cmd: Message):
    await handle_user_status(bot, cmd)

# Back Button
BACK_BUTTON = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Go Back ⬅️", callback_data="cbback")]])

@Client.on_message(~filters.private)
async def delcmd(_, message: Message):
    if await delcmd_is_on(message.chat.id) and message.text.startswith("/") or message.text.startswith("!"):
        await message.delete()
    await message.continue_propagation()


@Client.on_message(filters.command(["reload", f"reload@{BOT_USERNAME}"]))
@authorized_users_only # Fuk Off Everyone! Admin Only Command!
async def update_admin(client, message):
    global fuck
    admins = await client.get_chat_members(message.chat.id, filter="administrators")
    new_ads = []
    for u in admins:
        new_ads.append(u.user.id)
    fuck[message.chat.id] = new_ads
    await message.reply_text("**Successfully Updated Admin List ✅!**")


# Control Menu Of Player
@Client.on_message(command(["control", f"control@{BOT_USERNAME}", "p"]))
@errors
@authorized_users_only
async def controlset(_, message: Message):
    await message.reply_text(
        "**Successfully Opened Control Menu Of Streamer Player!**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⏸ Pause ⏸", callback_data="cbpause"
                    ),
                    InlineKeyboardButton(
                        "▶️ Resume ▶️", callback_data="cbresume"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "⏩ Skip ⏩", callback_data="cbskip"
                    ),
                    InlineKeyboardButton(
                        "⏹ End ⏹", callback_data="cbend"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🔇 Mute 🔇", callback_data="cbmute"
                    ),
                    InlineKeyboardButton(
                        "🔈 Unmute 🔈", callback_data="cbunmute"
                    )
                ]
            ]
        )
    )



@Client.on_message(command(["pause", f"pause@{BOT_USERNAME}", "p"]))
@errors
@authorized_users_only
async def pause(_, message: Message):
    if callsmusic.pause(message.chat.id):
        await message.reply_text("⏸ Paused")
    else:
        await message.reply_text("❗️ Nothing is playing")

@Client.on_message(command(["resume", f"resume@{BOT_USERNAME}", "r"]))
@errors
@authorized_users_only
async def resume(_, message: Message):
    if callsmusic.resume(message.chat.id):
        await message.reply_text("🎧 Resumed")
    else:
        await message.reply_text("❗️ Nothing is paused")


@Client.on_message(command(["end", f"end@{BOT_USERNAME}", "e"]))
@errors
@authorized_users_only
async def stop(_, message: Message):
    if message.chat.id not in callsmusic.active_chats:
        await message.reply_text("❗️ Nothing is playing")
    else:
        try:
            queues.clear(message.chat.id)
        except QueueEmpty:
            pass

        await callsmusic.stop(message.chat.id)
        await message.reply_text("✅ Cleared the queue and left the Voice Chat!")


@Client.on_message(command(["skip", f"skip@{BOT_USERNAME}", "s"]))
@errors
@authorized_users_only
async def skip(_, message: Message):
    if message.chat.id not in callsmusic.active_chats:
        await message.reply_text("❗️ Nothing is playing")
    else:
        queues.task_done(message.chat.id)

        if queues.is_empty(message.chat.id):
            await callsmusic.stop(message.chat.id)
        else:
            await callsmusic.set_stream(
                message.chat.id, queues.get(message.chat.id)["file"]
            )

        await message.reply_text("🗑 Skipped")


@Client.on_message(command(["mute", f"mute@{BOT_USERNAME}", "m"]))
@errors
@authorized_users_only
async def mute(_, message: Message):
    result = callsmusic.mute(message.chat.id)

    if result == 0:
        await message.reply_text("🔇 Muted")
    elif result == 1:
        await message.reply_text("🔇 Already muted")
    elif result == 2:
        await message.reply_text("❗️ Not in voice chat")


@Client.on_message(command(["unmute", f"unmute@{BOT_USERNAME}", "um"]))
@errors
@authorized_users_only
async def unmute(_, message: Message):
    result = callsmusic.unmute(message.chat.id)

    if result == 0:
        await message.reply_text("🔈 Unmuted")
    elif result == 1:
        await message.reply_text("🔈 Already unmuted")
    elif result == 2:
        await message.reply_text("❗️ Not in voice chat")


# Music Player Callbacks (Control by buttons feature)

@Client.on_callback_query(filters.regex("cbpause"))
async def cbpause(_, query: CallbackQuery):
    if callsmusic.pause(query.message.chat.id):
        await query.edit_message_text("⏸ Song Paused", reply_markup=BACK_BUTTON)
    else:
        await query.edit_message_text("❗️ Nothing is playing, Lol!", reply_markup=BACK_BUTTON)

@Client.on_callback_query(filters.regex("cbresume"))
async def cbresume(_, query: CallbackQuery):
    if callsmusic.resume(query.message.chat.id):
        await query.edit_message_text("🎧 Song Resumed", reply_markup=BACK_BUTTON)
    else:
        await query.edit_message_text("❗️ Nothing is paused, Lol!", reply_markup=BACK_BUTTON)

@Client.on_callback_query(filters.regex("cbend"))
async def cbend(_, query: CallbackQuery):
    if query.message.chat.id not in callsmusic.active_chats:
        await query.edit_message_text("❗️ Nothing is playing", reply_markup=BACK_BUTTON)
    else:
        try:
            queues.clear(query.message.chat.id)
        except QueueEmpty:
            pass

        await callsmusic.stop(query.message.chat.id)
        await query.edit_message_text("✅ Cleared the queue and left the Voice Chat!", reply_markup=BACK_BUTTON)

@Client.on_callback_query(filters.regex("cbskip"))
async def cbskip(_, query: CallbackQuery):
     if query.message.chat.id not in callsmusic.active_chats:
        await query.edit_message_text("❗️ Nothing is playing", reply_markup=BACK_BUTTON)
     else:
        queues.task_done(query.message.chat.id)
        
        if queues.is_empty(query.message.chat.id):
            await callsmusic.stop(query.message.chat.id)
        else:
            await callsmusic.set_stream(
                query.message.chat.id, queues.get(query.message.chat.id)["file"]
            )

        await query.edit_message_text("🗑 Skipped", reply_markup=BACK_BUTTON)

@Client.on_callback_query(filters.regex("cbmute"))
async def cbmute(_, query: CallbackQuery):
    result = callsmusic.mute(query.message.chat.id)

    if result == 0:
        await query.edit_message_text("🔇 Muted", reply_markup=BACK_BUTTON)
    elif result == 1:
        await query.edit_message_text("🔇 Already muted", reply_markup=BACK_BUTTON)
    elif result == 2:
        await query.edit_message_text("❗️ Not in voice chat", reply_markup=BACK_BUTTON)

@Client.on_callback_query(filters.regex("cbunmute"))
async def cbunmute(_, query: CallbackQuery):
    result = callsmusic.unmute(query.message.chat.id)

    if result == 0:
        await query.edit_message_text("🔈 Unmuted", reply_markup=BACK_BUTTON)
    elif result == 1:
        await query.edit_message_text("🔈 Already unmuted", reply_markup=BACK_BUTTON)
    elif result == 2:
        await query.edit_message_text("❗️ Not in voice chat", reply_markup=BACK_BUTTON)


# Anti-Command Feature On/Off

@Client.on_message(filters.command(["delcmd", f"delcmd@{BOT_USERNAME}"]) & ~filters.private)
@authorized_users_only
async def delcmdc(_, message: Message):
    if len(message.command) != 2:
        await message.reply_text("Lol! This isn't the way to use this command 😂! Please read **/help** ☺️")
        return
    status = message.text.split(None, 1)[1].strip()
    status = status.lower()
    chat_id = message.chat.id
    if status == "on":
        if await delcmd_is_on(message.chat.id):
            await message.reply_text("Eh! You are already enabled This Service 😉")
            return
        else:
            await delcmd_on(chat_id)
            await message.reply_text(
                "Successfully Enabled Delete Command Feature For This Chat 😇"
            )
    elif status == "off":
        await delcmd_off(chat_id)
        await message.reply_text("Successfully Disabled Delete Command Feature For This Chat 😌")
    else:
        await message.reply_text(
            "Can't Understand What you're talking about! Maybe Read **/help** 🤔"
        )
