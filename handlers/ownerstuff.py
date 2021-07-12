# Credits @AbirHasan2005, @DevsExpo and DaisyXMusic
# This file is part of CallsMusic-Plus (https://github.com/Itz-fork/Callsmusic-Plus)

import sys
import os
import heroku3
import time
import traceback
import asyncio
import shutil
import psutil

from pyrogram import Client, filters
from pyrogram.types import Message, Dialog, Chat
from pyrogram.errors import UserAlreadyParticipant
from datetime import datetime
from functools import wraps
from os import environ, execle, path, remove
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from callsmusic import client as pakaya
from helpers.database import db
from helpers.dbthings import main_broadcast_handler
from handlers.musicdwn import humanbytes, get_text
from config import BOT_USERNAME, BOT_OWNER, UPSTREAM_REPO, U_BRANCH, HEROKU_URL, HEROKU_API_KEY, HEROKU_APP_NAME, SUDO_USERS


# Stats Of Your Bot
@Client.on_message(filters.command("stats") & filters.user(BOT_OWNER))
async def botstats(_, message: Message):
    total, used, free = shutil.disk_usage(".")
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    total_users = await db.total_users_count()
    await message.reply_text(
        text=f"**💫 Bot Stats Of @{BOT_USERNAME} 💫** \n\n**🤖 Bot Version:** `V2.9.1` \n\n**👥 Users:** \n ↳**PM'ed Users:** `{total_users}` \n\n**💾 Disk Usage,** \n ↳**Total Disk Space:** `{total}` \n ↳**Used:** `{used}({disk_usage}%)` \n ↳**Free:** `{free}` \n\n**🎛 Hardware Usage,** \n ↳**CPU Usage:** `{cpu_usage}%` \n ↳**RAM Usage:** `{ram_usage}%`",
        parse_mode="Markdown",
        quote=True
    )


# Broadcast message to users (This will Broadcast using Bot with Db)
@Client.on_message(filters.private & filters.command("broadcast") & filters.user(BOT_OWNER) & filters.reply)
async def broadcast_handler_open(_, m: Message):
    await main_broadcast_handler(m, db)

# Broadcast message to users (This will Broadcast using streamer account without db)
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
        async for dialog in pakaya.iter_dialogs():
            try:
                await pakaya.send_message(dialog.chat.id, lmao)
                sent = sent+1
                await wtf.edit(f"`ChatCasting...` \n\n**Sent to:** `{sent}` Chats \n**Failed in:** {failed} Chats")
            except:
                failed=failed+1
                await wtf.edit(f"`ChatCasting...` \n\n**Sent to:** `{sent}` Chats \n**Failed in:** {failed} Chats")
            await asyncio.sleep(3)
        await message.reply_text(f"`ChatCasting Finished 😌` \n\n**Sent to:** `{sent}` Chats \n**Failed in:** {failed} Chats")


# Ban User
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


# Unban User
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
        unban_log_text = f"`Unbanning user...` /n**User ID:**{user_id}"
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


# Banned User List
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


# Updator
REPO_ = UPSTREAM_REPO
BRANCH_ = U_BRANCH

