from pyrogram import Client, filters
from pyrogram.types import Message  # Add this import to fix the error
from config import OWNER_ID, FORCE_SUB_CHANNEL_1, FORCE_SUB_CHANNEL_2, FORCE_SUB_CHANNEL_3, FORCE_SUB_CHANNEL_4
@Client.on_message(filters.private & filters.user(OWNER_ID) & filters.command('checkforcesub'))
async def checkforcesub(client: Client, message: Message):
    # Prepare the message with the values of the force sub-channel variables
    force_sub_channels = (
        f"Force Sub-Channel 1: {FORCE_SUB_CHANNEL_1}\n"
        f"Force Sub-Channel 2: {FORCE_SUB_CHANNEL_2}\n"
        f"Force Sub-Channel 3: {FORCE_SUB_CHANNEL_3}\n"
        f"Force Sub-Channel 4: {FORCE_SUB_CHANNEL_4}"
    )
    
    # Send the message to the owner
    await message.reply(force_sub_channels)