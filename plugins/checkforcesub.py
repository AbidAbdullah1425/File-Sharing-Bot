import os
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait
from bot import Bot  # Assuming Bot is imported from bot.py
from config import APP_ID, API_HASH, FORCE_SUB_CHANNEL_1, FORCE_SUB_CHANNEL_2, FORCE_SUB_CHANNEL_3, FORCE_SUB_CHANNEL_4, OWNER_ID

# Function to check if bot has permission to export invite link
async def check_bot_permissions_for_invite_link(client: Bot, channel_id: str):
    try:
        # Check if the provided ID is a public channel (@username) or a private one (numeric ID)
        if channel_id.startswith('@'):
            # Public channel: Check using username
            chat = await client.get_chat(channel_id)
        else:
            # Private channel or supergroup: Check using numeric ID
            chat = await client.get_chat(int(channel_id))

        # If it's a supergroup or channel, check bot's admin rights
        if chat.type in ['supergroup', 'channel']:
            chat_member = await client.get_chat_member(channel_id, "me")
            if chat_member.status in ['administrator', 'creator']:
                if chat_member.can_invite_to_group:  # Check permission to export invite link
                    return True, f"✅ The bot has permission to generate an invite link in the channel/group with ID {channel_id}"
                else:
                    return False, "❌ The bot does not have permission to export the invite link in this channel/group."
            else:
                return False, "❌ The bot is not an admin in this channel/group."
        else:
            return False, "❌ The specified ID does not belong to a valid group or channel."
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

# Command to set FORCE_SUB_CHANNEL_1
@Bot.on_message(filters.private & filters.user(OWNER_ID) & filters.command('setforcesub1'))
async def set_forcesub1(client: Bot, message):
    try:
        # Extract the channel ID from the message
        channel_id = message.text.split(' ')[1]

        # Ensure the channel ID is valid
        if not (channel_id.startswith('-100') or channel_id.startswith('@')):
            await message.reply("❌ Invalid channel ID format. It should start with '-100' for private channels or '@username' for public channels.")
            return

        # Check bot's permission to export invite link
        is_permitted, permission_message = await check_bot_permissions_for_invite_link(client, channel_id)
        if is_permitted:
            os.environ["FORCE_SUB_CHANNEL_1"] = channel_id  # Save the new channel ID to environment variable
            await message.reply(f"✅ FORCE_SUB_CHANNEL_1 has been updated to: {channel_id}")
        else:
            await message.reply(permission_message)
    except IndexError:
        await message.reply("❌ Please provide a valid channel ID after the command. Example: `/setforcesub1 -1002176591513`")

# Command to set FORCE_SUB_CHANNEL_2
@Bot.on_message(filters.private & filters.user(OWNER_ID) & filters.command('setforcesub2'))
async def set_forcesub2(client: Bot, message):
    try:
        # Extract the channel ID from the message
        channel_id = message.text.split(' ')[1]

        # Ensure the channel ID is valid
        if not (channel_id.startswith('-100') or channel_id.startswith('@')):
            await message.reply("❌ Invalid channel ID format. It should start with '-100' for private channels or '@username' for public channels.")
            return

        # Check bot's permission to export invite link
        is_permitted, permission_message = await check_bot_permissions_for_invite_link(client, channel_id)
        if is_permitted:
            os.environ["FORCE_SUB_CHANNEL_2"] = channel_id  # Save the new channel ID to environment variable
            await message.reply(f"✅ FORCE_SUB_CHANNEL_2 has been updated to: {channel_id}")
        else:
            await message.reply(permission_message)
    except IndexError:
        await message.reply("❌ Please provide a valid channel ID after the command. Example: `/setforcesub2 -1002176591513`")

# Command to set FORCE_SUB_CHANNEL_3
@Bot.on_message(filters.private & filters.user(OWNER_ID) & filters.command('setforcesub3'))
async def set_forcesub3(client: Bot, message):
    try:
        # Extract the channel ID from the message
        channel_id = message.text.split(' ')[1]

        # Ensure the channel ID is valid
        if not (channel_id.startswith('-100') or channel_id.startswith('@')):
            await message.reply("❌ Invalid channel ID format. It should start with '-100' for private channels or '@username' for public channels.")
            return

        # Check bot's permission to export invite link
        is_permitted, permission_message = await check_bot_permissions_for_invite_link(client, channel_id)
        if is_permitted:
            os.environ["FORCE_SUB_CHANNEL_3"] = channel_id  # Save the new channel ID to environment variable
            await message.reply(f"✅ FORCE_SUB_CHANNEL_3 has been updated to: {channel_id}")
        else:
            await message.reply(permission_message)
    except IndexError:
        await message.reply("❌ Please provide a valid channel ID after the command. Example: `/setforcesub3 -1002176591513`")

# Command to set FORCE_SUB_CHANNEL_4
@Bot.on_message(filters.private & filters.user(OWNER_ID) & filters.command('setforcesub4'))
async def set_forcesub4(client: Bot, message):
    try:
        # Extract the channel ID from the message
        channel_id = message.text.split(' ')[1]

        # Ensure the channel ID is valid
        if not (channel_id.startswith('-100') or channel_id.startswith('@')):
            await message.reply("❌ Invalid channel ID format. It should start with '-100' for private channels or '@username' for public channels.")
            return

        # Check bot's permission to export invite link
        is_permitted, permission_message = await check_bot_permissions_for_invite_link(client, channel_id)
        if is_permitted:
            os.environ["FORCE_SUB_CHANNEL_4"] = channel_id  # Save the new channel ID to environment variable
            await message.reply(f"✅ FORCE_SUB_CHANNEL_4 has been updated to: {channel_id}")
        else:
            await message.reply(permission_message)
    except IndexError:
        await message.reply("❌ Please provide a valid channel ID after the command. Example: `/setforcesub4 -1002176591513`")

# Subscription Checking Function (used in your other file)
async def is_subscribed(filter, client, update):
    if not (FORCE_SUB_CHANNEL_1 or FORCE_SUB_CHANNEL_2 or FORCE_SUB_CHANNEL_3 or FORCE_SUB_CHANNEL_4):
        return True

    user_id = update.from_user.id
    if user_id in ADMINS:
        return True

    member_status = [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]
    for channel_id in [FORCE_SUB_CHANNEL_1, FORCE_SUB_CHANNEL_2, FORCE_SUB_CHANNEL_3, FORCE_SUB_CHANNEL_4]:
        if not channel_id:
            continue

        try:
            member = await client.get_chat_member(chat_id=channel_id, user_id=user_id)
        except UserNotParticipant:
            return False

        if member.status not in member_status:
            return False

    return True

# Make sure that the bot is initialized and running correctly with the correct `APP_ID` and `API_HASH`
bot = Bot("my_bot", api_id=APP_ID, api_hash=API_HASH, bot_token="your_bot_token")  # Replace with actual bot token
bot.run()
