class script(object):
    # START MESSAGE WITH ⏳ ANIMATION
    START_TXT = """<b>ʜᴇʏ, {}! 👋</b>
<b>ɪ'ᴍ ᴀ ᴘᴏᴡᴇʀғᴜʟ ZIP ➝ UNZIP ʙᴏᴛ 🗜️</b>
<b>ᴇxᴛʀᴀᴄᴛ & ᴄᴏᴍᴘʀᴇss ғɪʟᴇs ᴜᴘ ᴛᴏ 𝟺ɢʙ 💾</b>
<b>ᴊᴜsᴛ sᴇɴᴅ ᴀ ZIP / RAR / FILE — ɢᴇᴛ ᴜɴᴢɪᴘᴘᴇᴅ ғɪʟᴇs ⚡</b>
<b>💎 ᴘʀᴇᴍɪᴜᴍ: 4GB | 🆓 ғʀᴇᴇ: 2GB</b>"""

    GSTART_TXT = """<b>ʜᴇʏ, {}! ⏳</b>

<b>ɪ'ᴍ ᴀ ғᴀsᴛ ZIP ➝ UNZIP ʙᴏᴛ 🤖</b>
<b>ᴜɴᴢɪᴘ ғɪʟᴇs ᴜᴘ ᴛᴏ 𝟺ɢʙ 💎</b>

<b>Premium users get ultra-fast extraction 🚀</b>"""

    HELP_TXT = """<b>✨ ʜᴏᴡ ᴛᴏ ᴜɴᴢɪᴘ ғɪʟᴇs ✨</b>

<b>1️⃣ sᴇɴᴅ ᴀ ZIP / RAR / FILE 📦</b>
<b>2️⃣ ᴄʜᴏᴏꜱᴇ ᴜᴘʟᴏᴀᴅ ᴍᴏᴅᴇ (ᴠɪᴅᴇᴏ/ᴅᴏᴄ) 🎬</b>
<b>3️⃣ ᴡᴀɪᴛ ғᴏʀ ᴇxᴛʀᴀᴄᴛɪᴏɴ ⏳</b>
<b>4️⃣ ɢᴇᴛ ᴜɴᴢɪᴘᴘᴇᴅ ғɪʟᴇs 📂</b>

<b>📌 ғᴇᴀᴛᴜʀᴇs:</b>
<b>➤ Extract ZIP / RAR / 7Z files 🗜️</b>
<b>➤ Compress files into ZIP 📦</b>
<b>➤ File size up to 𝟺GB 💾</b>
<b>➤ Premium: fast unzip ⚡</b>
<b>➤ Free: normal speed 🕒</b>
<b>➤ Supports all file types 📁</b>
<b>➤ Custom thumbnail support 🖼️</b>
<b>➤ Upload as video or document 📹📄</b>
<b>➤ Forced subscription enabled ✅</b>

<b>📍 ꜱᴜᴘᴘᴏʀᴛᴇᴅ ғᴏʀᴍᴀᴛs:</b>
<b>• ZIP files: .zip</b>
<b>• RAR files: .rar</b>
<b>• 7Z files: .7z</b>
<b>• TAR files: .tar, .tar.gz, .tgz, .tar.bz2</b>

<b>🎯 ᴛʜᴜᴍʙɴᴀɪʟ ᴄᴏᴍᴍᴀɴᴅs:</b>
<b>/set_thumbnail - Set custom thumbnail</b>
<b>/show_thumbnail - View your thumbnail</b>
<b>/del_thumbnail - Delete thumbnail</b>

<b>📊 ᴏᴛʜᴇʀ ᴄᴏᴍᴍᴀɴᴅs:</b>
<b>/info - Your user information</b>
<b>/plan - Check premium plans</b>"""

    ABOUT_TXT = """<b>╭────[ ʙᴏᴛ ᴅᴇᴛᴀɪʟs ]────⍟
├⍟ Mʏ Nᴀᴍᴇ : <a href=https://t.me/{}>{}</a>
├⍟ Dᴇᴠᴇʟᴏᴘᴇʀ : <a href={}>Zᴇʀᴏᴅᴇᴠ</a>
├⍟ Oᴡɴᴇʀ : @Venuboyy
├⍟ Lɪʙʀᴀʀʏ : <a href='https://docs.pyrogram.org/'>ᴘʏʀᴏɢʀᴀᴍ</a>
├⍟ Lᴀɴɢᴜᴀɢᴇ : <a href='https://www.python.org/'>ᴘʏᴛʜᴏɴ 𝟹</a>
├⍟ Dᴀᴛᴀʙᴀsᴇ : <a href='https://www.mongodb.com/'>ᴍᴏɴɢᴏ ᴅʙ</a>
├⍟ Fɪʟᴇ Lɪᴍɪᴛ : 𝟺ɢʙ (Premium) 💎
├⍟ Fʀᴇᴇ Lɪᴍɪᴛ : 2ɢʙ 🆓
├⍟ Bᴜɪʟᴅ Sᴛᴀᴛᴜs : ᴠ1.0 [ ꜱᴛᴀʙʟᴇ ]
╰───────────────⍟</b>"""

    # PREMIUM MESSAGES
    PREMIUM_TXT = """<b>💎 ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴs 💎</b>

<b>🌟 ᴘʀᴇᴍɪᴜᴍ ʙᴇɴᴇғɪᴛs:</b>
<b>✅ 4GB file size limit</b>
<b>✅ Ultra-fast extraction</b>
<b>✅ Priority support</b>
<b>✅ No ads</b>
<b>✅ Custom thumbnail support</b>
<b>✅ Unlimited daily extractions</b>

<b>💰 ᴘʀɪᴄɪɴɢ:</b>
<b>• 1 Month - 100⭐</b>
<b>• 3 Months - 250⭐</b>
<b>• 6 Months - 450⭐</b>
<b>• 1 Year - 800⭐</b>

<b>📞 Contact @Venuboyy to purchase!</b>"""

    BPREMIUM_TXT = """<b>💎 ᴜᴘɢʀᴀᴅᴇ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ 💎</b>

<b>🎯 ғʀᴇᴇ ᴜsᴇʀs: 2GB limit</b>
<b>💎 ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs: 4GB limit</b>

<b>🚀 ɢᴇᴛ 2x ғᴀsᴛᴇʀ ᴇxᴛʀᴀᴄᴛɪᴏɴ!</b>
<b>✨ ᴜɴʟɪᴍɪᴛᴇᴅ ᴅᴀɪʟʏ ᴇxᴛʀᴀᴄᴛɪᴏɴs!</b>

<b>💰 ᴄʜᴇᴄᴋ ᴏᴜᴛ ᴏᴜʀ ᴘʟᴀɴs ʙᴇʟᴏᴡ! 👇</b>"""

    PREMIUM_END_TEXT = """<b>😔 ʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ʜᴀs ᴇxᴘɪʀᴇᴅ!</b>

<b>👋 ʜᴇʏ {},</b>
<b>ʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇss ʜᴀs ᴇɴᴅᴇᴅ.</b>

<b>ʀᴇɴᴇᴡ ɴᴏᴡ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ ᴇɴᴊᴏʏɪɴɢ 4GB ʟɪᴍɪᴛ ᴀɴᴅ ғᴀsᴛ ᴇxᴛʀᴀᴄᴛɪᴏɴ! 🚀</b>

<b>📞 ᴄᴏɴᴛᴀᴄᴛ: @Venuboyy</b>"""

    # FORCE SUBSCRIPTION
    FORCE_SUB_TEXT = """<b>⚠️ ᴘʟᴇᴀsᴇ ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs!</b>

<b>ʏᴏᴜ ᴍᴜsᴛ ᴊᴏɪɴ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ᴄʜᴀɴɴᴇʟs ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴏᴛ:</b>

<b>1️⃣ @zerodev2</b>
<b>2️⃣ @mvxyoffcail</b>

<b>ᴀғᴛᴇʀ ᴊᴏɪɴɪɴɢ, ᴄʟɪᴄᴋ "✅ ɪ ᴊᴏɪɴᴇᴅ" ʙᴜᴛᴛᴏɴ!</b>"""

    # WELCOME IMAGE
    WELCOME_IMAGE = "https://api.aniwallpaper.workers.dev/random?type=girl"

    # FORCE SUB CHANNELS
    FORCE_SUB_CHANNELS = ["zerodev2", "mvxyoffcail"]

    # FORCE SUB IMAGE
    FORCE_SUB_IMAGE = "https://i.ibb.co/pr2H8cwT/img-8312532076.jpg"

    # ADMIN INFO
    ADMIN_USERNAME = "@Venuboyy"
