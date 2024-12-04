from pyrogram import Client, filters
from database.database import set_force_sub_channels, get_force_sub_channels
from bot import Bot

@Bot.on_message(filters.command("setfsub") & filters.user(ADMINS))
async def set_force_sub(client, message):
    try:
        # Extract channel ID from the command
        args = message.text.split()
        if len(args) != 2 or not args[1].startswith("-100"):
            await message.reply_text("Please provide exactly one valid channel ID in the format: `/setfsub -100XXXXXXXXX`")
            return

        channel_id = args[1]
        # Update MongoDB with the new channel ID
        set_force_sub_channels([channel_id])  # Function assumes a list of IDs
        await message.reply_text(f"Force subscription channel set to {channel_id} successfully!")
    except Exception as e:
        print(f"Error: {str(e)}")  # Log the error silently


@Bot.on_message(filters.command("getfsub") & filters.user(ADMINS))
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
