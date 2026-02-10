import time
import math
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import errors
from script import script

# Temporary storage
class temp:
    B_LINK = ""
    B_USERS_CANCEL = False
    B_GROUPS_CANCEL = False

def get_readable_file_size(size_in_bytes):
    """Convert bytes to readable format"""
    if size_in_bytes is None:
        return "0B"
    index = 0
    size_table = ["B", "KB", "MB", "GB", "TB"]
    while size_in_bytes >= 1024 and index < 4:
        size_in_bytes /= 1024
        index += 1
    return f"{round(size_in_bytes, 2)}{size_table[index]}"

def get_readable_time(seconds):
    """Convert seconds to readable time format"""
    result = ''
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)
    if days != 0:
        result += f'{days}d '
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0:
        result += f'{hours}h '
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0:
        result += f'{minutes}m '
    seconds = int(seconds)
    result += f'{seconds}s'
    return result

async def progress_for_pyrogram(current, total, status_msg, start, text):
    """Progress callback for Pyrogram"""
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff)
        time_to_completion = round((total - current) / speed)
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = get_readable_time(elapsed_time)
        estimated_total_time = get_readable_time(estimated_total_time)

        progress = "[{0}{1}] \n".format(
            ''.join(["█" for i in range(math.floor(percentage / 5))]),
            ''.join(["░" for i in range(20 - math.floor(percentage / 5))])
        )

        tmp = progress + f"""
{text}

<b>📊 ᴘʀᴏɢʀᴇss:</b> {round(percentage, 2)}%
<b>✅ ᴅᴏɴᴇ:</b> {get_readable_file_size(current)}
<b>📦 ᴛᴏᴛᴀʟ:</b> {get_readable_file_size(total)}
<b>🚀 sᴘᴇᴇᴅ:</b> {get_readable_file_size(speed)}/s
<b>⏱️ ᴇᴛᴀ:</b> {estimated_total_time if estimated_total_time != '' else "0s"}
"""
        try:
            await status_msg.edit(text=tmp)
        except:
            pass

async def get_seconds(time_string):
    """Convert time string to seconds"""
    try:
        parts = time_string.split()
        if len(parts) != 2:
            return 0
        
        amount = int(parts[0])
        unit = parts[1].lower()
        
        time_units = {
            'second': 1, 'seconds': 1, 'sec': 1, 's': 1,
            'minute': 60, 'minutes': 60, 'min': 60, 'm': 60,
            'hour': 3600, 'hours': 3600, 'h': 3600,
            'day': 86400, 'days': 86400, 'd': 86400,
            'week': 604800, 'weeks': 604800, 'w': 604800,
            'month': 2592000, 'months': 2592000,
            'year': 31536000, 'years': 31536000, 'y': 31536000
        }
        
        return amount * time_units.get(unit, 0)
    except:
        return 0

async def check_user_subscription(client, message):
    """Check if user has subscribed to required channels"""
    user_id = message.from_user.id
    
    # Check all force sub channels
    not_subscribed = []
    
    for channel in script.FORCE_SUB_CHANNELS:
        try:
            member = await client.get_chat_member(f"@{channel}", user_id)
            if member.status in ['left', 'kicked']:
                not_subscribed.append(channel)
        except:
            not_subscribed.append(channel)
    
    if not_subscribed:
        # Create join buttons
        buttons = []
        for channel in script.FORCE_SUB_CHANNELS:
            buttons.append([InlineKeyboardButton(f"📢 ᴊᴏɪɴ @{channel}", url=f"https://t.me/{channel}")])
        
        buttons.append([InlineKeyboardButton("✅ ɪ ᴊᴏɪɴᴇᴅ", callback_data="check_subscription")])
        
        await message.reply_photo(
            photo=script.FORCE_SUB_IMAGE,
            caption=script.FORCE_SUB_TEXT,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return False
    
    return True

async def users_broadcast(user_id, message, pin):
    """Broadcast message to a user"""
    try:
        if pin:
            await message.copy(chat_id=user_id)
            # Note: Pinning in private chats not supported by Telegram
        else:
            await message.copy(chat_id=user_id)
        return user_id, "Success"
    except errors.FloodWait as e:
        raise e
    except errors.InputUserDeactivated:
        return user_id, "Deleted"
    except errors.UserIsBlocked:
        return user_id, "Blocked"
    except Exception as e:
        return user_id, "Error"

async def groups_broadcast(chat_id, message, pin):
    """Broadcast message to a group"""
    try:
        msg = await message.copy(chat_id=chat_id)
        if pin:
            try:
                await msg.pin(disable_notification=True)
            except:
                pass
        return "Success"
    except Exception as e:
        return "Error"

async def clear_junk(user_id, message):
    """Check if user is active"""
    try:
        await message.copy(chat_id=user_id)
        return True, "Success"
    except errors.InputUserDeactivated:
        return False, "Deleted"
    except errors.UserIsBlocked:
        return False, "Blocked"
    except Exception as e:
        return False, "Error"

async def junk_group(chat_id, message):
    """Check if group is active"""
    try:
        await message.copy(chat_id=chat_id)
        return True, "Success", ""
    except Exception as e:
        return False, "deleted", str(e)
