from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery

from config import BOT_OWNER


OWNER_TEXT = "**Hello My Master 😇!** Please select option from below buttons \n\n ~ @NexaBotsUpdates"

OWNER_HELPCB=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⚙️ Owner Tools ⚙️", callback_data="cbownertools"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🧑‍💻 User Help 🧑‍💻", callback_data="cbhelpmenu"
                    )
                ]
            ]
        )


# Main owner help menu

@Client.on_callback_query(filters.regex("cbownertools"))
async def cbownertools(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**He he! You Opened Owner Menu!

Please Select an Option From Below buttons 😊!**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Bans", callback_data="cbbans"
                    ),
                    InlineKeyboardButton(
                        "Unbans", callback_data="cbunbans"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "User Stats", callback_data="cbuserstats"
                    ),
                    InlineKeyboardButton(
                        "Broadcast", callback_data="cbbroadcast"
                    )
                ]
            ]
        )
    )


# Bans
@Client.on_callback_query(filters.regex("cbbans"))
async def cbbans(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>Help For Bans Plugin</b>

**Feature:** Ban Users From Using This Bot!

**Usage:**
    - Send User ID of that user, Ban Duration and Ban Reason with `/ban` command.


**Example:** `/ban 1234567891 2 Test`

 - This will ban user with \nUser ID: `1234567891` \nFor: `2 Days` \nReason will be: `Test`

Made with ❤️ by **@NexaBotsUpdates**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "◀️ Back ◀️", callback_data="cbownertools"
                    )
                ]
            ]
        )
    )


# Unbans
@Client.on_callback_query(filters.regex("cbunbans"))
async def cbunbans(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>Help For Unbans Plugin</b>

**Feature:** Unban Banned Users!

**Usage:**
    - Send User ID of that user with `/unban` command.


**Example:** `/ban 1234567891`

 - This will unban user with User ID: `1234567891`

Made with ❤️ by **@NexaBotsUpdates**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "◀️ Back ◀️", callback_data="cbownertools"
                    )
                ]
            ]
        )
    )

# User Stats
@Client.on_callback_query(filters.regex("cbuserstats"))
async def cbuserstats(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>Help For User Stats Plugin</b>

**Feature:** See How Many Users are using this bot!

**Usage:**
    - Send `/stats` command in Bot PM


Made with ❤️ by **@NexaBotsUpdates**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "◀️ Back ◀️", callback_data="cbownertools"
                    )
                ]
            ]
        )
    )

# Broadcast
@Client.on_callback_query(filters.regex("cbbroadcast"))
async def cbbroadcast(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>Help For Broadcast Plugin</b>

**Feature:** Broadcast Messages To Users Using This Bot!

**Usage:**
    1. If You Set `BROADCAST_AS_COPY` to `False`
     - Reply to a message to Broadcast it.
     
    2. If You Set `BROADCAST_AS_COPY` to `True`
     - Reply to a message to Broadcast it.


Made with ❤️ by **@NexaBotsUpdates**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "◀️ Back ◀️", callback_data="cbownertools"
                    )
                ]
            ]
        )
    )

# Command
@Client.on_message(filters.private & filters.command("modhelp") & filters.user(BOT_OWNER) & ~filters.edited)
async def modhelp(_, message: Message):
    await message.reply_text(OWNER_TEXT, reply_markup=OWNER_HELPCB)
