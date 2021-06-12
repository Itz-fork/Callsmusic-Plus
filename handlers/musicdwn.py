# (c) @TheHamkerCat , @MrDarkPrince & TeamDaisyX


from __future__ import unicode_literals

import os
from random import randint
from urllib.parse import urlparse

import aiofiles
import aiohttp
import ffmpeg
import requests
import wget
import youtube_dl

from aiohttp import ClientSession
from pyrogram import Client, filters
from pyrogram.types import Message
from youtube_search import YoutubeSearch
from Python_ARQ import ARQ

from config import ARQ_API_URL, ARQ_API_KEY
from helpers.merrors import capture_err
from helpers.modhelps import paste
from helpers.database import db, Database
from helpers.dbthings import handle_user_status


aiohttpsession = ClientSession()

is_downloading = False
arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiohttpsession)


def get_file_extension_from_url(url):
    url_path = urlparse(url).path
    basename = os.path.basename(url_path)
    return basename.split(".")[-1]

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


@Client.on_message(filters.private)
async def _(bot: Client, cmd: Message):
    await handle_user_status(bot, cmd)

@Client.on_message(filters.command(['yts', 'yst@MusicsNexa_Bot']))
def song(client, message):
    chat_id = message.from_user.id
        if not await db.is_user_exist(chat_id):
            await db.add_user(chat_id)
            await Client.send_message(
        chat_id=Config.LOG_CHANNEL,
        text=f"**📢 News ** \n#New_Music_Lover **Started To Using Meh!** \n\nFirst Name: `{message.from_user.first_name}` \nUser ID: `{message.from_user.id}` \nProfile Link: [{message.from_user.first_name}](tg://user?id={message.from_user.id})",
        parse_mode="markdown"
    )

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
        m.edit('Oops! ❌ Error')
        print(e)

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
    chat_id = message.from_user.id
        if not await db.is_user_exist(chat_id):
            await db.add_user(chat_id)
            await Client.send_message(
        chat_id=Config.LOG_CHANNEL,
        text=f"**📢 News ** \n#New_Music_Lover **Started To Using Meh!** \n\nFirst Name: `{message.from_user.first_name}` \nUser ID: `{message.from_user.id}` \nProfile Link: [{message.from_user.first_name}](tg://user?id={message.from_user.id})",
        parse_mode="markdown"
    )
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
    chat_id = message.from_user.id
        if not await db.is_user_exist(chat_id):
            await db.add_user(chat_id)
            await Client.send_message(
        chat_id=Config.LOG_CHANNEL,
        text=f"**📢 News ** \n#New_Music_Lover **Started To Using Meh!** \n\nFirst Name: `{message.from_user.first_name}` \nUser ID: `{message.from_user.id}` \nProfile Link: [{message.from_user.first_name}](tg://user?id={message.from_user.id})",
        parse_mode="markdown"
    )
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
    chat_id = message.from_user.id
        if not await db.is_user_exist(chat_id):
            await db.add_user(chat_id)
            await Client.send_message(
        chat_id=Config.LOG_CHANNEL,
        text=f"**📢 News ** \n#New_Music_Lover **Started To Using Meh!** \n\nFirst Name: `{message.from_user.first_name}` \nUser ID: `{message.from_user.id}` \nProfile Link: [{message.from_user.first_name}](tg://user?id={message.from_user.id})",
        parse_mode="markdown"
    )
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

@Client.on_message(filters.command(["ytvid", "ytvid@MusicsNexa_Bot"]))
async def ytmusic(client, message: Message):
    chat_id = message.from_user.id
        if not await db.is_user_exist(chat_id):
            await db.add_user(chat_id)
            await Client.send_message(
        chat_id=Config.LOG_CHANNEL,
        text=f"**📢 News ** \n#New_Music_Lover **Started To Using Meh!** \n\nFirst Name: `{message.from_user.first_name}` \nUser ID: `{message.from_user.id}` \nProfile Link: [{message.from_user.first_name}](tg://user?id={message.from_user.id})",
        parse_mode="markdown"
    )
    global is_downloading
    if is_downloading:
        await message.reply_text(
            "Sorry! **Another download is in progress !** Try Again After Sometime!"
        )
        return

    urlissed = get_text(message)

    pablo = await client.send_message(
        message.chat.id, f"`Getting {urlissed} From Youtube Servers. Please Wait For Moment!`"
    )
    if not urlissed:
        await pablo.edit("oWo! Invalid Command Syntax")
        return

    search = SearchVideos(f"{urlissed}", offset=1, mode="dict", max_results=1)
    mi = search.result()
    mio = mi["search_result"]
    mo = mio[0]["link"]
    thum = mio[0]["title"]
    fridayz = mio[0]["id"]
    thums = mio[0]["channel"]
    kekme = f"https://img.youtube.com/vi/{fridayz}/hqdefault.jpg"
    await asyncio.sleep(0.6)
    url = mo
    sedlyf = wget.download(kekme)
    opts = {
        "format": "best",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
        "outtmpl": "%(id)s.mp4",
        "logtostderr": False,
        "quiet": True,
    }
    try:
        is_downloading = True
        with youtube_dl.YoutubeDL(opts) as ytdl:
            infoo = ytdl.extract_info(url, False)
            duration = round(infoo["duration"] / 60)

            if duration > 999:
                await pablo.edit(
                    f"❌ Videos longer than 999 minute(s) aren't allowed, the provided video is {duration} minute(s)"
                )
                is_downloading = False
                return
            ytdl_data = ytdl.extract_info(url, download=True)

    except Exception:
        # await pablo.edit(event, f"**Failed To Download** \n**Error :** `{str(e)}`")
        is_downloading = False
        return

    c_time = time.time()
    file_stark = f"{ytdl_data['id']}.mp4"
    capy = f"**🎧️ Music Video Name:** `{thum}` \n\n**👨‍💻️ Your Keyword:** `{urlissed}` \n**😉️ YouTube Channel:** `{thums}` \n**🔗️ Video Link :** `{mo}`"
    await client.send_video(
        message.chat.id,
        video=open(file_stark, "rb"),
        duration=int(ytdl_data["duration"]),
        file_name=str(ytdl_data["title"]),
        thumb=sedlyf,
        caption=capy,
        supports_streaming=True,
        progress=progress,
        progress_args=(
            pablo,
            c_time,
            f"`Please Wait! I'm Uploading {urlissed} Song From YouTube Music!`",
            file_stark,
        ),
    )
    await pablo.delete()
    is_downloading = False
    for files in (sedlyf, file_stark):
        if files and os.path.exists(files):
            os.remove(files)
