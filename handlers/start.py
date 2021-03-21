from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from helpers.filters import command, other_filters, other_filters2


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
