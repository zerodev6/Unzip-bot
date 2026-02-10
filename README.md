# 🗜️ Telegram Unzip Bot

A powerful Telegram bot that extracts ZIP, RAR, 7Z, and TAR archive files. Supports premium features with file size limits up to 4GB and large file uploads using user session.

## ✨ Features

### 🎯 Core Features
- **Extract Multiple Formats**: ZIP, RAR, 7Z, TAR, TAR.GZ, TGZ, TAR.BZ2
- **Upload Modes**: Upload as Video or Document
- **Large File Support**: Upload files up to 4GB using user session
- **Custom Thumbnails**: Set custom thumbnails for uploads
- **File Size Limits**:
  - Free Users: 2GB
  - Premium Users: 4GB
- **Force Subscription**: Require users to join channels
- **Premium System**: Telegram Star payment integration
- **Admin Broadcast**: Broadcast messages to users/groups
- **User Management**: Track users and premium status

### 💎 Premium Features
- 4GB file size limit
- Ultra-fast extraction
- Priority support
- Custom thumbnail support
- Unlimited daily extractions

### 📋 Supported Archive Formats
- ZIP files (.zip)
- RAR files (.rar)
- 7Z files (.7z)
- TAR files (.tar, .tar.gz, .tgz, .tar.bz2)

## 🚀 Deployment

### Prerequisites
- Python 3.8 or higher
- MongoDB database
- Telegram Bot Token
- API ID and API Hash from my.telegram.org
- **Session String** (for uploading files larger than 50MB)

### Installation

#### Method 1: Manual Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd telegram-unzip-bot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Generate Session String**
```bash
python generate_session.py
```
Follow the prompts to generate your session string. This is **required** for uploading files larger than 50MB.

4. **Set up environment variables**

Create a `.env` file:

```env
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
SESSION_STRING=your_session_string_here
DATABASE_URL=your_mongodb_url
ADMINS=123456789,987654321
FORCE_SUB_CHANNELS=channel1,channel2
PREMIUM_LOGS=channel_id
BOT_USERNAME=your_bot_username
```

5. **Run the bot**
```bash
python bot.py
```

#### Method 2: Docker Deployment (Recommended)

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd telegram-unzip-bot
```

2. **Generate Session String**
```bash
python generate_session.py
```

3. **Create .env file** (see above for format)

4. **Build and run with Docker Compose**
```bash
docker-compose up -d
```

5. **View logs**
```bash
docker-compose logs -f
```

6. **Stop the bot**
```bash
docker-compose down
```

#### Method 3: Docker without Compose

```bash
# Build the image
docker build -t unzip-bot .

# Run the container
docker run -d \
  --name telegram-unzip-bot \
  --env-file .env \
  -v $(pwd)/downloads:/app/downloads \
  unzip-bot

# View logs
docker logs -f telegram-unzip-bot

# Stop the bot
docker stop telegram-unzip-bot
```

### Deploy on VPS/Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker and Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo apt install docker-compose -y

# Clone and deploy
git clone <your-repo-url>
cd telegram-unzip-bot
python generate_session.py  # Generate session
nano .env  # Edit configuration
docker-compose up -d
```

## 📝 Bot Commands

### User Commands
- `/start` - Start the bot
- `/help` - Get help information
- `/about` - About the bot
- `/info` - Your user information
- `/plan` - Check premium plans
- `/myplan` - Your current premium plan
- `/set_thumbnail` - Set custom thumbnail (reply to photo)
- `/show_thumbnail` - View your current thumbnail
- `/del_thumbnail` - Delete your thumbnail

### Admin Commands
- `/broadcast` - Broadcast message to all users
- `/grp_broadcast` - Broadcast to all groups
- `/add_premium <user_id> <time>` - Add premium to user
  - Example: `/add_premium 123456789 1 month`
- `/remove_premium <user_id>` - Remove premium from user
- `/get_premium <user_id>` - Get premium details
- `/premium_users` - List all premium users
- `/clear_junk` - Clean inactive users from database
- `/junk_group` - Clean inactive groups

## 🎨 File Structure

```
.
├── bot.py              # Main bot file with user session support
├── config.py           # Configuration settings
├── database.py         # MongoDB database handler
├── script.py           # Bot messages and texts
├── utils.py            # Helper functions
├── premium.py          # Premium management
├── broadcast.py        # Broadcast system
├── generate_session.py # Session string generator
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose configuration
├── .dockerignore       # Docker ignore file
├── .env.example        # Environment variables template
└── README.md          # This file
```

## ⚙️ Configuration

### Session String (Important!)

The session string allows the bot to upload files larger than 50MB (up to 4GB) using your Telegram user account.

**Generate Session String:**
```bash
python generate_session.py
```

Or use online generator: https://replit.com/@subinps/generatepyrogramsession

**⚠️ Security Notes:**
- Never share your session string
- It gives full access to your Telegram account
- Keep it secure like a password
- Only use with trusted bots

### Premium Plans (Telegram Stars)
Edit in `config.py`:
```python
STAR_PREMIUM_PLANS = {
    100: "1 month",
    250: "3 months",
    450: "6 months",
    800: "1 year"
}
```

### Force Subscription Channels
Set in environment variables:
```env
FORCE_SUB_CHANNELS=channel1,channel2
```

### File Size Limits
Edit in `config.py`:
```python
MAX_FILE_SIZE_FREE = 2 * 1024 * 1024 * 1024  # 2GB
MAX_FILE_SIZE_PREMIUM = 4 * 1024 * 1024 * 1024  # 4GB
```

## 📊 Database Schema

### Users Collection
```json
{
  "id": 123456789,
  "join_date": "2025-02-10",
  "expiry_time": "2025-03-10",
  "thumbnail": "path/to/thumbnail.jpg"
}
```

### Chats Collection
```json
{
  "id": -1001234567890,
  "title": "Group Name",
  "join_date": "2025-02-10"
}
```

## 🔧 Troubleshooting

### Bot not responding
- Check if bot token is correct
- Verify bot is running
- Check MongoDB connection

### Files not extracting
- Ensure sufficient disk space
- Check file format is supported
- Verify file isn't corrupted

### Large files not uploading (over 50MB)
- Verify SESSION_STRING is set correctly
- Check user session is valid
- Regenerate session string if needed

### Premium not working
- Check MongoDB connection
- Verify expiry_time is set correctly
- Check timezone settings

### Docker issues
- Ensure Docker is installed: `docker --version`
- Check if port is available
- View logs: `docker-compose logs -f`

## 📞 Support

- Developer: [@Venuboyy](https://t.me/Venuboyy)
- Support Channels:
  - [@zerodev2](https://t.me/zerodev2)
  - [@mvxyoffcail](https://t.me/mvxyoffcail)

## 📜 License

This project is for educational purposes. Use at your own risk.

## 🙏 Credits

- **Pyrogram** - MTProto API framework
- **MongoDB** - Database
- **py7zr** - 7Z extraction
- **rarfile** - RAR extraction
- **Docker** - Containerization

## 🌟 Features Coming Soon

- ✅ Torrent download support
- ✅ Multi-archive extraction
- ✅ Password-protected archives
- ✅ Batch file processing
- ✅ Advanced statistics

## 💝 Donate

Support development:
- Contact [@Venuboyy](https://t.me/Venuboyy)

---

<p align="center">Made with ❤️ by Zerodev</p>
<p align="center">🇱🇰 Sri Lanka & 🇮🇳 India</p>
