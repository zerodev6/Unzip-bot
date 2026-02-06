import asyncio
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from database.users_chats_db import db
from Script import script
from info import ADMINS, FORCE_SUB_CHANNELS, FORCE_SUB_IMAGE, WELCOME_IMAGE_API, OWNER_USERNAME
from pyrogram.errors import UserNotParticipant

async def is_subscribed(client, user_id):
    """Check if user is subscribed to all force sub channels"""
    try:
        for channel in FORCE_SUB_CHANNELS:
            try:
                member = await client.get_chat_member(f"@{channel}", user_id)
                if member.status in ["left", "kicked"]:
                    return False, channel
            except UserNotParticipant:
                return False, channel
            except Exception as e:
                print(f"Error checking subscription for {channel}: {e}")
                continue
        return True, None
    except Exception as e:
        print(f"Error in is_subscribed: {e}")
        return True, None

@Client.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    # Add user to database
    if not await db.is_user_exist(user_id):
        await db.add_user(user_id, user_name)
    
    # Check force subscription
    subscribed, channel = await is_subscribed(client, user_id)
    if not subscribed:
        buttons = []
        for ch in FORCE_SUB_CHANNELS:
            buttons.append([InlineKeyboardButton(f"📢 Join {ch}", url=f"https://t.me/{ch}")])
        buttons.append([InlineKeyboardButton("🔄 Check Again", callback_data="check_sub")])
        
        channels_text = "\n".join([f"• @{ch}" for ch in FORCE_SUB_CHANNELS])
        
        try:
            await message.reply_photo(
                photo=FORCE_SUB_IMAGE,
                caption=script.FORCE_SUB_TEXT.format(channels=channels_text),
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        except:
            await message.reply_text(
                script.FORCE_SUB_TEXT.format(channels=channels_text),
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        return
    
    # Show loading animation
    loading_msg = await message.reply_text("⏳")
    await asyncio.sleep(2)
    await loading_msg.delete()
    
    # Get random welcome image
    try:
        response = requests.get(WELCOME_IMAGE_API)
        if response.status_code == 200:
            data = response.json()
            image_url = data.get('url', WELCOME_IMAGE_API)
        else:
            image_url = WELCOME_IMAGE_API
    except:
        image_url = WELCOME_IMAGE_API
    
    buttons = [
        [
            InlineKeyboardButton("📚 Help", callback_data="help"),
            InlineKeyboardButton("ℹ️ About", callback_data="about")
        ],
        [
            InlineKeyboardButton("💎 Premium", callback_data="premium_info"),
            InlineKeyboardButton("📊 My Plan", callback_data="myplan")
        ],
        [
            InlineKeyboardButton("👨‍💻 Developer", url=f"https://t.me/{OWNER_USERNAME.replace('@', '')}")
        ]
    ]
    
    try:
        await message.reply_photo(
            photo=image_url,
            caption=script.START_TXT.format(user_name),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except:
        await message.reply_text(
            script.START_TXT.format(user_name),
            reply_markup=InlineKeyboardMarkup(buttons)
        )

@Client.on_callback_query(filters.regex("^check_sub$"))
async def check_sub_callback(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    
    subscribed, channel = await is_subscribed(client, user_id)
    if not subscribed:
        await callback_query.answer("❌ You haven't joined all channels yet!", show_alert=True)
        return
    
    await callback_query.message.delete()
    await callback_query.answer("✅ Subscription verified!")
    
    # Show start message
    user_name = callback_query.from_user.first_name
    
    try:
        response = requests.get(WELCOME_IMAGE_API)
        if response.status_code == 200:
            data = response.json()
            image_url = data.get('url', WELCOME_IMAGE_API)
        else:
            image_url = WELCOME_IMAGE_API
    except:
        image_url = WELCOME_IMAGE_API
    
    buttons = [
        [
            InlineKeyboardButton("📚 Help", callback_data="help"),
            InlineKeyboardButton("ℹ️ About", callback_data="about")
        ],
        [
            InlineKeyboardButton("💎 Premium", callback_data="premium_info"),
            InlineKeyboardButton("📊 My Plan", callback_data="myplan")
        ],
        [
            InlineKeyboardButton("👨‍💻 Developer", url=f"https://t.me/{OWNER_USERNAME.replace('@', '')}")
        ]
    ]
    
    try:
        await callback_query.message.reply_photo(
            photo=image_url,
            caption=script.START_TXT.format(user_name),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except:
        await callback_query.message.reply_text(
            script.START_TXT.format(user_name),
            reply_markup=InlineKeyboardMarkup(buttons)
        )

@Client.on_callback_query(filters.regex("^help$"))
async def help_callback(client, callback_query: CallbackQuery):
    buttons = [
        [InlineKeyboardButton("🔙 Back", callback_data="start")]
    ]
    await callback_query.message.edit_text(
        script.HELP_TXT,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@Client.on_callback_query(filters.regex("^about$"))
async def about_callback(client, callback_query: CallbackQuery):
    me = await client.get_me()
    buttons = [
        [InlineKeyboardButton("🔙 Back", callback_data="start")]
    ]
    await callback_query.message.edit_text(
        script.ABOUT_TXT.format(me.username, me.first_name, OWNER_USERNAME),
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )

@Client.on_callback_query(filters.regex("^start$"))
async def start_callback(client, callback_query: CallbackQuery):
    user_name = callback_query.from_user.first_name
    buttons = [
        [
            InlineKeyboardButton("📚 Help", callback_data="help"),
            InlineKeyboardButton("ℹ️ About", callback_data="about")
        ],
        [
            InlineKeyboardButton("💎 Premium", callback_data="premium_info"),
            InlineKeyboardButton("📊 My Plan", callback_data="myplan")
        ],
        [
            InlineKeyboardButton("👨‍💻 Developer", url=f"https://t.me/{OWNER_USERNAME.replace('@', '')}")
        ]
    ]
    
    await callback_query.message.edit_text(
        script.START_TXT.format(user_name),
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@Client.on_message(filters.command("help") & filters.private)
async def help_command(client, message):
    buttons = [
        [InlineKeyboardButton("🏠 Home", callback_data="start")]
    ]
    await message.reply_text(
        script.HELP_TXT,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@Client.on_message(filters.command("about") & filters.private)
async def about_command(client, message):
    me = await client.get_me()
    buttons = [
        [InlineKeyboardButton("🏠 Home", callback_data="start")]
    ]
    await message.reply_text(
        script.ABOUT_TXT.format(me.username, me.first_name, OWNER_USERNAME),
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )
