import pytz
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message
from database.users_chats_db import db

@Client.on_message(filters.command("info") & filters.private)
async def user_info(client, message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    username = message.from_user.username
    
    # Add user to database if not exists
    if not await db.is_user_exist(user_id):
        await db.add_user(user_id, user_name)
    
    # Get user data
    user_data = await db.get_user(user_id)
    ban_status = await db.get_ban_status(user_id)
    thumbnail = await db.get_thumbnail(user_id)
    
    # Check premium status
    is_premium = False
    premium_text = "❌ No"
    expiry_text = "N/A"
    
    if user_data and user_data.get("expiry_time"):
        expiry = user_data.get("expiry_time")
        expiry_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata"))
        
        if expiry_ist > datetime.now(pytz.timezone("Asia/Kolkata")):
            is_premium = True
            premium_text = "✅ Yes"
            expiry_text = expiry_ist.strftime("%d-%m-%Y %I:%M:%S %p")
            
            # Calculate time left
            current_time = datetime.now(pytz.timezone("Asia/Kolkata"))
            time_left = expiry_ist - current_time
            days = time_left.days
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            expiry_text += f"\n⏰ Time Left: {days}d {hours}h {minutes}m"
    
    # Join date
    join_date = "N/A"
    if user_data and user_data.get("join_date"):
        join_date_obj = user_data.get("join_date")
        if hasattr(join_date_obj, 'strftime'):
            join_date = join_date_obj.strftime("%d-%m-%Y %I:%M:%S %p")
    
    info_text = f"""
<b>👤 USER INFORMATION</b>

<b>📝 Basic Details:</b>
• Name: {user_name}
• Username: @{username if username else 'None'}
• User ID: <code>{user_id}</code>

<b>💎 Premium Status:</b>
• Premium: {premium_text}
• Expiry: {expiry_text}

<b>🖼️ Thumbnail:</b>
• Set: {'✅ Yes' if thumbnail else '❌ No'}

<b>🚫 Ban Status:</b>
• Banned: {'✅ Yes' if ban_status['is_banned'] else '❌ No'}
{f"• Reason: {ban_status['ban_reason']}" if ban_status['is_banned'] else ''}

<b>📅 Join Date:</b>
• {join_date}

<b>📊 File Limits:</b>
• Max Size: {'4GB' if is_premium else '2GB'}
• Priority: {'High' if is_premium else 'Normal'}
"""
    
    await message.reply_text(info_text)
