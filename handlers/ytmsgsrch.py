# Original Code From DaisyXMusic
# Copyright (C) 2021  Inuka asith 


# the logging things
import logging

from pyrogram.types import Message
from search_engine_parser import GoogleSearch
from youtube_search import YoutubeSearch

from pyrogram import Client, filters

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

import pyrogram

logging.getLogger("pyrogram").setLevel(logging.WARNING)

@Client.on_message(pyrogram.filters.command(["ytsearch"]))
async def ytsearch(_, message: Message):
    try:
        if len(message.command) < 2:
            await message.reply_text("`/ytsearch` needs an argument!")
            return
        query = message.text.split(None, 1)[1]
        m = await message.reply_text("**Searching For Your Keyword** 😒")
        results = YoutubeSearch(query, max_results=4).to_dict()
        thumb = "https://telegra.ph/file/a4b7d13da17c3cc828ab9.jpg"
        i = 0
        text = ""
        while i < 4:
            text += f"Title - {results[i]['title']}\n"
            text += f"Duration - {results[i]['duration']}\n"
            text += f"Views - {results[i]['views']}\n"
            text += f"Channel - {results[i]['channel']}\n"
            text += f"https://youtube.com{results[i]['url_suffix']}\n\n"
            i += 1
        await m.delete()
        await m.reply_photo(thumb, caption=text, disable_web_page_preview=True)
    except Exception as e:
        await message.reply_text(str(e))
