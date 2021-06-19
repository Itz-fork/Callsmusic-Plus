import traceback
import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

from helpers.database import db
from helpers.dbthings import main_broadcast_handler, delcmd_is_on, delcmd_on, delcmd_off
from config import BOT_OWNER

@Client.on_message(filters.private & filters.command("broadcast") & filters.user(BOT_OWNER) & filters.reply)
async def broadcast_handler_open(_, m: Message):
    await main_broadcast_handler(m, db)


@Client.on_message(filters.private & filters.command("stats") & filters.user(BOT_OWNER))
async def sts(_, m: Message):
    total_users = await db.total_users_count()
    await m.reply_text(text=f"**I have** `{total_users}` **Users In My Database**", parse_mode="Markdown", quote=True)


@Client.on_message(filters.private & filters.command("ban") & filters.user(BOT_OWNER))
async def ban(c: Client, m: Message):
    if len(m.command) == 1:
        await m.reply_text(
            f"Use this command to ban Users from using this bot 🤒! Read __**/modhelp**__ to Learn how to use this 🤭!",
            quote=True
        )
        return
    try:
        user_id = int(m.command[1])
        ban_duration = int(m.command[2])
        ban_reason = ' '.join(m.command[3:])
        ban_log_text = f"`Banning User 🗑...` \nUser ID: `{user_id}` \nDuration: `{ban_duration}` \nReason: `{ban_reason}`"
        try:
            await c.send_message(
                user_id,
                f"Lmao You are **Banned 😂!** \n\nReason: `{ban_reason}` \nDuration: `{ban_duration}` day(s). \n\n**Message From The Owner! Ask in **@Nexa_bots** if you think this was an mistake."
            )
            ban_log_text += '\n\nSuccessfully Notified About This Ban to that **Dumb User** 😅'
        except:
            traceback.print_exc()
            ban_log_text += f"\n\nKCUF! I can't Notify About This Ban to That **Dumb User** 🤯 \n\n`{traceback.format_exc()}`"
        await db.ban_user(user_id, ban_duration, ban_reason)
        print(ban_log_text)
        await m.reply_text(
            ban_log_text,
            quote=True
        )
    except:
        traceback.print_exc()
        await m.reply_text(
            f"An Error Occoured ❌! Traceback is given below\n\n`{traceback.format_exc()}`",
            quote=True
        )


@Client.on_message(filters.private & filters.command("unban") & filters.user(BOT_OWNER))
async def unban(c: Client, m: Message):
    if len(m.command) == 1:
        await m.reply_text(
            f"Use this command to ban Users from using this bot 🤒! Read __**/modhelp**__ to Learn how to use this 🤭!",
            quote=True
        )
        return
    try:
        user_id = int(m.command[1])
        unban_log_text = f"Unbanning user {user_id}"
        try:
            await c.send_message(
                user_id,
                f"Good News! **You are Unbanned** 😊!"
            )
            unban_log_text += '\n\nSuccessfully Notified About This to that **Good User** 😅'
        except:
            traceback.print_exc()
            unban_log_text += f"\n\nKCUF! I can't Notify About This to That **Dumb User** 🤯 \n\n`{traceback.format_exc()}`"
        await db.remove_ban(user_id)
        print(unban_log_text)
        await m.reply_text(
            unban_log_text,
            quote=True
        )
    except:
        traceback.print_exc()
        await m.reply_text(
            f"An Error Occoured ❌! Traceback is given below\n\n`{traceback.format_exc()}`",
            quote=True
        )


@Client.on_message(filters.private & filters.command("banlist") & filters.user(BOT_OWNER))
async def _banned_usrs(_, m: Message):
    all_banned_users = await db.get_all_banned_users()
    banned_usr_count = 0
    text = ''
    async for banned_user in all_banned_users:
        user_id = banned_user['id']
        ban_duration = banned_user['ban_status']['ban_duration']
        banned_on = banned_user['ban_status']['banned_on']
        ban_reason = banned_user['ban_status']['ban_reason']
        banned_usr_count += 1
        text += f"➬ **User ID**: `{user_id}`, **Ban Duration**: `{ban_duration}`, **Banned Date**: `{banned_on}`, **Ban Reason**: `{ban_reason}`\n\n"
    reply_text = f"**Total Banned:** `{banned_usr_count}`\n\n{text}"
    if len(reply_text) > 4096:
        with open('banned-user-list.txt', 'w') as f:
            f.write(reply_text)
        await m.reply_document('banned-user-list.txt', True)
        os.remove('banned-user-list.txt')
        return
    await m.reply_text(reply_text, True)


# Anti-Command Feature On/Off

@Client.on_message(filters.command("delcmd") & ~filters.private)
async def delcmdc(_, message: Message):
    if len(message.command) != 2:
        await message.reply_text("Lol! Wrong way Bro!")
        return
    status = message.text.split(None, 1)[1].strip()
    status = status.lower()
    chat_id = message.chat.id
    if status == "on":
        await delcmd_on(chat_id)
        await message.reply_text(
            "Enabled Delete Command Feature"
        )
    elif status == "off":
        await delcmd_off(chat_id)
        await message.reply_text("Disabled Delete Command Feature")
    else:
        await message.reply_text(
            "Can't Understand What you're talking about!"
        )
