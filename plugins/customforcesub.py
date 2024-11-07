from bot import Bot  # Import Bot from bot.py
from pyrogram import filters
from pyrogram.types import Message
from config import FORCE_SUB_CHANNEL_1, FORCE_SUB_CHANNEL_2, FORCE_SUB_CHANNEL_3, FORCE_SUB_CHANNEL_4

@Bot.on_message(filters.private & filters.user(OWNER_ID) & filters.command('setforcesub1'))
async def set_forcesub1(client: Bot, message: Message):
    # Extract channel ID from the message
    channel_id = message.text.split(' ', 1)[1]

    # Update the corresponding FORCE_SUB_CHANNEL variable
    global FORCE_SUB_CHANNEL_1  # This ensures the variable is updated globally
    FORCE_SUB_CHANNEL_1 = channel_id

    # Send confirmation message to owner
    await message.reply(f"Force Sub-Channel 1 has been updated to: {FORCE_SUB_CHANNEL_1}")

@Bot.on_message(filters.private & filters.user(OWNER_ID) & filters.command('setforcesub2'))
async def set_forcesub2(client: Bot, message: Message):
    # Extract channel ID from the message
    channel_id = message.text.split(' ', 1)[1]

    # Update the corresponding FORCE_SUB_CHANNEL variable
    global FORCE_SUB_CHANNEL_2
    FORCE_SUB_CHANNEL_2 = channel_id

    # Send confirmation message to owner
    await message.reply(f"Force Sub-Channel 2 has been updated to: {FORCE_SUB_CHANNEL_2}")

@Bot.on_message(filters.private & filters.user(OWNER_ID) & filters.command('setforcesub3'))
async def set_forcesub3(client: Bot, message: Message):
    # Extract channel ID from the message
    channel_id = message.text.split(' ', 1)[1]

    # Update the corresponding FORCE_SUB_CHANNEL variable
    global FORCE_SUB_CHANNEL_3
    FORCE_SUB_CHANNEL_3 = channel_id

    # Send confirmation message to owner
    await message.reply(f"Force Sub-Channel 3 has been updated to: {FORCE_SUB_CHANNEL_3}")

@Bot.on_message(filters.private & filters.user(OWNER_ID) & filters.command('setforcesub4'))
async def set_forcesub4(client: Bot, message: Message):
    # Extract channel ID from the message
    channel_id = message.text.split(' ', 1)[1]

    # Update the corresponding FORCE_SUB_CHANNEL variable
    global FORCE_SUB_CHANNEL_4
    FORCE_SUB_CHANNEL_4 = channel_id

    # Send confirmation message to owner
    await message.reply(f"Force Sub-Channel 4 has been updated to: {FORCE_SUB_CHANNEL_4}")
