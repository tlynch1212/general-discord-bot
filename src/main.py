import random
import time
import discord
import os
import json

from urllib.request import Request, urlopen
from datetime import datetime
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
MINECRAFT_ADDRESS = os.getenv('MINECRAFT_ADDRESS')
MINECRAFT_BLOCK_IMAGE = 'https://static.wikia.nocookie.net/minecraft/images/f/fe/GrassNew.png/revision/latest/scale-to-width-down/340'
MINECRAFT_MESSAGE_ID = 1186396044628594778
SERVER_STATUS_CHANNEL_ID = 1183495317656698990

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='$', description=description, intents=discord.Intents.all())

def getRandomResponse():
    listOfResponses = [
        'Whats that?',
        'bbw?',
        'Am I into that?',
        'Please, I need to know.',
        'Bath & Body Works'
    ]

    return random.choice(listOfResponses)

async def update_minecraft_server_status(message):
    # Get details of the mc server
    request = Request(
        url=f"https://api.mcsrvstat.us/bedrock/3/{MINECRAFT_ADDRESS}", 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    response = urlopen(request)
    data = json.load(response)
    
    online = data['online']
    port = data['port']
    name = data['motd']['clean'][0].strip()
    version = data['version']
    online_players = data['players']['online']
    max_players = data['players']['max']

    # Try to get the details of the server
    if online:
        description = 'Server is Live!'
    else:
        description = 'Server is Not Online'

    # Create the initial embed object
    embed=discord.Embed(title="Server Status", description=description, color=0x109319)

    # Add author, thumbnail, fields, and footer to the embed
    embed.set_author(name="Minecraft Server", icon_url=MINECRAFT_BLOCK_IMAGE)

    embed.set_thumbnail(url=MINECRAFT_BLOCK_IMAGE)
    
    # Add the fields
    embed.add_field(name="Name", value=name, inline=False)
    embed.add_field(name="Address", value=MINECRAFT_ADDRESS, inline=True)
    embed.add_field(name="Port", value=port, inline=True)
    embed.add_field(name="Players", value=f"{online_players}/{max_players}", inline=False)
    embed.add_field(name="Version", value=version, inline=True)

    # Get the time and add as footer
    now = datetime.now()
    current_time = now.strftime("%a %d %b %H:%M")
    embed.set_footer(text=f"Last Updated: {current_time}")
    
    # Send the embed to the discord channel
    await message.edit(embed=embed)


@bot.event
async def on_ready():
    update_minecraft_status.start()
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    print("Bot is ready!")


@bot.command(name="repeat")
async def repeat(ctx, arg):
    await ctx.send(arg)

@bot.event
async def on_message(message):
    if str.lower(message.content) == 'bbw?':
        await message.channel.send(getRandomResponse())

@tasks.loop(seconds=60.0)
async def update_minecraft_status():
    channel = bot.get_channel(SERVER_STATUS_CHANNEL_ID)
    message = await channel.fetch_message(MINECRAFT_MESSAGE_ID)
    await update_minecraft_server_status(message)

bot.run(TOKEN)