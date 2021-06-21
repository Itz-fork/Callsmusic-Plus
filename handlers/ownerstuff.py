import os
import shlex
import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message
from typing import Tuple


async def execute(cmd: str) -> Tuple[str, str, int, int]:
    """Run Commands"""
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )

# Command to update yt-dl
@Client.on_message(filters.command(["uytdl", "uytdl@MusicsNexa_bot"]))
async def uytdl(_, message: Message):
  await execute("sudo youtube-dl -U")
