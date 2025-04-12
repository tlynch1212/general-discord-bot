from dotenv import load_dotenv
import os

load_dotenv()

#discord stuff
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
BOT_TESTING_CHANNEL_ID = int(os.getenv('BOT_TESTING_CHANNEL_ID'))
GENERAL_CHANNEL_ID = int(os.getenv('GENERAL_CHANNEL_ID'))
OWNER_USER_ID = int(os.getenv('OWNER_USER_ID'))

#wos
WOS_API = os.getenv('WOS_API')