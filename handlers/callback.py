from asyncio import QueueEmpty

from callsmusic import callsmusic, queues

from helpers.filters import command
from helpers.decorators import errors, authorized_users_only

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, Message


@Client.on_callback_query(("close"))
async def close(_, query: CallbackQuery):
    await query.message.delete()


@Client.on_callback_query(("pause"))
@errors
@authorized_users_only
async def pause(_, query: CallbackQuery):
    if callsmusic.pause(message.chat.id):
        await query.message.edit_text("⏸ Paused")
    else:
        await query.edit_text("❗️ Nothing is playing")


@Client.on_callback_query(("resume"))
@errors
@authorized_users_only
async def resume(_, query: CallbackQuery):
    if callsmusic.resume(message.chat.id):
        await query.message.edit_text("🎧 Resumed")
    else:
        await query.message.edit_text("❗️ Nothing is paused")


@Client.on_callback_query(("stop"))
@errors
@authorized_users_only
async def stop(_, query: CallbackQuery):
    if message.chat.id not in callsmusic.active_chats:
        await query.message.edit_text("❗️ Nothing is playing")
    else:
        try:
            queues.clear(message.chat.id)
        except QueueEmpty:
            pass

        await callsmusic.stop(message.chat.id)
        await query.message.edit_text("✅ Cleared the queue and left the Voice Chat!")


@Client.on_callback_query(("skip"))
@errors
@authorized_users_only
async def skip(_, query: CallbackQuery):
    if message.chat.id not in callsmusic.active_chats:
        await query.message.edit_text("❗️ Nothing is playing")
    else:
        queues.task_done(message.chat.id)

        if queues.is_empty(message.chat.id):
            await callsmusic.stop(message.chat.id)
        else:
            await callsmusic.set_stream(
                message.chat.id, queues.get(message.chat.id)["file"]
            )

        await query.message.edit_text("Skipped.")


@Client.on_callback_query(("mute"))
@errors
@authorized_users_only
async def mute(_, query: CallbackQuery):
    result = callsmusic.mute(message.chat.id)

    if result == 0:
        await query.message.edit_text("🔇 Muted")
    elif result == 1:
        await query.message.edit_text("🔇 Already muted")
    elif result == 2:
        await query.message.edit_text("❗️ Not in voice chat")


@Client.on_callback_query(("unmute"))
@errors
@authorized_users_only
async def unmute(_, query: CallbackQuery):
    result = callsmusic.unmute(message.chat.id)

    if result == 0:
        await query.message.edit_text("🔈 Unmuted")
    elif result == 1:
        await query.message.edit_text("🔈 Already unmuted")
    elif result == 2:
        await query.message.edit_text("❗️ Not in voice chat")
