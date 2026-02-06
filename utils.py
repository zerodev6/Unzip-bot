import time
import math
import asyncio
from pyrogram import enums
from pyrogram.errors import FloodWait, UserNotParticipant

class temp:
    BANNED_USERS = []
    BANNED_CHATS = []
    B_USERS_CANCEL = False
    B_GROUPS_CANCEL = False
    B_LINK = ""

def get_readable_time(seconds: int) -> str:
    """Convert seconds to readable time format"""
    count = 0
    readable_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        readable_time += time_list.pop() + ", "

    time_list.reverse()
    readable_time += ":".join(time_list)

    return readable_time

def get_readable_file_size(size_in_bytes: int) -> str:
    """Convert bytes to human readable format"""
    if size_in_bytes is None:
        return "0B"
    index = 0
    size_in_bytes = float(size_in_bytes)
    while size_in_bytes >= 1024:
        size_in_bytes /= 1024
        index += 1
    try:
        return f"{round(size_in_bytes, 2)}{['B', 'KB', 'MB', 'GB', 'TB'][index]}"
    except IndexError:
        return "File too large"

async def get_seconds(time_str: str) -> int:
    """Convert time string to seconds"""
    time_str = time_str.lower().strip()
    parts = time_str.split()
    
    if len(parts) != 2:
        return 0
    
    try:
        value = int(parts[0])
        unit = parts[1]
        
        if unit in ["second", "seconds", "sec", "s"]:
            return value
        elif unit in ["minute", "minutes", "min", "m"]:
            return value * 60
        elif unit in ["hour", "hours", "h"]:
            return value * 3600
        elif unit in ["day", "days", "d"]:
            return value * 86400
        elif unit in ["week", "weeks", "w"]:
            return value * 604800
        elif unit in ["month", "months", "mo"]:
            return value * 2592000
        elif unit in ["year", "years", "y"]:
            return value * 31536000
        else:
            return 0
    except:
        return 0

def progress_bar(percentage):
    """Generate progress bar"""
    filled = int(percentage / 5)
    empty = 20 - filled
    return "█" * filled + "░" * empty

async def progress_for_pyrogram(current, total, ud_type, message, start):
    """Progress callback for pyrogram uploads/downloads"""
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = get_readable_time(elapsed_time / 1000)
        estimated_total_time = get_readable_time(estimated_total_time / 1000)

        progress = progress_bar(percentage)
        
        tmp = f"""
{ud_type}

{progress}

📁 Total Size : {get_readable_file_size(total)}
{'📥 Downloaded' if ud_type == '⬇️ 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱𝗶𝗻𝗴...' else '📤 Uploaded'} : {get_readable_file_size(current)}
📊 Progress : {percentage:.2f}%
⚡ Speed : {get_readable_file_size(speed)}/s
⏳ Remaining : {get_readable_time((total - current) / speed)}
"""
        try:
            await message.edit_text(text=tmp)
        except:
            pass

async def users_broadcast(user_id, broadcast_message, pin):
    """Send broadcast message to user"""
    try:
        await broadcast_message.copy(chat_id=user_id)
        if pin:
            try:
                await broadcast_message.pin(chat_id=user_id, disable_notification=True)
            except:
                pass
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await users_broadcast(user_id, broadcast_message, pin)
    except Exception as e:
        if "blocked" in str(e).lower():
            return False, "Blocked"
        elif "deleted" in str(e).lower():
            return False, "Deleted"
        else:
            return False, "Error"

async def groups_broadcast(chat_id, broadcast_message, pin):
    """Send broadcast message to group"""
    try:
        await broadcast_message.copy(chat_id=chat_id)
        if pin:
            try:
                await broadcast_message.pin(chat_id=chat_id, disable_notification=True)
            except:
                pass
        return "Success"
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await groups_broadcast(chat_id, broadcast_message, pin)
    except Exception:
        return "Error"

async def clear_junk(user_id, message):
    """Check if user is accessible"""
    try:
        await message._client.send_chat_action(user_id, enums.ChatAction.TYPING)
        return True, "Success"
    except Exception as e:
        if "blocked" in str(e).lower():
            return False, "Blocked"
        elif "deleted" in str(e).lower():
            return False, "Deleted"
        else:
            return False, "Error"

async def junk_group(chat_id, message):
    """Check if group is accessible"""
    try:
        await message._client.send_chat_action(chat_id, enums.ChatAction.TYPING)
        return True, "Success", ""
    except Exception as e:
        return False, "deleted", str(e)
