from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery


@Client.on_callback_query(filters.regex("close"))
async def close(_, query: CallbackQuery):
    await query.message.delete()

# Command list callback

@Client.on_callback_query(filters.regex("cmdlistcb"))
async def cmdlistcb(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>Hi {message.from_user.first_name} 😉️!</b>

Here is the list of available commands! 😃️

• **Group Admin Only Commands 👮 ✓,**

 ➲ <code>/play</code> - Reply to supported url or "/play supported url"
 ➲ <code>/skip</code> - Skip currenly playing song!
 ➲ <code>/pause</code> - Pause currently playing song!
 ➲ <code>/resume</code> - Resume currently pushed song!
 ➲ <code>/mute</code> - Mutes Streamer!
 ➲ <code>/unmute</code> - Unmutes streamer!
 ➲ <code>/joingrp</code> - To Add Streamer Account To Your Group!
 ➲ <code>/leavegrp</code> - To Remove Streamer Account From Your Group!


• **Group Members Commands 👮 ✓,**

 ➲ <code>/vc</code> - Give voice chat link of your group! (Only For Public Groups)
 ➲ <code>/yts (song name)</code> - Download song by it's name!
 ➲ <code>/ytvid (song name)</code> - Download Videos From YouTube!
 ➲ <code>/saavn (song name)</code> - Download Songs From Saavn!
 ➲ <code>/deezer (song namme)</code> - Download Songs From Deezer!

 
Made with ❤️ by **@NexaBotsUpdates**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "👀️ Supported Sites 👀️", url="https://ytdl-org.github.io/youtube-dl/supportedsites.html"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "⚜️ Support Group ⚜️", url="https://t.me/Nexa_bots"
                    )
                ],
                [
                    InlineKeyboardButton(
                    "🔰️ My Update Channel 🔰️", url="https://t.me/NexaBotsUpdates"
                    )
                ]
            ]
        )
    )
