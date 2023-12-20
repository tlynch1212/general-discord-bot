from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
MINECRAFT_ADDRESS = os.getenv('MINECRAFT_ADDRESS')
MINECRAFT_BLOCK_IMAGE = 'https://static.wikia.nocookie.net/minecraft/images/f/fe/GrassNew.png/revision/latest/scale-to-width-down/340'
MINECRAFT_MESSAGE_ID = int(os.getenv('MINECRAFT_MESSAGE_ID'))
SERVER_STATUS_CHANNEL_ID = int(os.getenv('SERVER_STATUS_CHANNEL_ID'))
BOT_REPLIES_CHANNEL_ID = int(os.getenv('BOT_REPLIES_CHANNEL_ID'))
OWNER_USER_ID = int(os.getenv('OWNER_USER_ID'))
BLACKLIST = os.environ.get("BLACKLIST").split(',')