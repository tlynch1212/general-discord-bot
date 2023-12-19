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
MINECRAFT_MESSAGE_ID = int(os.getenv('MINECRAFT_MESSAGE_ID'))
SERVER_STATUS_CHANNEL_ID = int(os.getenv('SERVER_STATUS_CHANNEL_ID'))
BOT_REPLIES_CHANNEL_ID = int(os.getenv('BOT_REPLIES_CHANNEL_ID'))
OWNER_USER_ID = int(os.getenv('OWNER_USER_ID'))

description = '''I am the bot for the EBDB Discord. I am not very good though so dont get your hopes up.'''
bot = commands.Bot(command_prefix="/", description=description, intents=discord.Intents.all())

async def getRandomResponse():
    channel = bot.get_channel(BOT_REPLIES_CHANNEL_ID)
    messages = [message async for message in channel.history(limit=200)]
    
    return random.choice(messages).content

async def update_minecraft_server_status(message):
    try:
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

        if online:
            description = 'Server is Live!'
        else:
            description = 'Server is Not Online'

        embed=discord.Embed(title="Server Status", description=description, color=0x109319)
        
        embed.set_author(name="Minecraft Server", icon_url=MINECRAFT_BLOCK_IMAGE)
        embed.set_thumbnail(url=MINECRAFT_BLOCK_IMAGE)
        
        # Get the time and add as footer
        now = datetime.now()
        current_time = now.strftime("%a %d %b %H:%M")
        embed.set_footer(text=f"Last Updated: {current_time}")
        
        embed.add_field(name="Name", value=name, inline=False)
        embed.add_field(name="Address", value=MINECRAFT_ADDRESS, inline=True)
        embed.add_field(name="Port", value=port, inline=True)
        embed.add_field(name="Players", value=f"{online_players}/{max_players}", inline=False)
        embed.add_field(name="Version", value=version, inline=True)
    except Exception as ex:
        embed=discord.Embed(title="Server Status", description='Error', color=0x109319)
        
        embed.set_author(name="Minecraft Server", icon_url=MINECRAFT_BLOCK_IMAGE)
        embed.set_thumbnail(url=MINECRAFT_BLOCK_IMAGE)
        
        # Get the time and add as footer
        now = datetime.now()
        current_time = now.strftime("%a %d %b %H:%M")
        embed.set_footer(text=f"Last Updated: {current_time}")

        embed.add_field(name="Uh Oh!", value='Damn, the api must be broken again.', inline=False)
        embed.add_field(name="Error", value=ex, inline=False)

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



@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if 'bbw?' in str.lower(message.content) or 'gynch' in str.lower(message.content):
        await message.channel.send(await getRandomResponse())

@bot.command()
async def sync(ctx):
    print("sync command")
    if ctx.author.id == OWNER_USER_ID:
        await bot.tree.sync()
        await ctx.send('Command tree synced.')
    else:
        await ctx.send('You must be the owner to use this command!')

@bot.tree.command(name="add-response", description='Adds the text you enter to the bot responses')
async def addResponse(ctx, text: str):
    responseText = text
    channel = bot.get_channel(BOT_REPLIES_CHANNEL_ID)
    messages = [message async for message in channel.history(limit=200)]
    foundMessage = ''
    for message in messages:
        if str.lower(message.content) == str.lower(responseText):
            foundMessage = message
            break

    if foundMessage == '':
        await channel.send(responseText)
        await ctx.response.send_message(f'Added {responseText} to my responses.')
    else:
        await ctx.response.send_message(f'{responseText} is already in my responses.')

@bot.tree.command(name="remove-response", description='Removes the text you enter from the bot responses')
async def removeResponse(ctx, text: str):
    responseText = text
    channel = bot.get_channel(BOT_REPLIES_CHANNEL_ID)
    messages = [message async for message in channel.history(limit=200)]
    foundMessage = ''
    for message in messages:
        if str.lower(message.content) == str.lower(responseText):
            foundMessage = message
            break

    if foundMessage != '':
        await foundMessage.delete()
        await ctx.response.send_message(f'Removed {foundMessage.content} from my responses.')
    else:
        await ctx.response.send_message(f'{responseText} is not in my responses.')


@tasks.loop(seconds=60.0)
async def update_minecraft_status():
    channel = bot.get_channel(SERVER_STATUS_CHANNEL_ID)
    message = await channel.fetch_message(MINECRAFT_MESSAGE_ID)

    await update_minecraft_server_status(message)

bot.run(TOKEN)