import os
from pyrogram import Client, filters
from pyrogram.types import Message
from config import OWNER_ID  # Ensure OWNER_ID is imported from your config.py

# Function to check if the bot is an admin in the given private channel using its channel ID
async def check_if_bot_is_admin(client: Client, channel_id: int):
    try:
        # Check if the bot is an admin in the channel by channel ID
        chat_member = await client.get_chat_member(channel_id, "me")
        if chat_member.status in ['administrator', 'creator']:
            return True, f"✅ Bot is an admin in the channel with ID {channel_id}."
        else:
            return False, f"❌ Bot is NOT an admin in the channel with ID {channel_id}."
    except Exception as e:
        return False, f"❌ Error checking admin status: {e}"

# Command to set force subscription variables
@Client.on_message(filters.private & filters.user(OWNER_ID) & filters.command('setforcesub'))
async def set_forcesub(client: Client, message: Message):
    # Step 1: Ask the owner for the private channel ID (instead of the URL)
    await message.reply("Please provide the private channel ID (numeric ID):")
    
    # Step 2: Wait for owner's response (the private channel ID)
    new_value = await client.ask(
        message.from_user.id,
        text="Please provide the private channel ID:",
        filters=filters.text,
        timeout=60
    )

    try:
        # Convert the provided input to an integer (the channel ID)
        channel_id = int(new_value.text)
    except ValueError:
        await message.reply("❌ Invalid input. Please provide a valid numeric channel ID.")
        return

    # Step 3: Check if the bot is an admin in the provided channel ID
    is_admin, admin_status_message = await check_if_bot_is_admin(client, channel_id)
    
    # Step 4: If the bot is not an admin, inform the owner and stop
    if not is_admin:
        await message.reply(admin_status_message)
        return
    
    # Step 5: If the bot is an admin, allow the owner to select which `FORCE_SUB_CHANNEL` to modify
    await message.reply(admin_status_message + "\n\nPlease choose which `FORCE_SUB_CHANNEL` to modify:\n1. FORCE_SUB_CHANNEL_1\n2. FORCE_SUB_CHANNEL_2\n3. FORCE_SUB_CHANNEL_3\n4. FORCE_SUB_CHANNEL_4")
    
    # Step 6: Wait for owner's selection (1, 2, 3, or 4)
    response = await client.ask(
        message.from_user.id,
        text="Please reply with the number of the channel (1, 2, 3, or 4):",
        filters=filters.text,
        timeout=60
    )
    
    # Step 7: Validate the selection
    if response.text not in ['1', '2', '3', '4']:
        await response.reply("❌ Invalid selection. Please choose between 1, 2, 3, or 4.")
        return
    
    # Step 8: Define the variable name based on the selected option (FORCE_SUB_CHANNEL_1 to FORCE_SUB_CHANNEL_4)
    variable_name = f"FORCE_SUB_CHANNEL_{response.text}"
    
    # Step 9: Update the value of the selected FORCE_SUB_CHANNEL_* in memory
    os.environ[variable_name] = str(channel_id)
    
    # Step 10: Confirm the update
    await message.reply(f"✅ Successfully updated {variable_name} to: {channel_id}")
