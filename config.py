#(©)CodeXBotz




import os
import logging
from logging.handlers import RotatingFileHandler



#Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "8108890822:AAGk9Lwfa2atQ2wvrfeZXfQ5STedcIHKa18")

#Your API ID from my.telegram.org
APP_ID = int(os.environ.get("APP_ID", "26254064"))

#Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "72541d6610ae7730e6135af9423b319c")

#Your db channel Id
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1002279496397"))

#OWNER ID
OWNER_ID = int(os.environ.get("OWNER_ID", "5296584067"))

#Port
PORT = os.environ.get("PORT", "8080")


#Database 
DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://teamprosperpay:AbidAbdullah199@cluster0.z93fita.mongodb.net/")
DB_NAME = os.environ.get("DATABASE_NAME", "ShanksStore")

#force sub channel id, if you want enable force sub

JOIN_REQUEST_ENABLE = os.environ.get("JOIN_REQUEST_ENABLED", None)

FORCE_SUB_CHANNEL_1 = int(os.environ.get("FORCE_SUB_CHANNEL_1", "-1002219567279"))
FORCE_SUB_CHANNEL_2 = int(os.environ.get("FORCE_SUB_CHANNEL_2", "-1002176591513"))
FORCE_SUB_CHANNEL_3 = int(os.environ.get("FORCE_SUB_CHANNEL_3", "-1002125561929"))
FORCE_SUB_CHANNEL_4 = int(os.environ.get("FORCE_SUB_CHANNEL_4", "-1002081959062"))

TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))

#start message
START_PIC = os.environ.get("START_PIC", "https://envs.sh/_BZ.jpg")
START_MSG = os.environ.get("START_MESSAGE", "Hello {first} Orewa ? Orewa Monkey D Bot, File Share neru Otoko Da!!!")
try:
    ADMINS=[]
    for x in (os.environ.get("ADMINS", "5296584067").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")

AUTO_DELETE_TIME = int(os.getenv("AUTO_DELETE_TIME", "600"))
AUTO_DELETE_MSG = os.environ.get("AUTO_DELETE_MSG", "File will be Deleted on 10 minutes.")
AUTO_DEL_SUCCESS_MSG = os.environ.get("AUTO_DEL_SUCCESS_MSG", "Osokatta na ? File Already Deleted Few Moments Ago.")


#Force sub message 
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "Huhh,You still haven't join my channels and trying to use me?Join them nowwww!then Try Again")

#set your Custom Caption here, Keep None for Disable Custom Caption
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)

#set True if you want to prevent users from forwarding files from bot
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False

#Set true if you want Disable your Channel Posts Share button
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'True'

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "❌Don't send me messages directly I'm only File Share bot!"

ADMINS.append(OWNER_ID)
ADMINS.append(5296584067)

LOG_FILE_NAME = "filesharingbot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
