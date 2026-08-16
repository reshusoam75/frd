import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

from pyrogram import Client
from telethon.sync import TelegramClient
from decouple import config

import logging
import sys
import configparser


logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.WARNING
)


# =========================
# Render Health Server
# =========================

PORT = int(os.environ.get("PORT", 8080))


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot is running")

    def log_message(self, format, *args):
        pass


def run_health_server():
    server = HTTPServer(("0.0.0.0", PORT), HealthHandler)
    server.serve_forever()


threading.Thread(
    target=run_health_server,
    daemon=True
).start()


# =========================
# Variables
# =========================

API_ID = config("API_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
BOT_TOKEN = config("BOT_TOKEN", default=None)
SESSION = config("SESSION", default=None)
FORCESUB = config("FORCESUB", default=None)
AUTH = config("AUTH", default=None, cast=int)


# =========================
# Proxy
# =========================

PROXY_TYPE = config("PROXY_TYPE", default=None)
PROXY_HOST = config("PROXY_HOST", default=None)
PROXY_PORT = config("PROXY_PORT", default=0, cast=int)

client_proxy = None
TelegramClient_proxy = None

if PROXY_TYPE and PROXY_HOST and PROXY_PORT != 0:
    client_proxy = {
        "scheme": PROXY_TYPE,
        "hostname": PROXY_HOST,
        "port": PROXY_PORT,
    }

    TelegramClient_proxy = (
        PROXY_TYPE,
        PROXY_HOST,
        PROXY_PORT
    )


# =========================
# Telethon Bot
# =========================

bot = TelegramClient(
    "bot",
    API_ID,
    API_HASH,
    proxy=TelegramClient_proxy
).start(
    bot_token=BOT_TOKEN
)


# =========================
# Pyrogram Userbot
# =========================

userbot = Client(
    "saverestricted",
    session_string=SESSION,
    api_hash=API_HASH,
    api_id=API_ID,
    proxy=client_proxy
)


config_parser = configparser.ConfigParser()
config_parser.read("config.ini")


try:
    userbot.start()
except BaseException:
    print("Userbot Error ! Have you added SESSION while deploying??")
    sys.exit(1)


# =========================
# Pyrogram Bot
# =========================

Bot = Client(
    "SaveRestricted",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
    proxy=client_proxy
)


try:
    Bot.start()
except Exception as e:
    print(e)
    sys.exit(1)