@Client.on_message(filters.command("update") & filters.user(BOT_OWNER))
async def updatebot(_, message: Message):
    msg = await message.reply_text("`Updating Module is Starting! Please Wait...`")
    try:
        repo = Repo()
    except GitCommandError:
        return await msg.edit(
            "`Invalid Git Command!`"
        )
    except InvalidGitRepositoryError:
        repo = Repo.init()
        if "upstream" in repo.remotes:
            origin = repo.remote("upstream")
        else:
            origin = repo.create_remote("upstream", REPO_)
        origin.fetch()
        repo.create_head(U_BRANCH, origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
    if repo.active_branch.name != U_BRANCH:
        return await msg.edit(
            f"Hmmm... Seems Like You Are Using Custom Branch Named `{repo.active_branch.name}`! Please Use `{U_BRANCH}` To Make This Works!"
        )
    try:
        repo.create_remote("upstream", REPO_)
    except BaseException:
        pass
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(U_BRANCH)
    if not HEROKU_URL:
        try:
            ups_rem.pull(U_BRANCH)
        except GitCommandError:
            repo.git.reset("--hard", "FETCH_HEAD")
        await run_cmd("pip3 install --no-cache-dir -r requirements.txt")
        await msg.edit("**Successfully Updated! Restarting Now!**")
        args = [sys.executable, "main.py"]
        execle(sys.executable, *args, environ)
        exit()
        return
    else:
        await msg.edit("`Heroku Detected!`")
        await msg.edit("`Updating and Restarting has Started! Please wait for 5-10 Minutes!`")
        ups_rem.fetch(U_BRANCH)
        repo.git.reset("--hard", "FETCH_HEAD")
        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(HEROKU_URL)
        else:
            remote = repo.create_remote("heroku", HEROKU_URL)
        try:
            remote.push(refspec="HEAD:refs/heads/master", force=True)
        except BaseException as error:
            await msg.edit(f"**Updater Error** \nTraceBack : `{error}`")
            return repo.__del__()


# Heroku Logs

async def edit_or_send_as_file(
    text: str,
    message: Message,
    client: Client,
    caption: str = "`Result!`",
    file_name: str = "result",
    parse_mode="md",
):
    """Send As File If Len Of Text Exceeds Tg Limit Else Edit Message"""
    if not text:
        await message.edit("`There is something other than text! Aborting...`")
        return
    if len(text) > 1024:
        await message.edit("`OutPut is Too Large to Send in TG, Sending As File!`")
        file_names = f"{file_name}.text"
        open(file_names, "w").write(text)
        await client.send_document(message.chat.id, file_names, caption=caption)
        await message.delete()
        if os.path.exists(file_names):
            os.remove(file_names)
        return
    else:
        return await message.edit(text, parse_mode=parse_mode)



heroku_client = None
if HEROKU_API_KEY:
    heroku_client = heroku3.from_key(HEROKU_API_KEY)

def _check_heroku(func):
    @wraps(func)
    async def heroku_cli(client, message):
        heroku_app = None
        if not heroku_client:
            await message.reply_text(
                "`Please Add Heroku API Key To Use This Feature!`"
            )
        elif not HEROKU_APP_NAME:
            await edit_or_reply(
                message, "`Please Add Heroku APP Name To Use This Feature!`"
            )
        if HEROKU_APP_NAME and heroku_client:
            try:
                heroku_app = heroku_client.app(HEROKU_APP_NAME)
            except:
                await message.reply_text(
                    message, "`Heroku Api Key And App Name Doesn't Match! Check it again`"
                )
            if heroku_app:
                await func(client, message, heroku_app)

    return heroku_cli

@Client.on_message(filters.command("logs") & filters.user(BOT_OWNER))
@_check_heroku
async def logswen(client: Client, message: Message, happ):
    msg = await message.reply_text("`Please Wait For a Moment!`")
    logs = happ.get_log()
    capt = f"Heroku Logs Of `{HEROKU_APP_NAME}`"
    await edit_or_send_as_file(logs, msg, client, capt, "logs")


# Restart Your Bot
@Client.on_message(filters.command("restart") & filters.user(BOT_OWNER))
@_check_heroku
async def restart(client: Client, message: Message, hap):
    msg = await message.reply_text("`Restarting Now! Please wait...`")
    hap.restart()


# Set Heroku Var
@Client.on_message(filters.command("setvar") & filters.user(BOT_OWNER))
@_check_heroku
async def setvar(client: Client, message: Message, app_):
    msg = await message.reply_text(message, "`Please Wait...!`")
    heroku_var = app_.config()
    _var = get_text(message)
    if not _var:
        await msg.edit("This is not the way bro! \n\n**Usage:**`/setvar VAR VALUE`")
        return
    if not " " in _var:
        await msg.edit("This is not the way bro! \n\n**Usage:**`/setvar VAR VALUE`")
        return
    var_ = _var.split(" ", 1)
    if len(var_) > 2:
        await msg.edit("This is not the way bro! \n\n**Usage:**`/setvar VAR VALUE`")
        return
    _varname, _varvalue = var_
    await msg.edit(f"**Variable:** `{_varname}` \n**New Value:** `{_varvalue}`")
    heroku_var[_varname] = _varvalue


# Delete Heroku Var
@Client.on_message(filters.command("delvar") & filters.user(BOT_OWNER))
@_check_heroku
async def delvar(client: Client, message: Message, app_):
    msg = await message.reply_text(message, "`Please Wait...!`")
    heroku_var = app_.config()
    _var = get_text(message)
    if not _var:
        await msg.edit("`Give Me a Var Name To Delete!`")
        return
    if not _var in heroku_var:
        await msg.edit("`Lol! This Var Doesn't Even Exists!`")
        return
    await msg.edit(f"Sucessfully Deleted Var Named `{_var}`")
    del heroku_var[_var]
