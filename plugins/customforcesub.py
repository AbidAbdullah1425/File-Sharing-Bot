from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import FORCE_SUB_CHANNEL_1, FORCE_SUB_CHANNEL_2, FORCE_SUB_CHANNEL_3, FORCE_SUB_CHANNEL_4, OWNER_ID

# Dictionary to store ForceSub channel IDs (mutable for dynamic updates)
force_sub_channels = {
    "FORCE_SUB_CHANNEL_1": FORCE_SUB_CHANNEL_1,
    "FORCE_SUB_CHANNEL_2": FORCE_SUB_CHANNEL_2,
    "FORCE_SUB_CHANNEL_3": FORCE_SUB_CHANNEL_3,
    "FORCE_SUB_CHANNEL_4": FORCE_SUB_CHANNEL_4,
}

# Command to display buttons for each ForceSub variable
@Client.on_message(filters.command("setforcesub") & filters.user(OWNER_ID))
async def setforcesub(client, message):
    keyboard = [
        [InlineKeyboardButton("FORCE_SUB_CHANNEL_1", callback_data="FORCE_SUB_CHANNEL_1")],
        [InlineKeyboardButton("FORCE_SUB_CHANNEL_2", callback_data="FORCE_SUB_CHANNEL_2")],
        [InlineKeyboardButton("FORCE_SUB_CHANNEL_3", callback_data="FORCE_SUB_CHANNEL_3")],
        [InlineKeyboardButton("FORCE_SUB_CHANNEL_4", callback_data="FORCE_SUB_CHANNEL_4")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await message.reply_text("Select a ForceSub channel to change:", reply_markup=reply_markup)

# Handle button press and prompt for new value
@Client.on_callback_query()
async def button_callback(client, callback_query):
    selected_var = callback_query.data
    callback_query.from_user_data["selected_var"] = selected_var
    await callback_query.message.edit_text(f"Please send a new channel ID for {selected_var}:")

# Handle text input and update the ForceSub variable
@Client.on_message(filters.text & filters.user(OWNER_ID))
async def handle_text(client, message):
    selected_var = message.from_user_data.get("selected_var")
    if selected_var:
        # Update the selected ForceSub variable with the new channel ID
        force_sub_channels[selected_var] = message.text
        await message.reply_text(f"{selected_var} has been updated to: {message.text}")
        message.from_user_data["selected_var"] = None  # Clear selected variable
    else:
        await message.reply_text("Please use /setforcesub to select a channel first.")

# Command to check current ForceSub channels and bot permissions
@Client.on_message(filters.command("checkforcesub") & filters.user(OWNER_ID))
async def checkforcesub(client, message):
    response = "Current ForceSub channels and bot access:\n"
    for name, channel_id in force_sub_channels.items():
        try:
            chat = await client.get_chat(channel_id)
            invite_link = await client.export_chat_invite_link(channel_id)
            response += f"{name}: {channel_id} ✅\n"
        except Exception:
            response += f"{name}: {channel_id} ❌ (Bot lacks permissions or invalid channel)\n"

    await message.reply_text(response)
