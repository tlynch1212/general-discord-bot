from dotenv import load_dotenv
import os

load_dotenv()

#discord stuff
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
SERVER_STATUS_CHANNEL_ID = int(os.getenv('SERVER_STATUS_CHANNEL_ID'))
BOT_REPLIES_CHANNEL_ID = int(os.getenv('BOT_REPLIES_CHANNEL_ID'))
OWNER_USER_ID = int(os.getenv('OWNER_USER_ID'))
BLACKLIST = os.environ.get("BLACKLIST").split(',')

GTA_MESSAGE_ID = int(os.getenv('GTA_MESSAGE_ID'))
MINECRAFT_MESSAGE_ID = int(os.getenv('MINECRAFT_MESSAGE_ID'))
BEAM_MESSAGE_ID = int(os.getenv('BEAM_MESSAGE_ID'))

#gta
GTA_LOGO = 'https://i.imgur.com/tFQPJJ9.png'

#minecraft
MINECRAFT_BLOCK_IMAGE = 'https://static.wikia.nocookie.net/minecraft/images/f/fe/GrassNew.png/revision/latest/scale-to-width-down/340'

#pterodactyl
PUBLIC_ADDRESS = os.getenv('PUBLIC_ADDRESS')
PTERODACTYL_ADDRESS = os.getenv('PTERODACTYL_ADDRESS')
PTERODACTYL_TOKEN = os.getenv('PTERODACTYL_TOKEN')

#beam
BEAM_SERVER_ID = os.getenv('BEAM_SERVER_ID')
BEAM_LOGO = os.getenv('BEAM_LOGO')