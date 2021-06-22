# This File Is Made and Owned By @TheHamkerCat and @TeamDaisyX

import socket

from helpers import aiodownloader

async def _netcat(host, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(content.encode())
    s.shutdown(socket.SHUT_WR)
    while True:
        data = s.recv(4096).decode("utf-8").strip("\n\x00")
        if not data:
            break
        return data
    s.close()


async def paste(content):
    link = await _netcat("ezup.dev", 9999, content)
    return link

# Downloader
downloader = aiodownloader.Handler()

async def download_url(url: str):
    loop = get_running_loop()
    file = await loop.run_in_executor(None, download, url)
    return file
