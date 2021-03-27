from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import datetime
from database import Database

from helpers.filters import command, other_filters, other_filters2


### Sexy Config Tho ###
db = Database(Config.DATABASE_URL, BOT_USERNAME)

@Client.on_message(command("start") & other_filters2)
async def start(_, message: Message):
    await message.reply_text(
        f"""<b>Hi {message.from_user.first_name} 😉️!</b>

I'm The Nexa Music Bot. Friend of <b>@MusicsNexa_Bot</b> 😏️.

I can play Music In Telegram Groups Via Voice Chat! 😌️.

Made with ❤️ <b>@NexaBotsUpdates</b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🤨️ How To Use Me 🤨️", url="https://telegra.ph/How-To-Use-Music-Nexa-Bot-03-16"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🔰️ My Update Channel ", url="https://t.me/NexaBotsUpdates"
                    ),
                    InlineKeyboardButton(
                        "⚜️ Support Group ⚜️", url="https://t.me/Nexa_bots"
                    )
                ]
            ]
        )
    )


@Client.on_message(command("start") & other_filters)
async def start2(_, message: Message):
    await message.reply_text(
        f"""<b>Hi {message.from_user.first_name} 😉️!</b>

I'm The Nexa Music Bot. Friend of <b>@MusicsNexa_Bot</b> 😏️.

I can play Music In Telegram Groups Via Voice Chat! 😌️.

Made with ❤️ <b>@NexaBotsUpdates</b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🤨️ How To Use Me 🤨️", url="https://telegra.ph/How-To-Use-Music-Nexa-Bot-03-16"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🔰️ My Update Channel ", url="https://t.me/NexaBotsUpdates"
                    ),
                    InlineKeyboardButton(
                        "⚜️ Support Group ⚜️", url="https://t.me/Nexa_bots"
                    )
                ]
            ]
        )
    )

    
@Client.on_message(command("help") & other_filters2)
async def help(_, message: Message):
    await message.reply_text(
        f"""<b>Hi {message.from_user.first_name} 😉️!</b>

Bruh! Do you need Help! 🤔️ yea yea I know it! 🙃️

How To Use Me? 🧐️

<b> 1. Add Me and @NexaMusicAssistant To Your Group!

 2. Give Admin To Me and @NexaMusicAssistant ! </b>
 
 Enjoy! 😌️

Made with ❤️ <b>@NexaBotsUpdates</b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔰️ My Update Channel ", url="https://t.me/NexaBotsUpdates"
                    ),
                    InlineKeyboardButton(
                        "⚜️ Support Group ⚜️", url="https://t.me/Nexa_bots"
                    )
                ]
            ]
        )
    )


@Client.on_message(command("help") & other_filters)
async def help2(_, message: Message):
    await message.reply_text(
        f"""<b>Hi {message.from_user.first_name} 😉️!</b>

Bruh! Do you need Help! 🤔️ yea yea I know it! 🙃️

How To Use Me? 🧐️

<b> 1. Add Me and @NexaMusicAssistant To Your Group!

 2. Give Admin To Me and @NexaMusicAssistant ! </b>
 
 Enjoy! 😌️ Also hit /cmdlist to see available commands! 😶️

Made with ❤️ <b>@NexaBotsUpdates</b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔰️ My Update Channel ", url="https://t.me/NexaBotsUpdates"
                    ),
                    InlineKeyboardButton(
                        "⚜️ Support Group ⚜️", url="https://t.me/Nexa_bots"
                    )
                ]
            ]
        )
    )

@Client.on_message(command("cmdlist") & other_filters2)
async def cmdlist(_, message: Message):
    await message.reply_text(
        f"""<b>Hi {message.from_user.first_name} 😉️!</b>

Here is the list of available commands! 😃️

<code>/play</code> - Reply to youtube url or "/play youtube link"
<code>/skip</code> - Skip currenly playing song!
<code>/pause</code> - Pause currently playing song!
<code>/resume</code> - Resume currently pushed song!
<code>/mute</code> - Mutes Streamer!
<code>/unmute</code> - Unmutes streamer!
 
 Enjoy! 😌️""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔰️ My Update Channel ", url="https://t.me/NexaBotsUpdates"
                    ),
                    InlineKeyboardButton(
                        "⚜️ Support Group ⚜️", url="https://t.me/Nexa_bots"
                    )
                ]
            ]
        )
    )
    
@Client.on_message(command("cmdlist") & other_filters)
async def cmdlist2(_, message: Message):
    await message.reply_text(
        f"""<b>Hi {message.from_user.first_name} 😉️!</b>

Here is the list of available commands! 😃️

<code>/play</code> - Reply to youtube url or "/play youtube link"
<code>/skip</code> - Skip currenly playing song!
<code>/pause</code> - Pause currently playing song!
<code>/resume</code> - Resume currently pushed song!
<code>/mute</code> - Mutes Streamer!
<code>/unmute</code> - Unmutes streamer!
 
 Enjoy! 😌️""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔰️ My Update Channel ", url="https://t.me/NexaBotsUpdates"
                    ),
                    InlineKeyboardButton(
                        "⚜️ Support Group ⚜️", url="https://t.me/Nexa_bots"
                    )
                ]
            ]
        )
    )

 
