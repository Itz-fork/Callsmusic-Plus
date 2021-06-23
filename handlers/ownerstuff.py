# Credits @AbirHasan2005
# CallsMusic-Plus (https://github.com/Itz-fork/Callsmusic-Plus)

import shutil
import psutil

from pyrogram import Client, filters
from handlers.musicdwn import humanbytes
from config import BOT_USERNAME, BOT_OWNER

@Client.on_message(filters.command("botstats") & filters.user(Config.BOT_OWNER))
async def botstats(_, message: Message):
    total, used, free = shutil.disk_usage(".")
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    await message.reply_text(
        text=f"**💫 Bot Stats Of @{BOT_USERNAME} 💫** \n\n**💾 Disk Usage,** \n ↳ **Total Disk Space:** `{total}` \n ↳**Used:** `{used}({disk_usage}%)` \n ↳**Free:** `{free}` \n**🎛 Hardware Usage,** \n ↳**CPU Usage:** `{cpu_usage}%` \n ↳**RAM Usage:** `{ram_usage}%`",
        parse_mode="Markdown",
        quote=True
    )
