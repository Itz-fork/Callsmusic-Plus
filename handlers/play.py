from os import path

from pyrogram import Client, filters # Ik this is weird as this shit is already imported in line 16! anyway ... Fuck Off!
from pyrogram.types import Message, Voice
from youtube_search import YoutubeSearch

from callsmusic import callsmusic, queues

import converter
import youtube
import aiohttp

from helpers.database import db, Database
from helpers.dbthings import handle_user_status
from config import DURATION_LIMIT, LOG_CHANNEL, BOT_USERNAME, THUMB_URL
from helpers.errors import DurationLimitError
from helpers.filters import command, other_filters
from helpers.decorators import errors


@Client.on_message(filters.private)
async def _(bot: Client, cmd: command):
    await handle_user_status(bot, cmd)

@Client.on_message(command(["play", f"play@{BOT_USERNAME}"]) & other_filters)
@errors
async def play(_, message: Message):
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
    else:
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

        if offset in (None,):
            await response.edit_text(f"`Lol! You did not give me anything to play!`")
            return

        url = text[offset:offset + length]
        file = await converter.convert(youtube.download(url))

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


# Pros reading this code be like: Wait wut? wtf? dumb? Me gonna die, lol etc.

@Client.on_message(command(["nplay", f"nplay@{BOT_USERNAME}"]) & other_filters)
@errors
async def nplay(_, message: Message):
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply('**Please Wait! Im Searching For Your Song 🔎...**')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        #print(results)
        title = results[0]["title"][:40]       
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f'thumb{title}.jpg'
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, 'wb').write(thumb.content)


        duration = results[0]["duration"]
        url_suffix = results[0]["url_suffix"]
        views = results[0]["views"]

    except Exception as e:
        m.edit(
            "Sorry To Say but I can't find anything ❌!\n\nTry Another Keyword! Btw you spelled it properly 🤔?"
        )
        print(str(e))
        return
    m.edit("**Downloading Your Song! Please Wait ⏰**")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        m.delete()
    except Exception as e:
        m.edit(e)

    try:
        os.remove(thumb_name)
    except Exception as e:
        print(e)
        
        file = await converter.convert(audio_file)

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
