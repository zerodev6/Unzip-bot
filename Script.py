class script(object):
    # START MESSAGE WITH ⏳ ANIMATION
    START_TXT = """<b>ʜᴇʏ, {}! ⏳</b>
<b>ɪ'ᴍ ᴀ ᴘᴏᴡᴇʀғᴜʟ ZIP ➝ UNZIP ʙᴏᴛ 🗜️</b>
<b>ᴇxᴛʀᴀᴄᴛ & ᴄᴏᴍᴘʀᴇss ғɪʟᴇs ᴜᴘ ᴛᴏ 𝟺ɢʙ 💾</b>
<b>🇱🇰 Greetings from Sri Lanka & 🇮🇳 India!</b>
<b>ᴊᴜsᴛ sᴇɴᴅ ᴀ ZIP / RAR / FILE — ɢᴇᴛ ᴜɴᴢɪᴘᴘᴇᴅ ғɪʟᴇs ⚡</b>"""

    GSTART_TXT = """<b>ʜᴇʏ, {}! ⏳</b>
<b>ɪ'ᴍ ᴀ ғᴀsᴛ ZIP ➝ UNZIP ʙᴏᴛ 🤖</b>
<b>ᴜɴᴢɪᴘ ғɪʟᴇs ᴜᴘ ᴛᴏ 𝟺ɢʙ 💎</b>
<b>Premium users get ultra-fast extraction 🚀</b>"""

    HELP_TXT = """<b>
✨ ʜᴏᴡ ᴛᴏ ᴜɴᴢɪᴘ ғɪʟᴇs ✨
1️⃣ sᴇɴᴅ ᴀ ZIP / RAR / FILE 📦
2️⃣ ᴡᴀɪᴛ ғᴏʀ ᴇxᴛʀᴀᴄᴛɪᴏɴ ⏳
3️⃣ ɢᴇᴛ ᴜɴᴢɪᴘᴘᴇᴅ ғɪʟᴇs 📂

📌 ғᴇᴀᴛᴜʀᴇs:
➤ Extract ZIP / RAR / 7Z files 🗜️
➤ Compress files into ZIP 📦
➤ File size up to 𝟺GB 💾
➤ Premium: fast unzip ⚡
➤ Free: normal speed 🕒
➤ Supports all file types 📁
➤ Forced subscription enabled

🎯 Commands:
/start - Start the bot
/help - Get help
/about - About bot
/myplan - Check premium status
/plan - Buy premium
/addthum - Add thumbnail
/viewthum - View thumbnail
/delectthum - Delete thumbnail
/info - Your user info
</b>"""

    ABOUT_TXT = """<b>╭────[ ʙᴏᴛ ᴅᴇᴛᴀɪʟs ]────⍟
├⍟ Mʏ Nᴀᴍᴇ : <a href=https://t.me/{}>{}</a>
├⍟ Dᴇᴠᴇʟᴏᴘᴇʀ : <a href={}>Zᴇʀᴏᴅᴇᴠ</a>
├⍟ Lɪʙʀᴀʀʏ : <a href='https://docs.pyrogram.org/'>ᴘʏʀᴏɢʀᴀᴍ</a>
├⍟ Lᴀɴɢᴜᴀɢᴇ : <a href='https://www.python.org/'>ᴘʏᴛʜᴏɴ 𝟹</a>
├⍟ Dᴀᴛᴀʙᴀsᴇ : <a href='https://www.mongodb.com/'>ᴍᴏɴɢᴏ ᴅʙ</a>
├⍟ Fɪʟᴇ Lɪᴍɪᴛ : 𝟺ɢʙ 💾
├⍟ Bᴜɪʟᴅ Sᴛᴀᴛᴜs : ᴠ1.0 [ ꜱᴛᴀʙʟᴇ ]
╰───────────────⍟</b>"""

    PREMIUM_END_TEXT = """👋 ʜᴇʏ {},

⚠️ ʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ sᴜʙsᴄʀɪᴘᴛɪᴏɴ ʜᴀs ᴇxᴘɪʀᴇᴅ!

🔄 ʀᴇɴᴇᴡ ɴᴏᴡ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ ᴇɴᴊᴏʏɪɴɢ:
✨ 4GB file extraction
⚡ Ultra-fast unzip speed
🚀 Priority processing

💎 Use /plan to renew your premium!"""

    BPREMIUM_TXT = """<b>💎 ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴs 💎

🆓 ғʀᴇᴇ ᴜsᴇʀs:
• File limit: 2GB
• Normal extraction speed
• Standard priority

⭐ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs:
• File limit: 4GB
• Ultra-fast extraction ⚡
• High priority processing
• No ads

💰 ᴘʀɪᴄɪɴɢ (Telegram Stars):
• 100⭐ - 1 month
• 250⭐ - 3 months
• 400⭐ - 6 months
• 700⭐ - 1 year

🎁 Get premium now and enjoy unlimited power!</b>"""

    FORCE_SUB_TEXT = """<b>⚠️ ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs ⚠️

To use this bot, you must join our channels:

{channels}

After joining, click the button below to check again!</b>"""

    THUMBNAIL_TEXT = """<b>🖼️ ᴛʜᴜᴍʙɴᴀɪʟ sᴇᴛᴛɪɴɢs

Your current thumbnail:</b>"""

    NO_THUMBNAIL_TEXT = """<b>❌ ɴᴏ ᴛʜᴜᴍʙɴᴀɪʟ sᴇᴛ

You haven't set a thumbnail yet.
Send a photo to set it as your thumbnail.</b>"""

    THUMBNAIL_SAVED = """<b>✅ ᴛʜᴜᴍʙɴᴀɪʟ sᴀᴠᴇᴅ!

Your custom thumbnail has been saved successfully!</b>"""

    THUMBNAIL_DELETED = """<b>🗑️ ᴛʜᴜᴍʙɴᴀɪʟ ᴅᴇʟᴇᴛᴇᴅ!

Your thumbnail has been removed.</b>"""
