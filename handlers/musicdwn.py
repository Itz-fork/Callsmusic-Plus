# (c) @TheHamkerCat , @MrDarkPrince


from __future__ import unicode_literals

import traceback
import os
from random import randint
from urllib.parse import urlparse

import aiofiles
import aiohttp
import ffmpeg
import requests
import wget
import youtube_dl

from pykeyboard import InlineKeyboard
from asyncio import gather
from os import remove
from random import randint
from aiohttp import ClientSession
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton
from youtube_search import YoutubeSearch
from Python_ARQ import ARQ

from config import ARQ_API_URL, ARQ_API_KEY
from helpers.merrors import capture_err
from helpers.modhelps import paste, downloader

is_downloading = False

aiohttpsession = ClientSession()
arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiohttpsession)


VIDEO_DATA = {}

# Convert seconds to mm:ss
async def timeFormat(seconds: int):
    seconds = int(seconds)
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


@Client.on_message(filters.command(['yts', 'yts@MusicsNexa_Bot']))
def song(client, message):

    user_id = message.from_user.id 
    user_name = message.from_user.first_name 
    rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"

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
        rep = f'🎙 **Title**: [{title[:35]}]({link})\n🎬 **Source**: `YouTube`\n⏱️ **Song Duration**: `{duration}`\n👁‍🗨 **Song Views**: `{views}`\n**Uploaded By**: **@MusicsNexa_Bot** \n **Join @NexaBotsUpdates 😉** '
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, thumb=thumb_name, parse_mode='md', title=title, duration=dur)
        m.delete()
    except Exception as e:
        m.edit(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)


# Funtion To Download Song
async def download_song(url):
    song_name = f"{randint(6969, 6999)}.mp3"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(song_name, mode="wb")
                await f.write(await resp.read())
                await f.close()
    return song_name


# Jiosaavn Music


@Client.on_message(filters.command(["saavn", "saavn@MusicsNexa_Bot"]) & ~filters.edited)
@capture_err
async def jssong(_, message):
    global is_downloading
    if len(message.command) < 2:
        await message.reply_text("Command `/saavn` requires an argument.")
        return
    if is_downloading:
        await message.reply_text(
            "Sorry! **Another download is in progress !** Try Again After Sometime!"
        )
        return
    is_downloading = True
    text = message.text.split(None, 1)[1]
    query = text.replace(" ", "%20")
    m = await message.reply_text("**Please Wait! I'm Searching For Your Song 🔎...**")
    try:
        songs = await arq.saavn(query)
        if not songs.ok:
            await message.reply_text(songs.result)
            return
        sname = songs.result[0].song
        slink = songs.result[0].media_url
        ssingers = songs.result[0].singers
        await m.edit("**Downloading Your Song! Please Wait ⏰**")
        song = await download_song(slink)
        await m.edit("**Uploading Your Song! Please Wait ⏰**")
        await message.reply_audio(
            audio=song,
            title=sname,
            performer=ssingers,
        )
        os.remove(song)
        await m.delete()
    except Exception as e:
        is_downloading = False
        await m.edit(str(e))
        return
    is_downloading = False


# Deezer Music


@Client.on_message(filters.command(["deezer", "deezer@MusicsNexa_Bot"]) & ~filters.edited)
@capture_err
async def deezsong(_, message):
    global is_downloading
    if len(message.command) < 2:
        await message.reply_text("command `/deezer` requires an argument.")
        return
    if is_downloading:
        await message.reply_text(
            "Sorry! **Another download is in progress !** Try Again After Sometime!"
        )
        return
    is_downloading = True
    text = message.text.split(None, 1)[1]
    query = text.replace(" ", "%20")
    m = await message.reply_text("**Please Wait! I'm Searching For Your Song 🔎...**")
    try:
        songs = await arq.deezer(query, 1)
        if not songs.ok:
            await message.reply_text(songs.result)
            return
        title = songs.result[0].title
        url = songs.result[0].url
        artist = songs.result[0].artist
        await m.edit("**Downloading Your Song! Please Wait ⏰**")
        song = await download_song(url)
        await m.edit("**Uploading Your Song! Please Wait ⏰**")
        await message.reply_audio(
            audio=song,
            title=title,
            performer=artist,
        )
        os.remove(song)
        await m.delete()
    except Exception as e:
        is_downloading = False
        await m.edit(str(e))
        return
    is_downloading = False


