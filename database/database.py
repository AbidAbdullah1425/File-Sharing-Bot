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
    """Check if a user exists in the database."""
    try:
        found = user_data.find_one({'_id': user_id})
        return bool(found)
    except Exception as e:
        print(f"Error in present_user: {e}")
        return False

async def add_user(user_id: int):
    """Add a new user to the database."""
    try:
        if not await present_user(user_id):
            user_data.insert_one({'_id': user_id})
            print(f"User {user_id} added to database.")
    except Exception as e:
        print(f"Error in add_user: {e}")

async def full_userbase():
    """Retrieve the full list of user IDs."""
    try:
        user_docs = user_data.find()
        return [doc['_id'] for doc in user_docs]
    except Exception as e:
        print(f"Error in full_userbase: {e}")
        return []

async def del_user(user_id: int):
    """Delete a user from the database."""
    try:
        user_data.delete_one({'_id': user_id})
        print(f"User {user_id} deleted from database.")
    except Exception as e:
        print(f"Error in del_user: {e}")

# Force subscription functions
def get_force_sub_channel():
    """Fetch the dynamic force subscription channel."""
    try:
        result = fsub_collection.find_one({"key": "FORCE_SUB_CHANNEL_1"})
        return result["FSUB_ID"] if result else None
    except Exception as e:
        print(f"Error in get_force_sub_channel: {e}")
        return None

def set_force_sub_channel(channel_id):
    """Update dynamic force subscription channel with a single ID."""
    try:
        fsub_collection.update_one(
            {"key": "FORCE_SUB_CHANNEL_1"},  # Use a key for single channel ID
            {"$set": {"FSUB_ID": channel_id}},  # Store a single channel ID
            upsert=True
        )
        print(f"Force subscription channel set to {channel_id}.")
    except Exception as e:
        print(f"Error in set_force_sub_channel: {e}")
