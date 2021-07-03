from os import path

from pyrogram import Client, filters # Ik this is weird as this shit is already imported in line 16! anyway ... Fuck Off!
from pyrogram.types import Message, Voice
from youtube_search import YoutubeSearch

from callsmusic import callsmusic, queues

import converter
import youtube
import requests
import aiohttp

from helpers.database import db, Database
from helpers.dbthings import handle_user_status
from config import DURATION_LIMIT, LOG_CHANNEL, BOT_USERNAME, THUMB_URL
from helpers.errors import DurationLimitError
from helpers.filters import command, other_filters
from helpers.decorators import errors
from converter.converter import convert
from . import que


@Client.on_message(filters.private)
async def _(bot: Client, cmd: command):
    await handle_user_status(bot, cmd)

@Client.on_message(command(["play", f"play@{BOT_USERNAME}"]) & other_filters)
@errors
async def play(_, message: Message):
        messages = [message]
        text = ""
        offset = None
        length = None

        if message.reply_to_message:
            messages.append(message.reply_to_message)

        for _message in messages:
            if offset:
                break

            if _message.entities:
                for entity in _message.entities:
                    if entity.type == "url":
                        text = _message.text or _message.caption
                        offset, length = entity.offset, entity.length
                        break

        if offset not in (None,):
            url = text[offset:offset + length]
            file = await converter.convert(youtube.download(url))
       
        if offset in (None,):
            query = ""
            for i in message.command[1:]:
                query += " " + str(i)
                print(query)
                ydl_opts = {"format": "bestaudio[ext=m4a]"}
                try:
                    results = YoutubeSearch(query, max_results=1).to_dict()
                    url = f"https://youtube.com{results[0]['url_suffix']}"
                    # print(results)
                    title = results[0]["title"][:40]
                    thumbnail = results[0]["thumbnails"][0]
                    thumb_name = f"thumb{title}.jpg"
                    thumb = requests.get(thumbnail, allow_redirects=True)
                    open(thumb_name, "wb").write(thumb.content)
                    duration = results[0]["duration"]
                    results[0]["url_suffix"]
                    views = results[0]["views"]
                except Exception as e:
                    await response.edit(
                        f"**Error:** {e}"
                    )
                    print(str(e))
                    return
                try:    
                    secmul, dur, dur_arr = 1, 0, duration.split(':')
                    for i in range(len(dur_arr)-1, -1, -1):
                        dur += (int(dur_arr[i]) * secmul)
                        secmul *= 60
                        if (dur / 60) > DURATION_LIMIT:
                            await response.edit(f"Bruh! Videos longer than `{DURATION_LIMIT}` minute(s) aren’t allowed, the provided audio is {round(audio.duration / 60)} minute(s) 😒")
                            return
                except:
                    pass
                
            file = await convert(youtube.download(url))

    else:
        audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
        response = await message.reply_text("**Processing Your Song 😇...**")
        
        if audio:
            if round(audio.duration / 60) > DURATION_LIMIT:
                raise DurationLimitError(
                    f"Bruh! Videos longer than `{DURATION_LIMIT}` minute(s) aren’t allowed, the provided audio is {round(audio.duration / 60)} minute(s) 😒"
                )
                
                file_name = audio.file_unique_id + "." + (
                    (
                        audio.file_name.split(".")[-1]
                    ) if (
                        not isinstance(audio, Voice)
                    ) else "ogg"
                )
                
                file = await converter.convert(
                    (
                        await message.reply_to_message.download(file_name)
                    )
                    if (
                        not path.isfile(path.join("downloads", file_name))
                    ) else file_name
                )
    
    if message.chat.id in callsmusic.active_chats:
        thumb = THUMB_URL
        position = await queues.put(message.chat.id, file=file)
        MENTMEH = message.from_user.mention()
        await response.delete()
        await message.reply_photo(thumb, caption=f"**Your Song Queued at position** `{position}`! \n**Requested by: {MENTMEH}**")
    else:
        thumb = THUMB_URL
        await callsmusic.set_stream(message.chat.id, file)
        await response.delete()
        await message.reply_photo(thumb, caption="**Playing Your Song 🎧...** \n**Requested by: {}**".format(message.from_user.mention()))
