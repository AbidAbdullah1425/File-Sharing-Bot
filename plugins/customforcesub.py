import os
from pyrogram import Client, filters
from pyrogram.errors import ChatWriteForbidden
from pyrogram.types import Message
from config import FORCE_SUB_CHANNEL_1, FORCE_SUB_CHANNEL_2, FORCE_SUB_CHANNEL_3, FORCE_SUB_CHANNEL_4, OWNER_ID

# Define a function to check if the bot can export the invite link
async def can_export_invite_link(client, channel_id):
    try:
        # Check if the bot has permission to export an invite link in the given channel
        chat_member = await client.get_chat_member(channel_id, "me")
        if chat_member.status in ['administrator', 'creator']:
            if chat_member.can_invite_to_group_via_link:
                return True
            else:
                return False, "❌ The bot cannot generate an invite link in this channel."
        else:
            return False, "❌ The bot is not an admin or creator in this channel."
    except Exception as e:
        return False, f"❌ Error checking permissions: {str(e)}"

# Handle the setforcesub1 command
@Client.on_message(filters.private & filters.user(OWNER_ID) & filters.command('setforcesub1'))
async def set_forcesub1(client: Client, message: Message):
    # Ask the owner for the channel ID
    await message.reply("Please provide the channel ID for FORCE_SUB_CHANNEL_1 (numeric ID):")
    
    # Wait for the owner's response
    response = await client.ask(
        message.from_user.id,
        text="Please provide the channel ID (numeric ID):",
        filters=filters.text,
        timeout=60
    )

    try:
        channel_id = int(response.text)
    except ValueError:
        await message.reply("❌ Invalid input. Please provide a valid numeric channel ID.")
        return
    
    # Check if the bot can export the invite link in the channel
    can_invite, status_message = await can_export_invite_link(client, channel_id)
    
    if not can_invite:
        await message.reply(status_message)
        return
    
    # Update the FORCE_SUB_CHANNEL_1 variable
    os.environ["FORCE_SUB_CHANNEL_1"] = str(channel_id)
    await message.reply(f"✅ Successfully updated FORCE_SUB_CHANNEL_1 to {channel_id}")

# Handle the setforcesub2 command
@Client.on_message(filters.private & filters.user(OWNER_ID) & filters.command('setforcesub2'))
async def set_forcesub2(client: Client, message: Message):
    await message.reply("Please provide the channel ID for FORCE_SUB_CHANNEL_2 (numeric ID):")
    
    # Wait for the owner's response
    response = await client.ask(
        message.from_user.id,
        text="Please provide the channel ID (numeric ID):",
        filters=filters.text,
        timeout=60
    )

    try:
        channel_id = int(response.text)
    except ValueError:
        await message.reply("❌ Invalid input. Please provide a valid numeric channel ID.")
        return
    
    # Check if the bot can export the invite link in the channel
    can_invite, status_message = await can_export_invite_link(client, channel_id)
    
    if not can_invite:
        await message.reply(status_message)
        return
    
    # Update the FORCE_SUB_CHANNEL_2 variable
    os.environ["FORCE_SUB_CHANNEL_2"] = str(channel_id)
    await message.reply(f"✅ Successfully updated FORCE_SUB_CHANNEL_2 to {channel_id}")

# Handle the setforcesub3 command
@Client.on_message(filters.private & filters.user(OWNER_ID) & filters.command('setforcesub3'))
async def set_forcesub3(client: Client, message: Message):
    await message.reply("Please provide the channel ID for FORCE_SUB_CHANNEL_3 (numeric ID):")
    
    # Wait for the owner's response
    response = await client.ask(
        message.from_user.id,
        text="Please provide the channel ID (numeric ID):",
        filters=filters.text,
        timeout=60
    )

    try:
        channel_id = int(response.text)
    except ValueError:
        await message.reply("❌ Invalid input. Please provide a valid numeric channel ID.")
        return
    
    # Check if the bot can export the invite link in the channel
    can_invite, status_message = await can_export_invite_link(client, channel_id)
    
    if not can_invite:
        await message.reply(status_message)
        return
    
    # Update the FORCE_SUB_CHANNEL_3 variable
    os.environ["FORCE_SUB_CHANNEL_3"] = str(channel_id)
    await message.reply(f"✅ Successfully updated FORCE_SUB_CHANNEL_3 to {channel_id}")

# Handle the setforcesub4 command
@Client.on_message(filters.private & filters.user(OWNER_ID) & filters.command('setforcesub4'))
async def set_forcesub4(client: Client, message: Message):
    await message.reply("Please provide the channel ID for FORCE_SUB_CHANNEL_4 (numeric ID):")
    
    # Wait for the owner's response
    response = await client.ask(
        message.from_user.id,
        text="Please provide the channel ID (numeric ID):",
        filters=filters.text,
        timeout=60
    )

    try:
        channel_id = int(response.text)
    except ValueError:
        await message.reply("❌ Invalid input. Please provide a valid numeric channel ID.")
        return
    
    # Check if the bot can export the invite link in the channel
    can_invite, status_message = await can_export_invite_link(client, channel_id)
    
    if not can_invite:
        await message.reply(status_message)
        return
    
    # Update the FORCE_SUB_CHANNEL_4 variable
    os.environ["FORCE_SUB_CHANNEL_4"] = str(channel_id)
    await message.reply(f"✅ Successfully updated FORCE_SUB_CHANNEL_4 to {channel_id}")
