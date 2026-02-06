import os
import time
import shutil
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from database.users_chats_db import db
from helpers.unzip_helper import unzip_helper
from utils import progress_for_pyrogram, get_readable_file_size
from info import FREE_USER_LIMIT, PREMIUM_USER_LIMIT, DOWNLOAD_LOCATION
from datetime import datetime
import pytz

# Create download directory if it doesn't exist
os.makedirs(DOWNLOAD_LOCATION, exist_ok=True)

async def is_premium_user(user_id):
    """Check if user has premium access"""
    data = await db.get_user(user_id)
    if data and data.get("expiry_time"):
        expiry = data.get("expiry_time")
        if expiry.replace(tzinfo=pytz.UTC) > datetime.now(pytz.UTC):
            return True
    return False

@Client.on_message(filters.private & filters.document)
async def handle_document(client, message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    # Add user to database if not exists
    if not await db.is_user_exist(user_id):
        await db.add_user(user_id, user_name)
    
    # Check ban status
    ban_status = await db.get_ban_status(user_id)
    if ban_status['is_banned']:
        await message.reply_text(f"❌ You are banned!\nReason: {ban_status['ban_reason']}")
        return
    
    file = message.document
    file_name = file.file_name
    file_size = file.file_size
    
    # Check if file is an archive
    supported_extensions = ['.zip', '.rar', '.7z', '.tar', '.tar.gz', '.tgz', '.tar.bz2']
    if not any(file_name.lower().endswith(ext) for ext in supported_extensions):
        await message.reply_text(
            "❌ Unsupported file format!\n\n"
            "Supported formats:\n"
            "• ZIP (.zip)\n"
            "• RAR (.rar)\n"
            "• 7Z (.7z)\n"
            "• TAR (.tar, .tar.gz, .tgz, .tar.bz2)"
        )
        return
    
    # Check file size limit
    is_premium = await is_premium_user(user_id)
    size_limit = PREMIUM_USER_LIMIT if is_premium else FREE_USER_LIMIT
    
    if file_size > size_limit:
        limit_text = "4GB" if is_premium else "2GB"
        await message.reply_text(
            f"❌ File too large!\n\n"
            f"Your limit: {limit_text}\n"
            f"File size: {get_readable_file_size(file_size)}\n\n"
            f"{'Upgrade to premium for 4GB limit! Use /plan' if not is_premium else ''}"
        )
        return
    
    # Create user-specific directory
    user_dir = os.path.join(DOWNLOAD_LOCATION, str(user_id))
    os.makedirs(user_dir, exist_ok=True)
    
    download_path = os.path.join(user_dir, file_name)
    extract_path = os.path.join(user_dir, "extracted")
    os.makedirs(extract_path, exist_ok=True)
    
    # Download file
    status_msg = await message.reply_text("⬇️ 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱𝗶𝗻𝗴...")
    
    start_time = time.time()
    
    try:
        await message.download(
            file_name=download_path,
            progress=progress_for_pyrogram,
            progress_args=("⬇️ 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱𝗶𝗻𝗴...", status_msg, start_time)
        )
    except Exception as e:
        await status_msg.edit_text(f"❌ Download failed: {str(e)}")
        shutil.rmtree(user_dir, ignore_errors=True)
        return
    
    # Show archive info
    archive_info = unzip_helper.get_archive_info(download_path)
    
    if 'error' not in archive_info:
        info_text = (
            f"📦 Archive Information:\n\n"
            f"📄 Name: {file_name}\n"
            f"📊 Size: {get_readable_file_size(archive_info['size'])}\n"
            f"📁 Files: {archive_info['files']}\n"
            f"🗜️ Format: {archive_info['format']}\n\n"
            f"🔄 Extracting files..."
        )
        await status_msg.edit_text(info_text)
    else:
        await status_msg.edit_text("🔄 Extracting files...")
    
    # Extract archive
    extraction_start = time.time()
    
    async def extraction_progress(current, total):
        if int(time.time() - extraction_start) % 3 == 0:  # Update every 3 seconds
            try:
                progress = (current / total) * 100
                await status_msg.edit_text(
                    f"🔄 Extracting files...\n\n"
                    f"Progress: {progress:.1f}%\n"
                    f"Files: {current}/{total}"
                )
            except:
                pass
    
    success, result = await unzip_helper.extract_archive(
        download_path,
        extract_path,
        extraction_progress
    )
    
    if not success:
        await status_msg.edit_text(f"❌ Extraction failed: {result}")
        shutil.rmtree(user_dir, ignore_errors=True)
        return
    
    # Get extracted files
    extracted_files = []
    for root, dirs, files in os.walk(extract_path):
        for file in files:
            file_path = os.path.join(root, file)
            extracted_files.append(file_path)
    
    if not extracted_files:
        await status_msg.edit_text("❌ No files found in archive!")
        shutil.rmtree(user_dir, ignore_errors=True)
        return
    
    await status_msg.edit_text(
        f"✅ Extraction completed!\n\n"
        f"📁 Total files: {len(extracted_files)}\n\n"
        f"⬆️ Uploading files..."
    )
    
    # Get user thumbnail
    thumbnail = await db.get_thumbnail(user_id)
    
    # Upload files
    uploaded = 0
    failed = 0
    
    for file_path in extracted_files:
        try:
            relative_path = os.path.relpath(file_path, extract_path)
            
            upload_start = time.time()
            
            await message.reply_document(
                document=file_path,
                thumb=thumbnail,
                caption=f"📁 {relative_path}",
                progress=progress_for_pyrogram,
                progress_args=("⬆️ 𝗨𝗽𝗹𝗼𝗮𝗱𝗶𝗻𝗴...", status_msg, upload_start)
            )
            
            uploaded += 1
            
            # Update status every 5 files
            if uploaded % 5 == 0:
                await status_msg.edit_text(
                    f"⬆️ Uploading files...\n\n"
                    f"✅ Uploaded: {uploaded}/{len(extracted_files)}"
                )
        
        except Exception as e:
            print(f"Failed to upload {file_path}: {e}")
            failed += 1
            continue
    
    # Final status
    total_time = time.time() - start_time
    minutes = int(total_time // 60)
    seconds = int(total_time % 60)
    
    await status_msg.edit_text(
        f"✅ Process completed!\n\n"
        f"📊 Statistics:\n"
        f"• Total files: {len(extracted_files)}\n"
        f"• Uploaded: {uploaded}\n"
        f"• Failed: {failed}\n"
        f"• Time: {minutes}m {seconds}s"
    )
    
    # Cleanup
    shutil.rmtree(user_dir, ignore_errors=True)

@Client.on_message(filters.command("zip") & filters.private)
async def zip_command(client, message: Message):
    await message.reply_text(
        "📦 How to create ZIP:\n\n"
        "1. Send me multiple files\n"
        "2. Use /done when finished\n"
        "3. I'll create a ZIP archive\n\n"
        "Note: This feature is coming soon!"
    )
