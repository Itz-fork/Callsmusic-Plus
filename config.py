# Don't ask me why this looks like a fucking shit! Just go and make a fukcking PR as i'm fucking lazy to do these things! Fuck Off!

import os
from os import getenv

from dotenv import load_dotenv

load_dotenv()

SESSION_NAME = getenv("SESSION_NAME", "session")
BOT_TOKEN = getenv("BOT_TOKEN")

API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")

DURATION_LIMIT = int(getenv("DURATION_LIMIT", "7"))

COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ !").split())

BOT_OWNER = int(os.environ.get("BOT_OWNER"))
SUDO_USERS = list(map(int, getenv("SUDO_USERS").split()))
BOT_USERNAME = os.environ.get("BOT_USERNAME")
DATABASE_URL = os.environ.get("DATABASE_URL")
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL"))

ARQ_API_KEY = getenv("ARQ_API_KEY")
# Don't Change Anything Here
ARQ_API_URL = "http://thearq.tech"