# Song Lyrics


@Client.on_message(filters.command(["lyrics", "lyrics@MusicsNexa_Bot"]))
async def lyrics_func(_, message):
    if len(message.command) < 2:
        await message.reply_text("**Sike That's The Wrong Command Usage!** \nUse `/lyrics` (song name)")
        return
    m = await message.reply_text("**Searching For Song Lyrics**")
    query = message.text.strip().split(None, 1)[1]
    song = await arq.lyrics(query)
    lyrics = song.result
    if len(lyrics) < 4095:
        await m.edit(f"__{lyrics}__")
        return
    lyrics = await paste(lyrics)
    await m.edit(f"**Oops! Lyrics Too Long To Send!** \n**Your Song Lyrics: [Click Here]({lyrics})**")
    
    
    
# Youtube Video Download

@Client.on_message(filters.command("ytvid"))
async def ytvidz(_, message):
    if len(message.command) != 2:
        return await message.reply_text("Lol! Wrong Way bro! Read **/help** section!")
    m = await message.reply_text("`Processing...`")
    url = message.text.split(None, 1)[1]
    results = await arq.ytdl(url)
    if not results.ok:
        return await m.edit(results.result)
    result = results.result
    title = result.title
    thumbnail = result.thumbnail
    duration = result.duration
    video = result.video
    buttons = InlineKeyboard(row_width=3)
    keyboard = []
    for media in video:
        quality = media.quality
        size = media.size
        url = media.url
        format = media.format
        data = str(randint(999, 9999999))
        VIDEO_DATA[data] = {
            "url": url,
            "title": title,
            "quality": quality,
            "duration": duration,
            "format": format,
            "thumbnail": thumbnail,
            "cc": message.from_user.mention if message.from_user else "Anon",
        }
        keyboard.append(
            InlineKeyboardButton(
                text=f"{quality} | {size}", callback_data=f"YtDl {data}"
            )
        )
    buttons.add(*keyboard)
    caption = f"""
**Title:** {title}
**Duration:** {await timeFormat(duration)}
"""
    await message.reply_photo(thumbnail, caption=caption, reply_markup=buttons)
    await m.delete()


@Client.on_callback_query(filters.regex(r"^YtDl"))
async def ytdlCallback(_, cq):
    await cq.message.edit("`Downloading...`")
    data_ = cq.data.split()[1]
    try:
        data = VIDEO_DATA[data_]
        url = data["url"]
        title = data["title"]
        duration = data["duration"]
        format = data["format"]
        thumbnail = data["thumbnail"]
        cc = data["cc"]
        caption = f"""
**Title:** `{title}`
**File Format:** `{format}`
**Duration:** `{await timeFormat(duration)}`
**Requested by:** `{cc}`
        """
        media, thumb = await gather(
            downloader.download(url), downloader.download(thumbnail)
        )
        await cq.message.edit("`Uploading...`")
        if format == "mp3":
            await cq.message.reply_audio(
                media,
                quote=False,
                caption=caption,
                duration=duration,
                thumb=thumb,
                title=title,
            )
        else:
            await cq.message.reply_video(
                media,
                caption=caption,
                quote=False,
                duration=duration,
                supports_streaming=True,
            )
        del VIDEO_DATA[data_]
        remove(thumb)
        remove(media)
        await cq.message.delete()
    except Exception as e:
        e = traceback.format_exc()
        print(e)
        del VIDEO_DATA[data_]
        await cq.message.delete()
