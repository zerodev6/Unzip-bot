import logging
import asyncio
from pyrogram import Client
from info import API_ID, API_HASH, BOT_TOKEN, STRING_SESSION
from database.users_chats_db import db
from utils import temp

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logging.getLogger("pyrogram").setLevel(logging.WARNING)

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="UnzipBot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="plugins")
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        temp.B_LINK = f"https://t.me/{me.username}"
        logging.info(f"Bot started as @{me.username}")
        
        # Initialize banned users and chats
        banned_users, banned_chats = await db.get_banned()
        temp.BANNED_USERS = banned_users
        temp.BANNED_CHATS = banned_chats
        
        print(f"""
╔═══════════════════════════════════════╗
║                                       ║
║   ✅ BOT STARTED SUCCESSFULLY!       ║
║                                       ║
║   Bot Username: @{me.username.ljust(20)} ║
║   Bot ID: {str(me.id).ljust(27)} ║
║                                       ║
╚═══════════════════════════════════════╝
        """)

    async def stop(self, *args):
        await super().stop()
        logging.info("Bot stopped!")

# User bot for uploads
if STRING_SESSION:
    class UserBot(Client):
        def __init__(self):
            super().__init__(
                name="UserBot",
                api_id=API_ID,
                api_hash=API_HASH,
                session_string=STRING_SESSION
            )

        async def start(self):
            await super().start()
            me = await self.get_me()
            logging.info(f"UserBot started as @{me.username}")

        async def stop(self, *args):
            await super().stop()
            logging.info("UserBot stopped!")

    user_bot = UserBot()
else:
    user_bot = None

bot = Bot()

async def main():
    try:
        await bot.start()
        if user_bot:
            await user_bot.start()
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        pass
    finally:
        await bot.stop()
        if user_bot:
            await user_bot.stop()

if __name__ == "__main__":
    asyncio.run(main())
