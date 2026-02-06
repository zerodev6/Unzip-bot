import motor.motor_asyncio
from info import DATABASE_URI, DATABASE_NAME
from datetime import datetime
import pytz

class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.grp = self.db.groups
        self.ban = self.db.banned

    def new_user(self, id, name):
        return dict(
            id=id,
            name=name,
            ban_status=dict(
                is_banned=False,
                ban_reason="",
            ),
            expiry_time=None,
            thumbnail=None,
            join_date=datetime.now(pytz.timezone("Asia/Kolkata"))
        )

    def new_group(self, id, title):
        return dict(
            id=id,
            title=title,
            chat_status=dict(
                is_disabled=False,
                reason="",
            ),
        )

    async def add_user(self, id, name):
        user = self.new_user(id, name)
        await self.col.insert_one(user)

    async def is_user_exist(self, id):
        user = await self.col.find_one({'id': int(id)})
        return bool(user)

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def remove_ban(self, id):
        ban_status = dict(
            is_banned=False,
            ban_reason=''
        )
        await self.col.update_one({'id': id}, {'$set': {'ban_status': ban_status}})

    async def ban_user(self, user_id, ban_reason="No Reason"):
        ban_status = dict(
            is_banned=True,
            ban_reason=ban_reason
        )
        await self.col.update_one({'id': user_id}, {'$set': {'ban_status': ban_status}})

    async def get_ban_status(self, id):
        default = dict(
            is_banned=False,
            ban_reason=''
        )
        user = await self.col.find_one({'id': int(id)})
        if not user:
            return default
        return user.get('ban_status', default)

    async def get_all_users(self):
        return self.col.find({})

    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

    async def get_banned(self):
        users = self.col.find({'ban_status.is_banned': True})
        chats = self.grp.find({'chat_status.is_disabled': True})
        b_chats = [chat['id'] async for chat in chats]
        b_users = [user['id'] async for user in users]
        return b_users, b_chats

    async def add_chat(self, chat, title):
        chat = self.new_group(chat, title)
        await self.grp.insert_one(chat)

    async def get_chat(self, chat):
        chat = await self.grp.find_one({'id': int(chat)})
        return chat if chat else False

    async def re_enable_chat(self, id):
        chat_status = dict(
            is_disabled=False,
            reason=""
        )
        await self.grp.update_one({'id': int(id)}, {'$set': {'chat_status': chat_status}})

    async def update_settings(self, id, settings):
        await self.grp.update_one({'id': int(id)}, {'$set': {'settings': settings}})

    async def disable_chat(self, chat, reason="No Reason"):
        chat_status = dict(
            is_disabled=True,
            reason=reason
        )
        await self.grp.update_one({'id': int(chat)}, {'$set': {'chat_status': chat_status}})

    async def total_chat_count(self):
        count = await self.grp.count_documents({})
        return count

    async def get_all_chats(self):
        return self.grp.find({})

    async def get_db_size(self):
        return (await self.db.command("dbstats"))['dataSize']

    # Premium Functions
    async def get_user(self, user_id):
        user_id = int(user_id)
        user = await self.col.find_one({"id": user_id})
        return user if user else None

    async def update_user(self, user_data):
        user_id = user_data["id"]
        await self.col.update_one(
            {"id": user_id},
            {"$set": user_data},
            upsert=True
        )

    async def remove_premium_access(self, user_id):
        user_id = int(user_id)
        user = await self.col.find_one({"id": user_id})
        if user and user.get("expiry_time"):
            await self.col.update_one(
                {"id": user_id},
                {"$unset": {"expiry_time": ""}}
            )
            return True
        return False

    # Thumbnail Functions
    async def set_thumbnail(self, user_id, file_id):
        """Set user thumbnail"""
        await self.col.update_one(
            {'id': int(user_id)},
            {'$set': {'thumbnail': file_id}},
            upsert=True
        )

    async def get_thumbnail(self, user_id):
        """Get user thumbnail"""
        user = await self.col.find_one({'id': int(user_id)})
        if user:
            return user.get('thumbnail')
        return None

    async def delete_thumbnail(self, user_id):
        """Delete user thumbnail"""
        await self.col.update_one(
            {'id': int(user_id)},
            {'$unset': {'thumbnail': ""}}
        )

db = Database(DATABASE_URI, DATABASE_NAME)
