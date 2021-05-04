from pyrogram import Client as Bot

from callsmusic import run
from config import API_ID, API_HASH, BOT_TOKEN


bot = Bot(
    ":memory:",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="handlers")
)

## Fucked Command ##

@Bot.on_message(filters.command("update") & filters.user(SUDOERS))
async def update_restart(_, message):
    await send(
        f'```{subprocess.check_output(["git", "pull"]).decode("UTF-8")}```'
    )
    os.execvp(
        f"python{str(pyver.split(' ')[0])[:3]}",
        [f"python{str(pyver.split(' ')[0])[:3]}", "main.py"],
    )

bot.start()
run()
