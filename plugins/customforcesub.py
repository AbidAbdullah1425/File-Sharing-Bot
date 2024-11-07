import os
from pyrogram import Client, filters
from pyrogram.types import Message
from config import OWNER_ID  # Make sure OWNER_ID is correctly imported from config

# Function to check if the bot has permission to export invite link in both groups and channels
async def check_bot_permissions_for_invite_link(client: Client, channel_id: int):
    try:
        # Get chat info (this will work for both groups and channels)
        chat = await client.get_chat(channel_id)

        # If it's a supergroup or channel, check bot's admin rights
        if chat.type in ['supergroup', 'channel']:
            # Get the bot's status in the chat (channel/group)
            chat_member = await client.get_chat_member(channel_id, "me")

            if chat_member.status in ['administrator', 'creator']:
                if chat_member.can_invite_to_group:  # Check permission to export invite link
                    return True, f"✅ The bot has permission to generate an invite link in the channel/group with ID {channel_id}."
                else:
                    return False, f"❌ The bot does not have permission to generate an invite link in the channel/group with ID {channel_id}."
            else:
                return False, f"❌ The bot is not an admin in the channel/group with ID {channel_id}."
        else:
            return False, "❌ The specified ID does not belong to a valid group or channel."

    except Exception as e:
        return False, f"❌ Error checking permissions for the channel/group with ID {channel_id}: {e}"

# Command to set FORCE_SUB_CHANNEL_1
@Client.on_message(filters.private & filters.user(OWNER_ID) & filters.command('setforcesub1'))
async def set_forcesub1(client: Client, message: Message):
    try:
        # Extract channel ID from the command (second word in the message)
        new_channel_id = int(message.text.split()[1])  # Example: '/setforcesub1 -1002176591513'
    except (IndexError, ValueError):
        await message.reply("❌ Please provide a valid numeric channel ID.")
        return

    # Check if the bot has permission to export an invite link in the provided channel
    is_allowed, status_message = await check_bot_permissions_for_invite_link(client, new_channel_id)

    if not is_allowed:
        await message.reply(status_message)
        return

    # If permission is granted, update the FORCE_SUB_CHANNEL_1 variable
    os.environ['FORCE_SUB_CHANNEL_1'] = str(new_channel_id)
    await message.reply(f"✅ Successfully updated FORCE_SUB_CHANNEL_1 to: {new_channel_id}")

# Command to set FORCE_SUB_CHANNEL_2
@Client.on_message(filters.private & filters.user(OWNER_ID) & filters.command('setforcesub2'))
async def set_forcesub2(client: Client, message: Message):
    try:
        new_channel_id = int(message.text.split()[1])  # Example: '/setforcesub2 -1002176591513'
    except (IndexError, ValueError):
        await message.reply("❌ Please provide a valid numeric channel ID.")
        return

    # Check if the bot has permission to export an invite link in the provided channel
    is_allowed, status_message = await check_bot_permissions_for_invite_link(client, new_channel_id)

    if not is_allowed:
        await message.reply(status_message)
        return

    # If permission is granted, update the FORCE_SUB_CHANNEL_2 variable
    os.environ['FORCE_SUB_CHANNEL_2'] = str(new_channel_id)
    await message.reply(f"✅ Successfully updated FORCE_SUB_CHANNEL_2 to: {new_channel_id}")

# Command to set FORCE_SUB_CHANNEL_3
@Client.on_message(filters.private & filters.user(OWNER_ID) & filters.command('setforcesub3'))
async def set_forcesub3(client: Client, message: Message):
    try:
        new_channel_id = int(message.text.split()[1])  # Example: '/setforcesub3 -1002176591513'
    except (IndexError, ValueError):
        await message.reply("❌ Please provide a valid numeric channel ID.")
        return

    # Check if the bot has permission to export an invite link in the provided channel
    is_allowed, status_message = await check_bot_permissions_for_invite_link(client, new_channel_id)

    if not is_allowed:
        await message.reply(status_message)
        return

    # If permission is granted, update the FORCE_SUB_CHANNEL_3 variable
    os.environ['FORCE_SUB_CHANNEL_3'] = str(new_channel_id)
    await message.reply(f"✅ Successfully updated FORCE_SUB_CHANNEL_3 to: {new_channel_id}")

# Command to set FORCE_SUB_CHANNEL_4
@Client.on_message(filters.private & filters.user(OWNER_ID) & filters.command('setforcesub4'))
async def set_forcesub4(client: Client, message: Message):
    try:
        new_channel_id = int(message.text.split()[1])  # Example: '/setforcesub4 -1002176591513'
    except (IndexError, ValueError):
        await message.reply("❌ Please provide a valid numeric channel ID.")
        return

    # Check if the bot has permission to export an invite link in the provided channel
    is_allowed, status_message = await check_bot_permissions_for_invite_link(client, new_channel_id)

    if not is_allowed:
        await message.reply(status_message)
        return

    # If permission is granted, update the FORCE_SUB_CHANNEL_4 variable
    os.environ['FORCE_SUB_CHANNEL_4'] = str(new_channel_id)
    await message.reply(f"✅ Successfully updated FORCE_SUB_CHANNEL_4 to: {new_channel_id}")
