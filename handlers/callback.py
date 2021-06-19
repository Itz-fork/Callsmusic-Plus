from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery

from handlers.start import FRIEND_BOT

# close calllback

@Client.on_callback_query(filters.regex("close"))
async def close(_, query: CallbackQuery):
    await query.message.delete()


# Start callback 

@Client.on_callback_query(filters.regex("cbstart"))
async def startcb(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>Hi {query.message.from_user.mention} 😉️!</b>

I'm The Nexa Music Bot! A Powerful Bot to Play Music in Your Group Voice Chat 😇!

Also I have more features! Please hit on **/help** to see them 😘!

Made with ❤️ <b>@NexaBotsUpdates</b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ Add Me To Your Group ➕", url="https://t.me/MusicsNexa_bot?startgroup=true"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "👮‍♂️ Help Menu 👮‍♂️", callback_data="cbhelpmenu"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🔰️ My Update Channel 🔰️", url="https://t.me/NexaBotsUpdates"
                    ),
                    InlineKeyboardButton(
                        "⚜️ Support Group ⚜️", url="https://t.me/Nexa_bots"
                    )
                ]
            ]
        )
    )
    

# Help Callback Menu

@Client.on_callback_query(filters.regex("cbhelpmenu"))
async def cbhelpmenu(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>Hi {query.message.from_user.mention} 😉️!</b>

**Here is the Help Menu For This Bot 😊!**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🤔 How To Use Me 🤔", callback_data="cbhowtouse"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Get Lyrics", callback_data="cbgetlyrics"
                    ),
                    InlineKeyboardButton(
                        "YT Search", callback_data="cbytsearch"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Music Downloader", callback_data="cbmusicdown"
                    ),
                    InlineKeyboardButton(
                        "YT Video Downloader", callback_data="cbytviddown"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Delete Commands", callback_data="cbdelcmds"
                    ),
                    InlineKeyboardButton(
                        "Quotely", callback_data="cbquotely"
                    )
                ]
            ]
        )
    )


# Lyrics Module Help

@Client.on_callback_query(filters.regex("cbgetlyrics"))
async def cbgetlyrics(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>Help For Lyrics Plugin</b>

**Feature:** Get Lyrics For Provided Song Name!

**Usage:**
    - Send Your Song Name with `/lyrics` command.

**Example:** `/lyrics faded`

Made with ❤️ by **@NexaBotsUpdates**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "◀️ Back ◀️", callback_data="cbhelpmenu"
                    )
                ]
            ]
        )
    )


# Yt Search Module Help

@Client.on_callback_query(filters.regex("cbytsearch"))
async def cbytsearch(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>Help For YT Search Plugin</b>

**Feature:** Search Youtube Videos Inline or Using a Command!

**Usage:**
    1. For Inline Search Feature,
     - Type `@MusicsNexa_Bot` in any chat then type ` `(space) and search.
    
    2. For Search Via Command,
     - Send `/ytsearch` command with your keyword.

**Example:**
    1. Example For Inline Search
     - `@MusicsNexa_Bot faded`
    
    2. Example For Search via Command
     - `/ytsearch faded`

Made with ❤️ by **@NexaBotsUpdates**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "◀️ Back ◀️", callback_data="cbhelpmenu"
                    )
                ]
            ]
        )
    )
    
    
# Music Downloader Help

@Client.on_callback_query(filters.regex("cbmusicdown"))
async def cbmusicdown(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>Help For Music Downloader Plugin</b>

**Feature:** Download Music As Audio From YouTube, Saavn, Deezer

**Usage:**
    1. For Youtube Audio Download,
      - Send Your Song Name with `/yts` command.
    
    2. For Saavn Audio Download,
      - Send Your Song Name with `/saavn` command.
    
    3. For Deezer Audio Download,
      - Send Your Song Name with `/deezer` command.

**Example:**
    1. Example For Youtube Audio Download,
      - `/yts alone`
    
    2. Example For Saavn Audio Download,
      - `/saavn faded`
    
    3. Example For Deezer Audio Download,
      - `/deezer unity`

Made with ❤️ by **@NexaBotsUpdates**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "◀️ Back ◀️", callback_data="cbhelpmenu"
                    )
                ]
            ]
        )
    )


# YT Video Downloader Help

@Client.on_callback_query(filters.regex("cbytviddown"))
async def cbytviddown(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>Help For YT Video Downloader Plugin</b>

**Feature:** Download Youtube Videos For Provided Name!

**Usage:**
    - Send Your Youtube Video Name with `/ytvid` command.

**Example:** `/ytvid faded`

Made with ❤️ by **@NexaBotsUpdates**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "◀️ Back ◀️", callback_data="cbhelpmenu"
                    )
                ]
            ]
        )
    )


# Delete Command Help

@Client.on_callback_query(filters.regex("cbdelcmds"))
async def cbdelcmds(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>Help For Delete Command Plugin</b>

**Feature:** Delete Commands Sent By Users Releated To This Bot!

**Usage:**
    1. To Turn On This,
      - Send `/delcmd on` command.
    
    2. To Turn Off This,
      - Send `/delcmd off` command.

Made with ❤️ by **@NexaBotsUpdates**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "◀️ Back ◀️", callback_data="cbhelpmenu"
                    )
                ]
            ]
        )
    )


# Quotely Help

@Client.on_callback_query(filters.regex("cbquotely"))
async def cbquotely(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>Help For Quotely Plugin</b>

**Feature:** Quote Messages Like Quotely Bot!

**Usage:**
    1. To Quote One Message,
      - `/q` reply to a text message
      
    2. To Quote More Than One Message,
      - `/q` [Integer] reply to a text message
     
    3. To Quote Message with Reply
      - `/q r` reply to a text message

**Example:**
    1. Example Quote One Message,
      - `/q` reply to a text message
      
    2. Example Quote More Than One Message,
      - `/q 2` reply to a text message
     
    3. Example Quote Message with Reply,
      - `/q r` reply to a text message

Made with ❤️ by **@NexaBotsUpdates**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "◀️ Back ◀️", callback_data="cbhelpmenu"
                    )
                ]
            ]
        )
    )
