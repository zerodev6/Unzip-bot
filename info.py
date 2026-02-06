import os
from os import environ

# Bot Configuration
API_ID = int(environ.get("API_ID", ""))
API_HASH = environ.get("API_HASH", "")
BOT_TOKEN = environ.get("BOT_TOKEN", "")
STRING_SESSION = environ.get("STRING_SESSION", "")

# Database
DATABASE_URI = environ.get("DATABASE_URI", "")
DATABASE_NAME = environ.get("DATABASE_NAME", "unzip_bot")

# Admins
ADMINS = [int(admin) if admin.isdigit() else admin for admin in environ.get('ADMINS', '').split()]

# Channels
FORCE_SUB_CHANNELS = [
    "zerodev2",
    "mvxyoffcail"
]

# URLs
SUPPORT_CHAT = environ.get("SUPPORT_CHAT", "https://t.me/zerodev2")
OWNER_USERNAME = "@Venuboyy"

# Limits
FREE_USER_LIMIT = 2 * 1024 * 1024 * 1024  # 2GB in bytes
PREMIUM_USER_LIMIT = 4 * 1024 * 1024 * 1024  # 4GB in bytes

# Premium Plans (in Telegram Stars)
STAR_PREMIUM_PLANS = {
    100: "1 month",
    250: "3 months",
    400: "6 months",
    700: "1 year"
}

# Logs
PREMIUM_LOGS = int(environ.get("PREMIUM_LOGS", "0"))

# Images
SUBSCRIPTION = "https://i.ibb.co/gMrpRQWP/photo-2025-07-09-05-21-32-7524948058832896004.jpg"
FORCE_SUB_IMAGE = "https://i.ibb.co/pr2H8cwT/img-8312532076.jpg"
WELCOME_IMAGE_API = "https://api.aniwallpaper.workers.dev/random?type=girl"

# Download/Upload Settings
DOWNLOAD_LOCATION = "./downloads"
CHUNK_SIZE = 1024 * 1024  # 1MB chunks for better speed