@Client.on_message(command("credits") & other_filters)
async def credits(_, message: Message):
    await message.reply_text(
        f"""<b>Hi {message.from_user.first_name} 😉️!</b>

This Project Is <b>Not Owned By Me</b> !

Owners are <b><a href="https://github.com/CallsMusic">CallsMusic</a> !

Respect To Code Owners! Not To Me!""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Source Code", url="https://github.com/CallsMusic/Callsmusic"
                    ),
                    InlineKeyboardButton(
                        "⚜️ Owners Channel ⚜️", url="https://t.me/callsmusic"
                    )
                ]
            ]
        )
    )
    

    
@Client.on_message(command("credits") & other_filters2)
async def credits2(_, message: Message):
    await message.reply_text(
        f"""<b>Hi {message.from_user.first_name} 😉️!</b>

This Project Is <b>Not Owned By Me</b> !

Owners are <b><a href="https://github.com/CallsMusic">CallsMusic</a> !

Respect To Code Owners! Not To Me!""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Source Code", url="https://github.com/CallsMusic/Callsmusic"
                    ),
                    InlineKeyboardButton(
                        "⚜️ Owners Channel ⚜️", url="https://t.me/callsmusic"
                    )
                ]
            ]
        )
    )   
    

@Client.on_message(command("search") & other_filters2)
async def search(_, message: Message):
    await message.reply_text(
        "💁🏻‍♂️ Do you want to search for a YouTube video?",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "✅ Yes", switch_inline_query_current_chat=""
                    ),
                    InlineKeyboardButton(
                        "No ❌", callback_data="close"
                    )
                ]
            ]
        )
    )
    
    

@Client.on_message(command("search") & other_filters)
async def search2(_, message: Message):
    await message.reply_text(
        "💁🏻‍♂️ Do you want to search for a YouTube video?",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "✅ Yeah", switch_inline_query_current_chat=""
                    ),
                    InlineKeyboardButton(
                        "Nope ❌", callback_data="close"
                    )
                ]
            ]
        )
    )

    ################## BETA TIME ######################
    
    @Client.on_message(command("donate") & other_filters2)
async def donate(_, message: Message):
    await message.reply_text(
        f"""<b>Hi {message.from_user.first_name} 😉️!</b>

I'm The Nexa Music Bot. Friend of <b>@MusicsNexa_Bot</b> 😏️.

My Master Needs Your Donations To Keep This Service Alive & Free! 😔️

You can Donate Him via below buttons

Made with ❤️ <b>@NexaBotsUpdates</b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "💰️ Donate 💰️", url="https://paypal.com"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🔰️ My Update Channel ", url="https://t.me/NexaBotsUpdates"
                    ),
                    InlineKeyboardButton(
                        "⚜️ Support Group ⚜️", url="https://t.me/Nexa_bots"
                    )
                ]
            ]
        )
    )


@Client.on_message(command("donate") & other_filters)
async def donate2(_, message: Message):
    await message.reply_text(
        f"""<b>Hi {message.from_user.first_name} 😉️!</b>

I'm The Nexa Music Bot. Friend of <b>@MusicsNexa_Bot</b> 😏️.

My Master Needs Your Donations To Keep This Service Alive & Free! 😔️

You can Donate Him via below buttons

Made with ❤️ <b>@NexaBotsUpdates</b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "💰️ Donate 💰️", url="https://paypal.com"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🔰️ My Update Channel ", url="https://t.me/NexaBotsUpdates"
                    ),
                    InlineKeyboardButton(
                        "⚜️ Support Group ⚜️", url="https://t.me/Nexa_bots"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Close This ❌", callback_data="close"
                    )
                ]
            ]
        )
    )

    
    

    

#################################### Oh Shit! Fucked Again Fucking BETA Version ###############################

@Client.on_message(filters.private & filters.command("status") & filters.user(BOT_OWNER))
async def sts(c, m):
	total_users = await db.total_users_count()
	await m.reply_text(text=f"**Total Users :** `{total_users}`", parse_mode="Markdown", quote=True)
    
    
