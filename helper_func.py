import base64
import re
import asyncio
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait
from database.database import get_force_sub_channel  # Import the MongoDB function
from config import FORCE_SUB_CHANNEL_1, FORCE_SUB_CHANNEL_2, FORCE_SUB_CHANNEL_3, FORCE_SUB_CHANNEL_4, ADMINS, AUTO_DELETE_TIME, AUTO_DEL_SUCCESS_MSG

async def is_subscribed(filter, client, update):
    # Retrieve the force subscription channel from MongoDB
    try:
        force_sub_channel = get_force_sub_channel("FORCE_SUB_CHANNEL_1")
    except Exception as e:
        print(f"Error retrieving channel from MongoDB: {e}")
        force_sub_channel = None

    # Fallback to config.py if no channel is found in MongoDB
    if not force_sub_channel:
        force_sub_channel = FORCE_SUB_CHANNEL_1

    # Skip the check if no valid channel ID is found
    if not force_sub_channel:
        return True

    user_id = update.from_user.id

    # Bypass check for admins
    if user_id in ADMINS:
        return True

    # Allowed member statuses
    allowed_statuses = {ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER}

    # Check if the user is subscribed to the channel
    try:
        member = await client.get_chat_member(chat_id=force_sub_channel, user_id=user_id)
        if member.status not in allowed_statuses:
            return False
    except UserNotParticipant:
        return False
    except FloodWait as e:
        print(f"FloodWait error: Waiting for {e.value} seconds")
        await asyncio.sleep(e.value)
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

    # If the user is subscribed, return True
    return True
    

async def encode(string):
    string_bytes = string.encode("ascii")
    base64_bytes = base64.urlsafe_b64encode(string_bytes)
    base64_string = (base64_bytes.decode("ascii")).strip("=")
    return base64_string

async def decode(base64_string):
    base64_string = base64_string.strip("=")  # Handle padding errors for older links
    base64_bytes = (base64_string + "=" * (-len(base64_string) % 4)).encode("ascii")
    string_bytes = base64.urlsafe_b64decode(base64_bytes)
    return string_bytes.decode("ascii")

async def get_messages(client, message_ids):
    messages = []
    total_messages = 0
    while total_messages != len(message_ids):
        temp_ids = message_ids[total_messages:total_messages+200]
        try:
            msgs = await client.get_messages(
                chat_id=client.db_channel.id,
                message_ids=temp_ids
            )
        except FloodWait as e:
            await asyncio.sleep(e.x)
            msgs = await client.get_messages(
                chat_id=client.db_channel.id,
                message_ids=temp_ids
            )
        except Exception:
            pass
        total_messages += len(temp_ids)
        messages.extend(msgs)
    return messages

async def get_message_id(client, message):
    if message.forward_from_chat:
        if message.forward_from_chat.id == client.db_channel.id:
            return message.forward_from_message_id
        else:
            return 0
    elif message.forward_sender_name:
        return 0
    elif message.text:
        pattern = "https://t.me/(?:c/)?(.*)/(\d+)"
        matches = re.match(pattern, message.text)
        if not matches:
            return 0
        channel_id = matches.group(1)
        msg_id = int(matches.group(2))
        if channel_id.isdigit():
            if f"-100{channel_id}" == str(client.db_channel.id):
                return msg_id
        else:
            if channel_id == client.db_channel.username:
                return msg_id
    else:
        return 0

def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    hmm = len(time_list)
    for x in range(hmm):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += f"{time_list.pop()}, "
    time_list.reverse()
    up_time += ":".join(time_list)
    return up_time

async def delete_file(messages, client, process):
    await asyncio.sleep(AUTO_DELETE_TIME)
    for msg in messages:
        try:
            await client.delete_messages(chat_id=msg.chat.id, message_ids=[msg.id])
        except Exception as e:
            await asyncio.sleep(e.x)
            print(f"The attempt to delete the media {msg.id} was unsuccessful: {e}")

    await process.edit_text(AUTO_DEL_SUCCESS_MSG)


subscribed = filters.create(is_subscribed)
