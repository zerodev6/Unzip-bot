from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from database.users_chats_db import db
from Script import script
import os

THUMB_LOCATION = "./thumbnails"
os.makedirs(THUMB_LOCATION, exist_ok=True)

@Client.on_message(filters.command("addthum") & filters.private)
async def add_thumbnail_command(client, message: Message):
    await message.reply_text(
        "🖼️ Send me a photo to set as your thumbnail.\n\n"
        "This thumbnail will be used for all extracted files."
    )

@Client.on_message(filters.photo & filters.private)
async def save_thumbnail(client, message: Message):
    user_id = message.from_user.id
    
    # Add user to database if not exists
    if not await db.is_user_exist(user_id):
        await db.add_user(user_id, message.from_user.first_name)
    
    # Get the largest photo size
    photo = message.photo
    file_id = photo.file_id
    
    # Save thumbnail to database
    await db.set_thumbnail(user_id, file_id)
    
    # Download and save locally
    thumb_path = os.path.join(THUMB_LOCATION, f"{user_id}.jpg")
    await message.download(file_name=thumb_path)
    
    buttons = [
        [
            InlineKeyboardButton("👁️ View Thumbnail", callback_data="view_thumb"),
            InlineKeyboardButton("🗑️ Delete", callback_data="delete_thumb")
        ]
    ]
    
    await message.reply_text(
        script.THUMBNAIL_SAVED,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@Client.on_message(filters.command("viewthum") & filters.private)
async def view_thumbnail_command(client, message: Message):
    user_id = message.from_user.id
    
    thumbnail = await db.get_thumbnail(user_id)
    
    if not thumbnail:
        buttons = [[InlineKeyboardButton("➕ Add Thumbnail", callback_data="add_thumb_info")]]
        await message.reply_text(
            script.NO_THUMBNAIL_TEXT,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return
    
    buttons = [
        [
            InlineKeyboardButton("🔄 Change", callback_data="add_thumb_info"),
            InlineKeyboardButton("🗑️ Delete", callback_data="delete_thumb")
        ]
    ]
    
    try:
        await message.reply_photo(
            photo=thumbnail,
            caption=script.THUMBNAIL_TEXT,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except:
        await message.reply_text(
            "❌ Failed to load thumbnail. Please set a new one.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("➕ Add Thumbnail", callback_data="add_thumb_info")]])
        )

@Client.on_message(filters.command("delectthum") & filters.private)
async def delete_thumbnail_command(client, message: Message):
    user_id = message.from_user.id
    
    thumbnail = await db.get_thumbnail(user_id)
    
    if not thumbnail:
        await message.reply_text("❌ No thumbnail set!")
        return
    
    # Delete from database
    await db.delete_thumbnail(user_id)
    
    # Delete local file
    thumb_path = os.path.join(THUMB_LOCATION, f"{user_id}.jpg")
    if os.path.exists(thumb_path):
        os.remove(thumb_path)
    
    await message.reply_text(script.THUMBNAIL_DELETED)

# Callback queries
@Client.on_callback_query(filters.regex("^view_thumb$"))
async def view_thumb_callback(client, callback_query):
    user_id = callback_query.from_user.id
    
    thumbnail = await db.get_thumbnail(user_id)
    
    if not thumbnail:
        await callback_query.answer("❌ No thumbnail set!", show_alert=True)
        return
    
    buttons = [
        [
            InlineKeyboardButton("🔄 Change", callback_data="add_thumb_info"),
            InlineKeyboardButton("🗑️ Delete", callback_data="delete_thumb")
        ]
    ]
    
    try:
        await callback_query.message.reply_photo(
            photo=thumbnail,
            caption=script.THUMBNAIL_TEXT,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        await callback_query.answer()
    except:
        await callback_query.answer("❌ Failed to load thumbnail!", show_alert=True)

@Client.on_callback_query(filters.regex("^add_thumb_info$"))
async def add_thumb_info_callback(client, callback_query):
    await callback_query.message.edit_text(
        "🖼️ Send me a photo to set as your thumbnail.\n\n"
        "This thumbnail will be used for all extracted files."
    )
    await callback_query.answer()

@Client.on_callback_query(filters.regex("^delete_thumb$"))
async def delete_thumb_callback(client, callback_query):
    user_id = callback_query.from_user.id
    
    thumbnail = await db.get_thumbnail(user_id)
    
    if not thumbnail:
        await callback_query.answer("❌ No thumbnail set!", show_alert=True)
        return
    
    # Delete from database
    await db.delete_thumbnail(user_id)
    
    # Delete local file
    thumb_path = os.path.join(THUMB_LOCATION, f"{user_id}.jpg")
    if os.path.exists(thumb_path):
        os.remove(thumb_path)
    
    await callback_query.message.edit_text(script.THUMBNAIL_DELETED)
    await callback_query.answer("✅ Thumbnail deleted!", show_alert=True)
