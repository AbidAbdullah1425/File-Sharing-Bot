from pyrogram import Client, filters
from database.database import set_force_sub_channels, get_force_sub_channels
from bot import Bot

@Bot.on_message(filters.command("setfsub") & filters.user(ADMINS))
async def set_force_sub(client, message):
    try:
        # Extract channel IDs from the command
        channel_ids = [cid for cid in message.text.split()[1:] if cid.startswith("-100")]
        if channel_ids:
            # Update MongoDB with new channel IDs
            set_force_sub_channels(channel_ids)
            await message.reply_text("Force subscription channels updated successfully!")
    except Exception as e:
        print(f"Error: {str(e)}")  # Log the error silently

@app.on_message(filters.command("get_force_sub") & filters.user(ADMINS))
async def get_force_sub(client, message):
    try:
        # Fetch current force subscription channels from MongoDB
        channels = get_force_sub_channels()
        if channels:
            channel_list = "\n".join(channels)
            await message.reply_text(f"Current Force Sub Channels:\n{channel_list}")
        else:
            await message.reply_text("No Force Sub Channels have been set.")
    except Exception as e:
        print(f"Error: {str(e)}")  # Log the error silently
