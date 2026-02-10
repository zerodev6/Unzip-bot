# 🚀 Quick Start Guide - Telegram Unzip Bot

## 📦 What's Inside?

Complete Telegram bot that extracts ZIP/RAR/7Z/TAR files with:
- ✅ Upload files up to **4GB** using user session
- ✅ Premium system with Telegram Stars
- ✅ Force subscription to channels
- ✅ Custom thumbnails
- ✅ Admin broadcast
- ✅ Docker support

## ⚡ Quick Setup (5 Minutes)

### Step 1: Extract Files
```bash
tar -xzf telegram-unzip-bot-final.tar.gz
cd telegram-unzip-bot
```

### Step 2: Get Your Credentials

1. **Get API Credentials**: Visit https://my.telegram.org
   - Login with your phone number
   - Go to "API Development Tools"
   - Note down `API_ID` and `API_HASH`

2. **Create Bot**: Message [@BotFather](https://t.me/BotFather)
   - Send `/newbot`
   - Choose name and username
   - Copy the bot token

3. **Generate Session String** (Required for 4GB uploads):
```bash
python3 generate_session.py
```
Follow prompts to login with your Telegram account.

### Step 3: Configure Bot
```bash
cp .env.example .env
nano .env  # or use any text editor
```

Fill in these required fields:
```env
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
SESSION_STRING=paste_session_string_here
DATABASE_URL=your_mongodb_url
ADMINS=your_telegram_user_id
```

### Step 4: Get MongoDB URL

**Option A - Free MongoDB Atlas:**
1. Go to https://www.mongodb.com/cloud/atlas
2. Create free account
3. Create cluster (choose free tier)
4. Create database user
5. Get connection string
6. Replace `<password>` with your password

**Option B - Quick test:**
```
DATABASE_URL=mongodb://localhost:27017/unzipbot
```
(Requires MongoDB installed locally)

### Step 5: Run Bot

**Option A - Docker (Recommended):**
```bash
docker-compose up -d
```

**Option B - Python:**
```bash
pip3 install -r requirements.txt
python3 bot.py
```

**Option C - Using startup script:**
```bash
chmod +x start.sh
./start.sh
```

## 🎯 Test Your Bot

1. Open Telegram and search for your bot
2. Send `/start`
3. Send a ZIP file to test extraction

## 📋 Important Files

| File | Purpose |
|------|---------|
| `bot.py` | Main bot with user session support |
| `generate_session.py` | Generate session string for 4GB uploads |
| `docker-compose.yml` | Docker deployment config |
| `start.sh` | Quick startup script |
| `.env` | Your configuration (create from .env.example) |

## 🔑 Session String - Why You Need It

**Without Session String:**
- ❌ Can only upload files up to 50MB (Telegram bot API limit)
- ✅ Bot works, but large files fail

**With Session String:**
- ✅ Upload files up to 4GB
- ✅ Uses your user account to bypass bot limits
- ✅ Required for premium features

**Security Notes:**
- Never share your session string
- It gives full access to your Telegram account
- Keep it secure in .env file

## 🐳 Docker Commands Cheat Sheet

```bash
# Start bot
docker-compose up -d

# View logs
docker-compose logs -f

# Restart bot
docker-compose restart

# Stop bot
docker-compose down

# Update bot
git pull
docker-compose up -d --build
```

## ❓ Common Issues

### "ModuleNotFoundError: No module named 'pyrogram'"
```bash
pip3 install -r requirements.txt
```

### "No SESSION_STRING configured"
```bash
python3 generate_session.py
# Add output to .env file
```

### "Bot not responding"
- Check bot token is correct
- Verify MongoDB connection
- Check logs: `docker-compose logs -f`

### "Can't upload large files"
- Verify SESSION_STRING is set
- Regenerate session if needed
- Check user session is active

## 📞 Get Help

- Developer: [@Venuboyy](https://t.me/Venuboyy)
- Channels: [@zerodev2](https://t.me/zerodev2) | [@mvxyoffcail](https://t.me/mvxyoffcail)

## 🎓 Next Steps

1. ✅ Read full `README.md` for all features
2. ✅ Configure force subscription channels
3. ✅ Set up premium system
4. ✅ Add admin users
5. ✅ Test with different archive formats

---

**Made with ❤️ by Zerodev | 🇱🇰 Sri Lanka & 🇮🇳 India**
