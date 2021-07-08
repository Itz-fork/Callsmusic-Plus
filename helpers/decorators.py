from typing import Callable
from functools import wraps

from pyrogram import Client
from pyrogram.types import Message, CallbackQuery

from helpers.admins import get_administrators
from config import SUDO_USERS


def errors(func: Callable) -> Callable:
    async def decorator(client: Client, message: Message):
        try:
            return await func(client, message)
        except Exception as e:
            await message.reply(f"❗️ {type(e).__name__}: {e}")

    return decorator


def authorized_users_only(func: Callable) -> Callable:
    async def decorator(client: Client, message: Message):
        if message.from_user.id in SUDO_USERS:
            return await func(client, message)

        administrators = await get_administrators(message.chat)

        for administrator in administrators:
            if administrator == message.from_user.id:
                return await func(client, message)

    return decorator


def admin_chack_cb(func):
    @wraps(func)
    async def gaeshit(message: Message, query: CallbackQuery):
        administrators = await get_administrators(query.message.chat)
        if message.from_user.id in SUDO_USERS:
            return await func(message, query)
        for administrator in administrators:
            if administrator == query.from_user.id:
                return await func(message, query)
        else:
            await query.answer("You Go Away, This isn't For You!", show_alert=True)
            return

    return gaeshit
