import motor.motor_asyncio
from config import Config
import datetime
import pytz

class Database:
    def __init__(self, uri):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client['UnzipBot']
        self.users = self.db['users']
        self.chats = self.db['chats']

    # User Management
    async def add_user(self, user_id):
        """Add a new user to the database"""
        try:
            user = await self.users.find_one({'id': user_id})
            if not user:
                await self.users.insert_one({
                    'id': user_id,
                    'join_date': datetime.datetime.now(),
                    'expiry_time': None,
                    'thumbnail': None
                })
            return True
        except Exception as e:
            print(f"Error adding user: {e}")
            return False

    async def get_user(self, user_id):
        """Get user data"""
        try:
            return await self.users.find_one({'id': user_id})
        except Exception as e:
            print(f"Error getting user: {e}")
            return None

    async def get_all_users(self):
        """Get all users"""
        try:
            return self.users.find({})
        except Exception as e:
            print(f"Error getting all users: {e}")
            return []

    async def total_users_count(self):
        """Get total users count"""
        try:
            return await self.users.count_documents({})
        except Exception as e:
            print(f"Error counting users: {e}")
            return 0

    async def delete_user(self, user_id):
        """Delete a user"""
        try:
            await self.users.delete_one({'id': user_id})
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False

    # Premium User Management
    async def is_premium_user(self, user_id):
        """Check if user is premium"""
        try:
            user = await self.get_user(user_id)
            if user and user.get('expiry_time'):
                expiry = user['expiry_time']
                if isinstance(expiry, datetime.datetime):
                    current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
                    if expiry.tzinfo is None:
                        expiry = pytz.timezone("Asia/Kolkata").localize(expiry)
                    return current_time < expiry
            return False
        except Exception as e:
            print(f"Error checking premium status: {e}")
            return False

    async def update_user(self, user_data):
        """Update user data"""
        try:
            user_id = user_data['id']
            await self.users.update_one(
                {'id': user_id},
                {'$set': user_data},
                upsert=True
            )
            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            return False

    async def remove_premium_access(self, user_id):
        """Remove premium access from user"""
        try:
            await self.users.update_one(
                {'id': user_id},
                {'$set': {'expiry_time': None}}
            )
            return True
        except Exception as e:
            print(f"Error removing premium: {e}")
            return False

    # Thumbnail Management
    async def set_thumbnail(self, user_id, thumbnail_path):
        """Set user thumbnail"""
        try:
            await self.users.update_one(
                {'id': user_id},
                {'$set': {'thumbnail': thumbnail_path}},
                upsert=True
            )
            return True
        except Exception as e:
            print(f"Error setting thumbnail: {e}")
            return False

    async def get_thumbnail(self, user_id):
        """Get user thumbnail"""
        try:
            user = await self.get_user(user_id)
            return user if user and user.get('thumbnail') else None
        except Exception as e:
            print(f"Error getting thumbnail: {e}")
            return None

    async def delete_thumbnail(self, user_id):
        """Delete user thumbnail"""
        try:
            await self.users.update_one(
                {'id': user_id},
                {'$set': {'thumbnail': None}}
            )
            return True
        except Exception as e:
            print(f"Error deleting thumbnail: {e}")
            return False

    # Chat Management (for groups)
    async def add_chat(self, chat_id, chat_title):
        """Add a chat to database"""
        try:
            chat = await self.chats.find_one({'id': chat_id})
            if not chat:
                await self.chats.insert_one({
                    'id': chat_id,
                    'title': chat_title,
                    'join_date': datetime.datetime.now()
                })
            return True
        except Exception as e:
            print(f"Error adding chat: {e}")
            return False

    async def get_all_chats(self):
        """Get all chats"""
        try:
            return self.chats.find({})
        except Exception as e:
            print(f"Error getting chats: {e}")
            return []

    async def total_chat_count(self):
        """Get total chats count"""
        try:
            return await self.chats.count_documents({})
        except Exception as e:
            print(f"Error counting chats: {e}")
            return 0

    async def delete_chat(self, chat_id):
        """Delete a chat"""
        try:
            await self.chats.delete_one({'id': chat_id})
            return True
        except Exception as e:
            print(f"Error deleting chat: {e}")
            return False

# Initialize database
db = Database(Config.DATABASE_URL)
