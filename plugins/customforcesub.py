from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import FORCE_SUB_CHANNEL_1, FORCE_SUB_CHANNEL_2, FORCE_SUB_CHANNEL_3, FORCE_SUB_CHANNEL_4, OWNER

# Dictionary to store the ForceSub channels
force_sub_channels = {
    "FORCE_SUB_CHANNEL_1": FORCE_SUB_CHANNEL_1,
    "FORCE_SUB_CHANNEL_2": FORCE_SUB_CHANNEL_2,
    "FORCE_SUB_CHANNEL_3": FORCE_SUB_CHANNEL_3,
    "FORCE_SUB_CHANNEL_4": FORCE_SUB_CHANNEL_4,
}

# Command to display buttons for each ForceSub variable
async def setforcesub(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER:
        await update.message.reply_text("You do not have permission to use this command.")
        return

    keyboard = [
        [InlineKeyboardButton("FORCE_SUB_CHANNEL_1", callback_data="FORCE_SUB_CHANNEL_1")],
        [InlineKeyboardButton("FORCE_SUB_CHANNEL_2", callback_data="FORCE_SUB_CHANNEL_2")],
        [InlineKeyboardButton("FORCE_SUB_CHANNEL_3", callback_data="FORCE_SUB_CHANNEL_3")],
        [InlineKeyboardButton("FORCE_SUB_CHANNEL_4", callback_data="FORCE_SUB_CHANNEL_4")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select a ForceSub channel to change:", reply_markup=reply_markup)

# Handle button press and prompt for new value
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["selected_var"] = query.data
    await query.edit_message_text(f"Please send a new channel ID for {query.data}:")

# Handle text input and update the ForceSub variable
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    selected_var = context.user_data.get("selected_var")
    if selected_var:
        force_sub_channels[selected_var] = update.message.text
        await update.message.reply_text(f"{selected_var} has been updated to: {update.message.text}")
        context.user_data["selected_var"] = None
    else:
        await update.message.reply_text("Please use /setforcesub to select a channel first.")

# Command to check current ForceSub channels and bot permissions
async def checkforcesub(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER:
        await update.message.reply_text("You do not have permission to use this command.")
        return

    response = "Current ForceSub channels and bot access:\n"
    for name, channel_id in force_sub_channels.items():
        try:
            # Check if the bot can export an invite link
            chat = await context.bot.get_chat(channel_id)
            await chat.export_invite_link()
            response += f"{name}: {channel_id} ✅\n"
        except Exception:
            response += f"{name}: {channel_id} ❌\n"

    await update.message.reply_text(response)

# Set up handlers in the bot setup file (e.g., bot.py)
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, filters

# Add handlers in your main bot setup file
def register_handlers(application):
    application.add_handler(CommandHandler("setforcesub", setforcesub))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_handler(CommandHandler("checkforcesub", checkforcesub))
