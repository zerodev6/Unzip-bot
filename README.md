# Unzip Bot - Professional Archive Extraction Bot

A powerful Telegram bot for extracting and managing archive files with premium features.

## Features

- ✅ Extract ZIP, RAR, 7Z, TAR files
- ✅ File size limits: 2GB (Free) / 4GB (Premium)
- ✅ Custom thumbnail support
- ✅ Premium subscription via Telegram Stars
- ✅ Fast download/upload with progress bars
- ✅ Force subscription to channels
- ✅ Admin controls (ban/unban users, broadcast)
- ✅ MongoDB database integration
- ✅ User statistics and info

## Supported Formats

- **ZIP files**: .zip
- **RAR files**: .rar
- **7Z files**: .7z
- **TAR files**: .tar, .tar.gz, .tgz, .tar.bz2

## Setup Instructions

### 1. Environment Variables

Create a `.env` file or set these variables:

```env
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
STRING_SESSION=your_string_session  # Optional, for 4GB upload support
DATABASE_URI=your_mongodb_uri
DATABASE_NAME=unzip_bot
ADMINS=admin_user_id admin_user_id2  # Space-separated
PREMIUM_LOGS=log_channel_id  # Optional
```

### 2. Get API Credentials

1. Go to [my.telegram.org](https://my.telegram.org)
2. Login with your phone number
3. Go to "API Development Tools"
4. Create a new application
5. Copy `API_ID` and `API_HASH`

### 3. Get Bot Token

1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Use `/newbot` command
3. Follow the instructions
4. Copy the bot token

### 4. Get String Session (Optional)

For uploading files larger than 2GB, you need a user session:

```python
from pyrogram import Client

api_id = "YOUR_API_ID"
api_hash = "YOUR_API_HASH"

with Client("my_account", api_id=api_id, api_hash=api_hash) as app:
    print(app.export_session_string())
```

Run this script and copy the string session.

### 5. MongoDB Setup

1. Create account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a cluster
3. Get connection string
4. Replace `<password>` with your database password

### 6. Installation

```bash
# Clone repository
git clone <your-repo-url>
cd unzip_bot

# Install dependencies
pip install -r requirements.txt

# Run the bot
python bot.py
```

## Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
```

## Commands

### User Commands
- `/start` - Start the bot
- `/help` - Get help
- `/about` - About the bot
- `/myplan` - Check premium status
- `/plan` - Buy premium
- `/addthum` - Add thumbnail
- `/viewthum` - View thumbnail
- `/delectthum` - Delete thumbnail
- `/info` - Your user info

### Admin Commands
- `/add_premium user_id time` - Add premium to user
- `/remove_premium user_id` - Remove premium
- `/get_premium user_id` - Get premium info
- `/premium_users` - List all premium users
- `/ban user_id [reason]` - Ban user
- `/unban user_id` - Unban user
- `/banned` - List banned users
- `/stats` - Bot statistics
- `/broadcast` - Broadcast to all users
- `/grp_broadcast` - Broadcast to all groups
- `/clear_junk` - Remove blocked/deleted users
- `/junk_group` - Remove inactive groups
- `/disable_chat chat_id [reason]` - Disable group
- `/enable_chat chat_id` - Enable group

## Premium Plans

- 100⭐ - 1 Month
- 250⭐ - 3 Months
- 400⭐ - 6 Months
- 700⭐ - 1 Year

## File Limits

- **Free Users**: 2GB per file
- **Premium Users**: 4GB per file

## Support

- Developer: [@Venuboyy](https://t.me/Venuboyy)
- Channel: [@zerodev2](https://t.me/zerodev2)

## License

This project is licensed under the MIT License.

## Credits

- Developed by Zerodev
- Built with Pyrogram
- Database: MongoDB
