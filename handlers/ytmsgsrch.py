# Original Code From DaisyXMusic
# Copyright (C) 2021  Inuka asith 


# the logging things
import logging

from pyrogram.types import Message
from search_engine_parser import GoogleSearch
from youtube_search import YoutubeSearch
from pyrogram import Client, filters

from helpers.database import db, Database
from helpers.dbthings import handle_user_status
from config import LOG_CHANNEL, BOT_USERNAME, THUMB_URL

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

import pyrogram

logging.getLogger("pyrogram").setLevel(logging.WARNING)


@Client.on_message(filters.private)
async def _(bot: Client, cmd: Message):
    await handle_user_status(bot, cmd)

@Client.on_message(pyrogram.filters.command(["ytsearch", f"ytsearch@{BOT_USERNAME}"]))
async def ytsearch(_, message: Message):
    try:
        if len(message.command) < 2:
            await message.reply_text("`/ytsearch` needs an argument!")
            return
        query = message.text.split(None, 1)[1]
        m = await message.reply_text("**Searching For Your Keyword** 😒")
        results = YoutubeSearch(query, max_results=4).to_dict()
        thumb = THUMB_URL
        i = 0
        text = ""
        while i < 4:
            text += f"📄**Title:** `{results[i]['title']}`\n"
            text += f"  ↳**Duration:** `{results[i]['duration']}`\n"
            text += f"  ↳**Views:** `{results[i]['views']}`\n"
            text += f"  ↳**Channel:** `{results[i]['channel']}`\n"
            text += f"  ↳**Url:** https://youtube.com{results[i]['url_suffix']}\n\n"
            i += 1
        await m.delete()
        await m.reply_photo(thumb, caption=text)
    except Exception as e:
        await message.reply_text(str(e))
