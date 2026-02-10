import os
import time
import asyncio
import shutil
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import FloodWait
import zipfile
import rarfile
import py7zr
import tarfile
from config import Config
from database import db
from script import script
from utils import (
    get_readable_file_size, 
    get_readable_time, 
    progress_for_pyrogram,
    check_user_subscription
)
import logging

logging.basicConfig(level=logging.INFO)

# Bot instance
app = Client(
    "UnzipBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    workers=50,
    sleep_threshold=10
)

# User Client for uploading large files (up to 4GB)
# This uses session string to bypass bot API 50MB upload limit
user_client = None
if Config.SESSION_STRING:
    try:
        user_client = Client(
            "UserSession",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            session_string=Config.SESSION_STRING,
            workers=50,
            sleep_threshold=10
        )
        logging.info("User client initialized successfully")
    except Exception as e:
        logging.error(f"Failed to initialize user client: {e}")
        user_client = None
else:
    logging.warning("No SESSION_STRING provided - large file uploads may be limited")

# Store user data temporarily
user_data = {}

@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    user_id = message.from_user.id
    
    # Check force subscription
    if not await check_user_subscription(client, message):
        return
    
    # Show loading animation
    loading_msg = await message.reply("⏳")
    await asyncio.sleep(2)
    await loading_msg.delete()
    
    # Add user to database
    await db.add_user(user_id)
    
    # Get random welcome image
    welcome_image = script.WELCOME_IMAGE
    
    # Welcome message
    buttons = [
        [
            InlineKeyboardButton("📚 ʜᴇʟᴘ", callback_data="help"),
            InlineKeyboardButton("ℹ️ ᴀʙᴏᴜᴛ", callback_data="about")
        ],
        [
            InlineKeyboardButton("💎 ᴘʀᴇᴍɪᴜᴍ", callback_data="premium_info"),
            InlineKeyboardButton("👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ", url=f"https://t.me/{script.ADMIN_USERNAME.replace('@', '')}")
        ]
    ]
    
    await message.reply_photo(
        photo=welcome_image,
        caption=script.START_TXT.format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_message(filters.command("help") & filters.private)
async def help_command(client, message):
    if not await check_user_subscription(client, message):
        return
    
    buttons = [
        [InlineKeyboardButton("🏠 ʜᴏᴍᴇ", callback_data="start")],
        [InlineKeyboardButton("💎 ɢᴇᴛ ᴘʀᴇᴍɪᴜᴍ", callback_data="premium_info")]
    ]
    
    await message.reply_text(
        script.HELP_TXT,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_message(filters.command("about") & filters.private)
async def about_command(client, message):
    if not await check_user_subscription(client, message):
        return
    
    me = await client.get_me()
    buttons = [[InlineKeyboardButton("🏠 ʜᴏᴍᴇ", callback_data="start")]]
    
    await message.reply_text(
        script.ABOUT_TXT.format(me.username, me.first_name, script.ADMIN_USERNAME),
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )

@app.on_message(filters.command("info") & filters.private)
async def user_info(client, message):
    if not await check_user_subscription(client, message):
        return
    
    user = message.from_user
    user_id = user.id
    
    # Get user data from database
    user_data = await db.get_user(user_id)
    is_premium = await db.is_premium_user(user_id)
    
    info_text = f"""
<b>👤 ʏᴏᴜʀ ɪɴғᴏʀᴍᴀᴛɪᴏɴ:</b>

<b>🆔 ᴜꜱᴇʀ ɪᴅ:</b> <code>{user_id}</code>
<b>👤 ɴᴀᴍᴇ:</b> {user.mention}
<b>👤 ᴜꜱᴇʀɴᴀᴍᴇ:</b> @{user.username if user.username else 'N/A'}
<b>💎 ᴘʀᴇᴍɪᴜᴍ:</b> {'✅ ʏᴇꜱ' if is_premium else '❌ ɴᴏ'}
<b>📦 ғɪʟᴇ ʟɪᴍɪᴛ:</b> {'4GB' if is_premium else '2GB'}
    """
    
    buttons = [[InlineKeyboardButton("💎 ɢᴇᴛ ᴘʀᴇᴍɪᴜᴍ", callback_data="premium_info")]]
    
    await message.reply_text(
        info_text,
        reply_markup=InlineKeyboardMarkup(buttons) if not is_premium else None
    )

@app.on_message(filters.command("set_thumbnail") & filters.private)
async def set_thumbnail(client, message):
    if not await check_user_subscription(client, message):
        return
    
    reply = message.reply_to_message
    if not reply or not reply.photo:
        return await message.reply("❌ ᴘʟᴇᴀꜱᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴘʜᴏᴛᴏ!")
    
    user_id = message.from_user.id
    
    try:
        # Create thumbnails directory
        thumb_dir = "downloads/thumbnails"
        os.makedirs(thumb_dir, exist_ok=True)
        
        # Download thumbnail
        thumb_path = f"{thumb_dir}/{user_id}_thumb.jpg"
        
        await reply.download(thumb_path)
        
        # Verify file was downloaded
        if not os.path.exists(thumb_path) or os.path.getsize(thumb_path) == 0:
            await message.reply("❌ ғᴀɪʟᴇᴅ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ᴛʜᴜᴍʙɴᴀɪʟ!")
            return
        
        # Save to database
        await db.set_thumbnail(user_id, thumb_path)
        
        await message.reply_photo(
            photo=thumb_path,
            caption="✅ ᴛʜᴜᴍʙɴᴀɪʟ ꜱᴀᴠᴇᴅ ꜱᴜᴄᴄᴇꜱꜱғᴜʟʟʏ!"
        )
    except Exception as e:
        logging.error(f"Error setting thumbnail: {e}")
        await message.reply(f"❌ ᴇʀʀᴏʀ: {str(e)}")

@app.on_message(filters.command("del_thumbnail") & filters.private)
async def delete_thumbnail(client, message):
    if not await check_user_subscription(client, message):
        return
    
    user_id = message.from_user.id
    
    try:
        # Get thumbnail path from database
        thumb_data = await db.get_thumbnail(user_id)
        
        # Delete from database
        await db.delete_thumbnail(user_id)
        
        # Delete file if exists
        if thumb_data and thumb_data.get("thumbnail"):
            thumb_path = thumb_data.get("thumbnail")
            if os.path.exists(thumb_path):
                os.remove(thumb_path)
        
        await message.reply("✅ ᴛʜᴜᴍʙɴᴀɪʟ ᴅᴇʟᴇᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱғᴜʟʟʏ!")
    except Exception as e:
        logging.error(f"Error deleting thumbnail: {e}")
        await message.reply("✅ ᴛʜᴜᴍʙɴᴀɪʟ ᴅᴇʟᴇᴛᴇᴅ!")

@app.on_message(filters.command("show_thumbnail") & filters.private)
async def show_thumbnail(client, message):
    if not await check_user_subscription(client, message):
        return
    
    user_id = message.from_user.id
    thumb_data = await db.get_thumbnail(user_id)
    
    if not thumb_data or not os.path.exists(thumb_data.get("thumbnail")):
        return await message.reply("❌ ɴᴏ ᴛʜᴜᴍʙɴᴀɪʟ ꜱᴇᴛ!")
    
    await message.reply_photo(
        photo=thumb_data["thumbnail"],
        caption="✨ ʏᴏᴜʀ ᴄᴜʀʀᴇɴᴛ ᴛʜᴜᴍʙɴᴀɪʟ"
    )

@app.on_message(filters.document | filters.video & filters.private)
async def handle_file(client, message: Message):
    if not await check_user_subscription(client, message):
        return
    
    user_id = message.from_user.id
    file = message.document or message.video
    
    # Check if it's an archive
    is_archive = file.file_name.lower().endswith(('.zip', '.rar', '.7z', '.tar', '.tar.gz', '.tgz', '.tar.bz2'))
    
    if not is_archive:
        return await message.reply("❌ ᴘʟᴇᴀꜱᴇ ꜱᴇɴᴅ ᴀ ᴠᴀʟɪᴅ ᴀʀᴄʜɪᴠᴇ ғɪʟᴇ!")
    
    # Check file size limit
    is_premium = await db.is_premium_user(user_id)
    max_size = 4 * 1024 * 1024 * 1024 if is_premium else 2 * 1024 * 1024 * 1024  # 4GB or 2GB
    
    if file.file_size > max_size:
        limit_text = "4GB" if is_premium else "2GB"
        return await message.reply(
            f"❌ ғɪʟᴇ ꜱɪᴢᴇ ᴇxᴄᴇᴇᴅꜱ {limit_text} ʟɪᴍɪᴛ!\n\n"
            f"💎 ᴜᴘɢʀᴀᴅᴇ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ ғᴏʀ 4GB ʟɪᴍɪᴛ" if not is_premium else ""
        )
    
    # Ask for upload mode
    buttons = [
        [
            InlineKeyboardButton("📹 ᴠɪᴅᴇᴏ", callback_data=f"mode_video_{message.id}"),
            InlineKeyboardButton("📄 ᴅᴏᴄᴜᴍᴇɴᴛ", callback_data=f"mode_document_{message.id}")
        ]
    ]
    
    user_data[user_id] = {"message_id": message.id}
    
    await message.reply(
        "🎯 ᴄʜᴏᴏꜱᴇ ᴜᴘʟᴏᴀᴅ ᴍᴏᴅᴇ:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_callback_query(filters.regex(r"^mode_"))
async def upload_mode_callback(client, callback_query):
    data = callback_query.data
    user_id = callback_query.from_user.id
    
    _, mode, msg_id = data.split("_")
    msg_id = int(msg_id)
    
    # Get the message
    message = await client.get_messages(user_id, msg_id)
    file = message.document or message.video
    
    await callback_query.message.delete()
    
    # Start extraction
    status_msg = await callback_query.message.reply("📥 ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...")
    
    download_path = None
    try:
        # Check premium status
        is_premium = await db.is_premium_user(user_id)
        
        # Download file
        download_path = f"downloads/{user_id}/"
        os.makedirs(download_path, exist_ok=True)
        
        file_path = os.path.join(download_path, file.file_name)
        
        start_time = time.time()
        
        await message.download(
            file_path,
            progress=progress_for_pyrogram,
            progress_args=(status_msg, start_time, "📥 ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...")
        )
        
        # Verify file was downloaded
        if not os.path.exists(file_path):
            await status_msg.edit("❌ ᴇʀʀᴏʀ: Failed to download file")
            return
        
        # Extract archive
        await status_msg.edit("🗜️ ᴇxᴛʀᴀᴄᴛɪɴɢ ғɪʟᴇꜱ...")
        
        extract_path = f"downloads/{user_id}/extracted/"
        os.makedirs(extract_path, exist_ok=True)
        
        try:
            if file.file_name.endswith('.zip'):
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_path)
            elif file.file_name.endswith('.rar'):
                with rarfile.RarFile(file_path, 'r') as rar_ref:
                    rar_ref.extractall(extract_path)
            elif file.file_name.endswith('.7z'):
                with py7zr.SevenZipFile(file_path, 'r') as sevenz_ref:
                    sevenz_ref.extractall(extract_path)
            elif file.file_name.endswith(('.tar', '.tar.gz', '.tgz', '.tar.bz2')):
                with tarfile.open(file_path, 'r:*') as tar_ref:
                    tar_ref.extractall(extract_path)
        except Exception as e:
            await status_msg.edit(f"❌ ᴇxᴛʀᴀᴄᴛɪᴏɴ ғᴀɪʟᴇᴅ: {str(e)}")
            if os.path.exists(download_path):
                shutil.rmtree(download_path)
            return
        
        # Get thumbnail
        thumb_path = None
        try:
            thumb_data = await db.get_thumbnail(user_id)
            if thumb_data and thumb_data.get("thumbnail"):
                thumb_path = thumb_data.get("thumbnail")
                # Verify thumbnail exists
                if not os.path.exists(thumb_path):
                    thumb_path = None
        except Exception as e:
            logging.error(f"Error getting thumbnail: {e}")
            thumb_path = None
        
        # Count total files
        total_files = sum([len(files) for _, _, files in os.walk(extract_path)])
        
        if total_files == 0:
            await status_msg.edit("❌ ɴᴏ ғɪʟᴇꜱ ғᴏᴜɴᴅ ɪɴ ᴀʀᴄʜɪᴠᴇ")
            if os.path.exists(download_path):
                shutil.rmtree(download_path)
            return
        
        # Upload files
        await status_msg.edit(f"📤 ᴜᴘʟᴏᴀᴅɪɴɢ {total_files} ғɪʟᴇ(s)...")
        
        uploaded_count = 0
        failed_count = 0
        
        for root, dirs, files in os.walk(extract_path):
            for filename in files:
                file_to_upload = os.path.join(root, filename)
                
                # Skip if file doesn't exist or is empty
                if not os.path.exists(file_to_upload):
                    logging.warning(f"File not found: {file_to_upload}")
                    failed_count += 1
                    continue
                
                file_size = os.path.getsize(file_to_upload)
                
                if file_size == 0:
                    logging.warning(f"Empty file skipped: {filename}")
                    failed_count += 1
                    continue
                
                try:
                    # Choose client: user_client for large files if available
                    current_client = client
                    if file_size > 50 * 1024 * 1024 and user_client and is_premium:
                        current_client = user_client
                    
                    # Update status
                    progress_text = f"📤 ᴜᴘʟᴏᴀᴅɪɴɢ {uploaded_count + 1}/{total_files}\n📄 {filename[:30]}..."
                    
                    if mode == "video":
                        await current_client.send_video(
                            chat_id=callback_query.message.chat.id,
                            video=file_to_upload,
                            caption=f"📹 {filename}\n💾 {get_readable_file_size(file_size)}",
                            thumb=thumb_path,
                            progress=progress_for_pyrogram,
                            progress_args=(status_msg, time.time(), progress_text)
                        )
                    else:
                        await current_client.send_document(
                            chat_id=callback_query.message.chat.id,
                            document=file_to_upload,
                            caption=f"📄 {filename}\n💾 {get_readable_file_size(file_size)}",
                            thumb=thumb_path,
                            progress=progress_for_pyrogram,
                            progress_args=(status_msg, time.time(), progress_text)
                        )
                    
                    uploaded_count += 1
                    
                except Exception as e:
                    logging.error(f"Error uploading {filename}: {e}")
                    failed_count += 1
                    continue
        
        # Final status
        result_text = f"✅ ᴄᴏᴍᴘʟᴇᴛᴇᴅ!\n\n"
        result_text += f"📤 ᴜᴘʟᴏᴀᴅᴇᴅ: {uploaded_count} ғɪʟᴇ(s)\n"
        if failed_count > 0:
            result_text += f"❌ ғᴀɪʟᴇᴅ: {failed_count} ғɪʟᴇ(s)"
        
        await status_msg.edit(result_text)
        
    except Exception as e:
        logging.error(f"Error processing file: {e}")
        try:
            await status_msg.edit(f"❌ ᴇʀʀᴏʀ: {str(e)[:100]}")
        except:
            pass
    
    finally:
        # Cleanup
        try:
            if download_path and os.path.exists(download_path):
                shutil.rmtree(download_path)
        except Exception as e:
            logging.error(f"Cleanup error: {e}")

# Handle torrent/magnet links
@app.on_message(filters.text & filters.private)
async def handle_torrent(client, message: Message):
    if not await check_user_subscription(client, message):
        return
    
    text = message.text
    
    # Check if it's a magnet link or torrent URL
    if text.startswith("magnet:?") or text.endswith(".torrent"):
        await message.reply(
            "🚧 ᴛᴏʀʀᴇɴᴛ ᴅᴏᴡɴʟᴏᴀᴅ ғᴇᴀᴛᴜʀᴇ ɪꜱ ᴄᴏᴍɪɴɢ ꜱᴏᴏɴ!\n\n"
            "💡 ғᴏʀ ɴᴏᴡ, ᴜꜱᴇ ᴢɪᴘ/ʀᴀʀ ғɪʟᴇꜱ"
        )

# Callback query handler
@app.on_callback_query()
async def callback_handler(client, callback_query):
    data = callback_query.data
    
    if data == "start":
        await callback_query.message.delete()
        await start_command(client, callback_query.message)
    
    elif data == "help":
        buttons = [[InlineKeyboardButton("🏠 ʜᴏᴍᴇ", callback_data="start")]]
        await callback_query.message.edit_text(
            script.HELP_TXT,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    
    elif data == "about":
        me = await client.get_me()
        buttons = [[InlineKeyboardButton("🏠 ʜᴏᴍᴇ", callback_data="start")]]
        await callback_query.message.edit_text(
            script.ABOUT_TXT.format(me.username, me.first_name, script.ADMIN_USERNAME),
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True
        )
    
    elif data == "premium_info":
        buttons = [
            [InlineKeyboardButton("💳 ʙᴜʏ ᴘʀᴇᴍɪᴜᴍ", callback_data="buy_info")],
            [InlineKeyboardButton("🏠 ʜᴏᴍᴇ", callback_data="start")]
        ]
        await callback_query.message.edit_text(
            script.PREMIUM_TXT,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    
    await callback_query.answer()

if __name__ == "__main__":
    print("Bot Started!")
    
    # Create downloads directory
    os.makedirs("downloads", exist_ok=True)
    os.makedirs("downloads/thumbnails", exist_ok=True)
    
    # Start web server for health checks (optional)
    from aiohttp import web
    
    async def health_check(request):
        return web.Response(text="Bot is running!")
    
    async def start_web_server():
        app_web = web.Application()
        app_web.router.add_get("/", health_check)
        runner = web.AppRunner(app_web)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", Config.PORT)
        await site.start()
        print(f"Web server started on port {Config.PORT}")
    
    if user_client:
        print("Starting with User Session for large file uploads (up to 4GB)")
        import asyncio
        loop = asyncio.get_event_loop()
        
        async def start_both():
            # Start web server
            await start_web_server()
            # Start user client
            await user_client.start()
            # Run bot
            await app.run()
        
        loop.run_until_complete(start_both())
    else:
        print("Starting without user session - upload limit: 50MB")
        import asyncio
        loop = asyncio.get_event_loop()
        
        async def start_bot_with_server():
            await start_web_server()
            await app.run()
        
        loop.run_until_complete(start_bot_with_server())
