# Don't ask me why this looks like a fucking shit! Just go and make a fukcking PR as i'm fucking lazy to do these things! Fuck Off!

import os
from os import getenv

from pyrogram import Client
from dotenv import load_dotenv
from helpers.modhelps import fetch_heroku_git_url

load_dotenv()

SESSION_NAME = getenv("SESSION_NAME", "session")
BOT_TOKEN = getenv("BOT_TOKEN")

API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")

DURATION_LIMIT = int(getenv("DURATION_LIMIT", "7"))

COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ !").split())

# Your Telegram User ID
BOT_OWNER = int(os.environ.get("BOT_OWNER"))
# Sudo users IDs, They are admins everywhere
SUDO_USERS = list(map(int, getenv("SUDO_USERS").split()))
# Your Bot's Username without "@"
BOT_USERNAME = os.environ.get("BOT_USERNAME")
# Your MongoDB url
DATABASE_URL = os.environ.get("DATABASE_URL")
# Your Log Channel! Make a private channel and get it's ID
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL"))
# If you need to broadcast messages as a copy or Forwarded Message
BROADCAST_AS_COPY = bool(os.environ.get("BROADCAST_AS_COPY", False))
# Thumbnail URL
THUMB_URL = os.environ.get("THUMB_URL", "https://telegra.ph/file/2ed47c81eda6b0624021d.jpg")
# Your Updates Channel! Don't Put Anything If you don't have one
UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", "NexaBotsUpdates")

# Your ARQ API Key
ARQ_API_KEY = getenv("ARQ_API_KEY")
# Don't Change Anything Here
ARQ_API_URL = "https://thearq.tech/"

# Updator Configs
HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None)
HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)
UPSTREAM_REPO = os.environ.get("UPSTREAM_REPO", "https://github.com/Itz-fork/Callsmusic-Plus")
U_BRANCH = "master"
HEROKU_URL = fetch_heroku_git_url(HEROKU_API_KEY, HEROKU_APP_NAME)

# Versions
cp_version = "v2.9.3.2"
nexaub_version = "v0.4"
