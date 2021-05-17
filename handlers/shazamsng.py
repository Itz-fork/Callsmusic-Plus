# This file is a part of DaisyX Telegram Bot

import os
from json import JSONDecodeError

import requests

# import ffmpeg
from pyrogram import Client, filters

from helpers.modhelps import edit_or_reply, fetch_audio

@Client.on_message(filters.command(["shazam", "shazam@MusicsNexa_bot"]))
async def shazamm(client, message):
    sed = await edit_or_reply(message, "`Shazaming In Progress!`")
    if not message.reply_to_message:
        await sed.edit("Reply To The Audio.")
        return
    if os.path.exists("friday.mp3"):
        os.remove("friday.mp3")
    kkk = await fetch_audio(client, message)
    downloaded_file_name = kkk
    f = {"file": (downloaded_file_name, open(downloaded_file_name, "rb"))}
    await sed.edit("**Searching For This Song In Friday's DataBase.**")
    r = requests.post("https://starkapi.herokuapp.com/shazam/", files=f)
    try:
        xo = r.json()
    except JSONDecodeError:
        await sed.edit(
            "`Seems Like Our Server Has Some Issues, Please Try Again Later!`"
        )
        return
    if xo.get("success") is False:
        await sed.edit("`Song Not Found In Database. Please Try Again.`")
        os.remove(downloaded_file_name)
        return
    xoo = xo.get("response")
    zz = xoo[1]
    zzz = zz.get("track")
    zzz.get("sections")[3]
    nt = zzz.get("images")
    image = nt.get("coverarthq")
    by = zzz.get("subtitle")
    title = zzz.get("title")
    messageo = f"""<b>Song Shazamed.</b>
<b>Song Name : </b>{title}
<b>Song By : </b>{by}
"""
    await client.send_photo(message.chat.id, image, messageo, parse_mode="HTML")
    os.remove(downloaded_file_name)
    await sed.delete()
