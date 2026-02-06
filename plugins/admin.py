from pyrogram import Client, filters , StopPropagation
from utils import temp
from pyrogram.types import Message
from database.users_chats_db import db
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from info import SUPPORT_CHAT, ADMINS
import os

async def banned_users(_, client, message: Message):
    return (
        message.from_user is not None or not message.sender_chat
    ) and message.from_user.id in temp.BANNED_USERS

banned_user = filters.create(banned_users)

@Client.on_message(filters.command('banned') & filters.user(ADMINS))
async def get_banned(client, message):
    banned_users, _ = await db.get_banned()
    if not banned_users:
        await message.reply_text("No banned users found.")
        return
    
    text = ""
    for user_id in banned_users:
        try:
            user = await client.get_users(user_id)
            text += f"{user.mention} (`{user.id}`)\n"
        except Exception:
            text += f"Undefined (`{user_id}`)\n"
    
    if len(text) > 4096:
        with open('banned_users.txt', 'w') as f:
            f.write(text)
        await message.reply_document('banned_users.txt')
        os.remove('banned_users.txt')
    else:
        await message.reply_text(text)

async def disabled_chat(_, client, message: Message):
    return message.chat.id in temp.BANNED_CHATS
disabled_group=filters.create(disabled_chat)

@Client.on_message(filters.private & banned_user & filters.incoming , group=-1)
async def ban_reply(bot, message):
    ban = await db.get_ban_status(message.from_user.id)
    await message.reply(f'Sorry Dude, You are Banned to use Me. \nBan Reason : {ban["ban_reason"]}')
    raise StopPropagation

@Client.on_message(filters.group & disabled_group & filters.incoming , group=-1)
async def grp_bd(bot, message):
    buttons = [[
        InlineKeyboardButton('Support', url=SUPPORT_CHAT)
    ]]
    reply_markup=InlineKeyboardMarkup(buttons)
    vazha = await db.get_chat(message.chat.id)
    k = await message.reply(
        text=f"CHAT NOT ALLOWED 🐞\n\nMy admins has restricted me from working here ! If you want to know more about it contact support..\nReason : <code>{vazha['reason']}</code>.",
        reply_markup=reply_markup)
    try:
        await k.pin()
    except:
        pass
    await bot.leave_chat(message.chat.id)
    raise StopPropagation

@Client.on_message(filters.command('ban') & filters.user(ADMINS))
async def ban_user(client, message):
    if len(message.command) < 2:
        await message.reply("Usage: /ban user_id [reason]")
        return
    
    try:
        user_id = int(message.command[1])
        reason = " ".join(message.command[2:]) if len(message.command) > 2 else "No reason provided"
        
        await db.ban_user(user_id, reason)
        temp.BANNED_USERS.append(user_id)
        
        try:
            user = await client.get_users(user_id)
            await message.reply_text(f"✅ Banned {user.mention}\nReason: {reason}")
        except:
            await message.reply_text(f"✅ Banned user {user_id}\nReason: {reason}")
    except ValueError:
        await message.reply_text("❌ Invalid user ID")
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

@Client.on_message(filters.command('unban') & filters.user(ADMINS))
async def unban_user(client, message):
    if len(message.command) < 2:
        await message.reply("Usage: /unban user_id")
        return
    
    try:
        user_id = int(message.command[1])
        
        await db.remove_ban(user_id)
        if user_id in temp.BANNED_USERS:
            temp.BANNED_USERS.remove(user_id)
        
        try:
            user = await client.get_users(user_id)
            await message.reply_text(f"✅ Unbanned {user.mention}")
        except:
            await message.reply_text(f"✅ Unbanned user {user_id}")
    except ValueError:
        await message.reply_text("❌ Invalid user ID")
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

@Client.on_message(filters.command('disable_chat') & filters.user(ADMINS))
async def disable_chat(client, message):
    if len(message.command) < 2:
        await message.reply("Usage: /disable_chat chat_id [reason]")
        return
    
    try:
        chat_id = int(message.command[1])
        reason = " ".join(message.command[2:]) if len(message.command) > 2 else "No reason provided"
        
        await db.disable_chat(chat_id, reason)
        temp.BANNED_CHATS.append(chat_id)
        
        await message.reply_text(f"✅ Disabled chat {chat_id}\nReason: {reason}")
    except ValueError:
        await message.reply_text("❌ Invalid chat ID")
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

@Client.on_message(filters.command('enable_chat') & filters.user(ADMINS))
async def enable_chat(client, message):
    if len(message.command) < 2:
        await message.reply("Usage: /enable_chat chat_id")
        return
    
    try:
        chat_id = int(message.command[1])
        
        await db.re_enable_chat(chat_id)
        if chat_id in temp.BANNED_CHATS:
            temp.BANNED_CHATS.remove(chat_id)
        
        await message.reply_text(f"✅ Enabled chat {chat_id}")
    except ValueError:
        await message.reply_text("❌ Invalid chat ID")
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

@Client.on_message(filters.command('stats') & filters.user(ADMINS))
async def stats_command(client, message):
    total_users = await db.total_users_count()
    total_chats = await db.total_chat_count()
    banned_users, banned_chats = await db.get_banned()
    
    # Count premium users
    premium_count = 0
    users = await db.get_all_users()
    async for user in users:
        data = await db.get_user(user['id'])
        if data and data.get("expiry_time"):
            premium_count += 1
    
    db_size = await db.get_db_size()
    db_size_mb = db_size / (1024 * 1024)
    
    stats_text = f"""
<b>📊 BOT STATISTICS</b>

<b>👥 Users:</b>
• Total: {total_users}
• Premium: {premium_count}
• Banned: {len(banned_users)}

<b>💬 Groups:</b>
• Total: {total_chats}
• Disabled: {len(banned_chats)}

<b>💾 Database:</b>
• Size: {db_size_mb:.2f} MB
"""
    
    await message.reply_text(stats_text)
