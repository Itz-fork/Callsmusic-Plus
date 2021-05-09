from os import path

from pyrogram import Client
from pyrogram.types import Message, Voice

from callsmusic import callsmusic, queues

import converter
import youtube
import aiohttp

from config import DURATION_LIMIT
from helpers.errors import DurationLimitError
from helpers.filters import command, other_filters
from helpers.decorators import errors

@Client.on_message(command("play") & other_filters)
@errors
async def play(_, message: Message):
    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None

    response = await message.reply_text("**Processing Your Song...** 😇")

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"Bruh! Videos longer than {DURATION_LIMIT} minute(s) aren’t allowed, the provided audio is {round(audio.duration / 60)} minute(s) 😒"
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
            await response.edit_text("Lol! `You did not give me anything to play!`")
            return

        url = text[offset:offset + length]
        file = await converter.convert(youtube.download(url))
        WHOREQED = message.from_user.first_name
        thumb = "https://telegra.ph/file/a4b7d13da17c3cc828ab9.jpg"
        queuedtxt = "**Your Song Queued at position {position}!**  **Requested by**: **{WHOREQED}**"
        playtxt = "**Playing Your Song 🎧...** **Requested by**: **{WHOREQED}**"

    if message.chat.id in callsmusic.active_chats:
        position = await queues.put(message.chat.id, file=file)
        await response.delete()
        await response.reply_photo(thumb, caption=queuedtxt)
    else:
        await callsmusic.set_stream(message.chat.id, file)
        await response.delete()
        await response.reply_photo(thumb, caption=playtxt)
