from pyrogram import Client, filters
from database.database import set_force_sub_channel, get_force_sub_channel
from bot import Bot
from config import ADMINS

f_invitelink = None

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
        set_force_sub_channel(channel_id)

        # Export invite link of the new force subscription channel
        try:
            link = (await client.get_chat(channel_id)).invite_link
            if not link:
                await client.export_chat_invite_link(channel_id)
                link = (await client.get_chat(channel_id)).invite_link
            # Store the invite link to a variable (f_invitelink)
            f_invitelink = link
            await message.reply_text(f"Force subscription channel set to {channel_id} successfully!\nInvite link: {f_invitelink}")
        except Exception as a:
            print(f"Error: {a}\nBot can't export invite link from the force subscription channel!\nPlease check the channel ID value and ensure the bot is an admin in the channel with 'Invite Users via Link' permission. Current channel ID: {channel_id}")

    except Exception as e:
        print(f"Error: {str(e)}")  # Log the error silently



@Bot.on_message(filters.command("getfsub") & filters.user(ADMINS))
async def get_force_sub(client, message):
    try:
        # Fetch the current force subscription channel from MongoDB
        channel_id = get_force_sub_channel()
        if channel_id:
            await message.reply_text(f"Current Force Sub Channel ID: {channel_id}")
        else:
            await message.reply_text("No Force Sub Channel has been set.")
    except Exception as e:
        print(f"Error: {str(e)}")  # Log the error silently
