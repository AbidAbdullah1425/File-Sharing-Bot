import os
from pyrogram import filters
from pyrogram.types import Message
from bot import Bot  # Import Bot class
from config import OWNER_ID, ADMINS

# Function to check if the bot has permission to export an invite link
async def can_export_invite_link(client, channel_id):
    try:
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


# Handle the /setforcesub1 command
@Bot.on_message(filters.private & filters.user(OWNER_ID) & filters.command('setforcesub1'))
async def set_forcesub1(client: Bot, message: Message):
    # Parse the channel ID from the command
    try:
        command_args = message.text.split()
        if len(command_args) != 2:
            await message.reply("❌ Please provide the channel ID. Example: /setforcesub1 -1002176591513")
            return

        channel_id = int(command_args[1])  # Convert channel ID to an integer
    except ValueError:
        await message.reply("❌ Invalid input. Please provide a valid numeric channel ID.")
        return

    # Check if the bot has permission to generate the invite link
    can_invite, status_message = await can_export_invite_link(client, channel_id)

    if not can_invite:
        await message.reply(status_message)
        return

    # Update the FORCE_SUB_CHANNEL_1 variable
    os.environ["FORCE_SUB_CHANNEL_1"] = str(channel_id)
    await message.reply(f"✅ Successfully updated FORCE_SUB_CHANNEL_1 to {channel_id}")


# Handle the /setforcesub2 command
@Bot.on_message(filters.private & filters.user(OWNER_ID) & filters.command('setforcesub2'))
async def set_forcesub2(client: Bot, message: Message):
    # Parse the channel ID from the command
    try:
        command_args = message.text.split()
        if len(command_args) != 2:
            await message.reply("❌ Please provide the channel ID. Example: /setforcesub2 -1002176591513")
            return

        channel_id = int(command_args[1])  # Convert channel ID to an integer
    except ValueError:
        await message.reply("❌ Invalid input. Please provide a valid numeric channel ID.")
        return

    # Check if the bot has permission to generate the invite link
    can_invite, status_message = await can_export_invite_link(client, channel_id)

    if not can_invite:
        await message.reply(status_message)
        return

    # Update the FORCE_SUB_CHANNEL_2 variable
    os.environ["FORCE_SUB_CHANNEL_2"] = str(channel_id)
    await message.reply(f"✅ Successfully updated FORCE_SUB_CHANNEL_2 to {channel_id}")


# Handle the /setforcesub3 command
@Bot.on_message(filters.private & filters.user(OWNER_ID) & filters.command('setforcesub3'))
async def set_forcesub3(client: Bot, message: Message):
    # Parse the channel ID from the command
    try:
        command_args = message.text.split()
        if len(command_args) != 2:
            await message.reply("❌ Please provide the channel ID. Example: /setforcesub3 -1002176591513")
            return

        channel_id = int(command_args[1])  # Convert channel ID to an integer
    except ValueError:
        await message.reply("❌ Invalid input. Please provide a valid numeric channel ID.")
        return

    # Check if the bot has permission to generate the invite link
    can_invite, status_message = await can_export_invite_link(client, channel_id)

    if not can_invite:
        await message.reply(status_message)
        return

    # Update the FORCE_SUB_CHANNEL_3 variable
    os.environ["FORCE_SUB_CHANNEL_3"] = str(channel_id)
    await message.reply(f"✅ Successfully updated FORCE_SUB_CHANNEL_3 to {channel_id}")


# Handle the /setforcesub4 command
@Bot.on_message(filters.private & filters.user(OWNER_ID) & filters.command('setforcesub4'))
async def set_forcesub4(client: Bot, message: Message):
    # Parse the channel ID from the command
    try:
        command_args = message.text.split()
        if len(command_args) != 2:
            await message.reply("❌ Please provide the channel ID. Example: /setforcesub4 -1002176591513")
            return

        channel_id = int(command_args[1])  # Convert channel ID to an integer
    except ValueError:
        await message.reply("❌ Invalid input. Please provide a valid numeric channel ID.")
        return

    # Check if the bot has permission to generate the invite link
    can_invite, status_message = await can_export_invite_link(client, channel_id)

    if not can_invite:
        await message.reply(status_message)
        return

    # Update the FORCE_SUB_CHANNEL_4 variable
    os.environ["FORCE_SUB_CHANNEL_4"] = str(channel_id)
    await message.reply(f"✅ Successfully updated FORCE_SUB_CHANNEL_4 to {channel_id}")
