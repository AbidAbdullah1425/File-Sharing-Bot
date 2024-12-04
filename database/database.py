import pymongo
from config import DB_URI, DB_NAME

# MongoDB setup
dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]

# Collections
user_data = database['users']
fsub_collection = database['fsub_ids']  # New collection for force subscription

# User management functions
async def present_user(user_id: int):
    found = user_data.find_one({'_id': user_id})
    return bool(found)

async def add_user(user_id: int):
    user_data.insert_one({'_id': user_id})
    return

async def full_userbase():
    user_docs = user_data.find()
    user_ids = []
    for doc in user_docs:
        user_ids.append(doc['_id'])
    return user_ids

async def del_user(user_id: int):
    user_data.delete_one({'_id': user_id})
    return

# Force subscription management functions
def get_force_sub_channels():
    """Fetch dynamic force subscription channels."""
    result = fsub_collection.find_one({"key": "force_sub_channels"})
    return result["channels"] if result else []

def set_force_sub_channel(channel_id):
    """Update dynamic force subscription channel with a single ID."""
    fsub_collection.update_one(
        {"key": "FORCE_SUB_CHANNEL_1"},  # Use a key for single channel ID
        {"$set": {"FSUB_ID": channel_id}},  # Store a single channel ID
        upsert=True
    )
