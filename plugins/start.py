import os
import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from config import ADMINS, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT, START_PIC, AUTO_DELETE_TIME, AUTO_DELETE_MSG, JOIN_REQUEST_ENABLE
from helper_func import subscribed, decode, get_messages, delete_file
from database.database import add_user, del_user, full_userbase, present_user
from plugins.FORCESUB import f_invitelink

# Setting up the logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    logger.info("Received /start command")
    id = message.from_user.id
    if not await present_user(id):
        try:
            await add_user(id)
            logger.info(f"Added new user with ID {id}")
        except Exception as e:
            logger.error(f"Error adding user with ID {id}: {e}")
    
    text = message.text
    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1]
        except IndexError:
            logger.warning("Base64 string extraction failed")
            return
        
        string = await decode(base64_string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except Exception as e:
                logger.error(f"Error parsing start and end IDs: {e}")
                return
            if start <= end:
                ids = range(start, end + 1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except Exception as e:
                logger.error(f"Error parsing single ID: {e}")
                return

        temp_msg = await message.reply("Please wait...")
        try:
            messages = await get_messages(client, ids)
            logger.info("Messages fetched successfully")
        except Exception as e:
            logger.error(f"Error fetching messages: {e}")
            await message.reply_text("Something went wrong..!")
            return
        await temp_msg.delete()

        track_msgs = []

        for msg in messages:
            if bool(CUSTOM_CAPTION) and bool(msg.document):
                caption = CUSTOM_CAPTION.format(previouscaption="" if not msg.caption else msg.caption.html, filename=msg.document.file_name)
            else:
                caption = "" if not msg.caption else msg.caption.html

            if DISABLE_CHANNEL_BUTTON:
                reply_markup = msg.reply_markup
            else:
                reply_markup = None

            if AUTO_DELETE_TIME and AUTO_DELETE_TIME > 0:
                try:
                    copied_msg_for_deletion = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                    if copied_msg_for_deletion:
                        track_msgs.append(copied_msg_for_deletion)
                    else:
                        logger.warning("Failed to copy message, skipping.")
                except FloodWait as e:
                    logger.info(f"Flood wait triggered: {e.value} seconds")
                    await asyncio.sleep(e.value)
                    copied_msg_for_deletion = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                    if copied_msg_for_deletion:
                        track_msgs.append(copied_msg_for_deletion)
                    else:
                        logger.warning("Failed to copy message after retry, skipping.")
                except Exception as e:
                    logger.error(f"Error copying message: {e}")
                    pass
            else:
                try:
                    await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                    await asyncio.sleep(0.5)
                except FloodWait as e:
                    logger.info(f"Flood wait triggered: {e.value} seconds")
                    await asyncio.sleep(e.value)
                    await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                except Exception as e:
                    logger.error(f"Error copying message: {e}")
                    pass

        if track_msgs:
            delete_data = await client.send_message(
                chat_id=message.from_user.id,
                text=AUTO_DELETE_MSG.format(time=AUTO_DELETE_TIME)
            )
            logger.info("Scheduling deletion of messages")
            asyncio.create_task(delete_file(track_msgs, client, delete_data))
        else:
            logger.info("No messages to track for deletion.")
        return
    else:
        logger.info("Sending start message")
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("😊 About Me", callback_data="about"),
                    InlineKeyboardButton("🔒 Close", callback_data="close")
                ]
            ]
        )
        if START_PIC:
            await message.reply_photo(
                photo=START_PIC,
                caption=START_MSG.format(
                    first=message.from_user.first_name,
                    last=message.from_user.last_name,
                    username=None if not message.from_user.username else '@' + message.from_user.username,
                    mention=message.from_user.mention,
                    id=message.from_user.id
                ),
                reply_markup=reply_markup,
                quote=True
            )
        else:
            await message.reply_text(
                text=START_MSG.format(
                    first=message.from_user.first_name,
                    last=message.from_user.last_name,
                    username=None if not message.from_user.username else '@' + message.from_user.username,
                    mention=message.from_user.mention,
                    id=message.from_user.id
                ),
                reply_markup=reply_markup,
                disable_web_page_preview=True,
                quote=True
            )
        return

# Other command handlers and functions would similarly be updated with logger calls as needed.


    
#=====================================================================================##

WAIT_MSG = """"<b>Processing ...</b>"""

REPLY_ERROR = """<code>Use this command as a replay to any telegram message with out any spaces.</code>"""

#=====================================================================================##


@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    try:
        # Log that the function was triggered
        logger.info(f"Received /start command from {message.from_user.id} ({message.from_user.first_name})")

        buttons = [
            [
                InlineKeyboardButton(text="Join Channel", url=f_invitelink if 'f_invitelink' in globals() else client.invitelink),
                InlineKeyboardButton(text="Join Channel", url=client.invitelink2),
            ],
            [
                InlineKeyboardButton(text="Join Channel", url=client.invitelink3),
                InlineKeyboardButton(text="Join Channel", url=client.invitelink4),
            ]
        ]

        try:
            command_argument = message.command[1]
            buttons.append(
                [
                    InlineKeyboardButton(
                        text='Try Again',
                        url=f"https://t.me/{client.username}?start={command_argument}"
                    )
                ]
            )
        except IndexError:
            logger.warning("No command argument found for 'Try Again' button")

        # Log that the reply is being sent
        logger.info(f"Sending reply to {message.from_user.id}")

        await message.reply(
            text=FORCE_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
            quote=True,
            disable_web_page_preview=True
        )

        # Log after sending the reply
        logger.info(f"Reply sent successfully to {message.from_user.id}")

    except Exception as e:
        # Log any exceptions that occur
        logger.error(f"An error occurred while handling /start command from {message.from_user.id}: {e}")


@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
        
        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()

