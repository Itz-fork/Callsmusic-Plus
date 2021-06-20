from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery

OWNER_TEXT = "**Hello My Master 😇!** Please select option from below buttons /n/n ~ @NexaBotsUpdates"

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
    )


# Main owner help menu

@Client.on_callback_query(filters.regex("cbownertools"))
async def cbownertools(_, query: CallbackQuery):
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
