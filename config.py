import os
from os import environ

class Config:
    # Required Environment Variables
    API_ID = "20288994"
    API_HASH = "d702614912f1ad370a0d18786002adbf"
    BOT_TOKEN = "8248221325:AAFLPwvn5wGzxYzDBs6GcZHVlqdpobm_X1w"
    
    # User Session String for uploading large files (up to 4GB)
    # Generate using: https://replit.com/@subinps/generatepyrogramsession
    SESSION_STRING = environ.get("SESSION_STRING", "")
    
    # Database
    DATABASE_URL = environ.get("DATABASE_URL", "")
    
    # Admin Configuration
    ADMINS = list(set(int(x) for x in environ.get("ADMINS", "").split()))
    
    # Channels Configuration
    FORCE_SUB_CHANNELS = environ.get("FORCE_SUB_CHANNELS", "").split()
    
    # Logs
    PREMIUM_LOGS = int(environ.get("PREMIUM_LOGS", "0"))
    
    # Premium Plans (Star prices)
    STAR_PREMIUM_PLANS = {
        100: "1 month",
        250: "3 months",
        450: "6 months",
        800: "1 year"
    }
    
    # File Size Limits (in bytes)
    MAX_FILE_SIZE_FREE = 2 * 1024 * 1024 * 1024  # 2GB
    MAX_FILE_SIZE_PREMIUM = 4 * 1024 * 1024 * 1024  # 4GB
    
    # Other Settings
    DOWNLOAD_LOCATION = "./downloads/"
    BOT_USERNAME = environ.get("BOT_USERNAME", "")
