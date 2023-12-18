import random
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='$', description=description, intents=discord.Intents.all())

def getRandomResponse():
    listOfResponses = [
        'Whats that?',
        'bbw?',
        'Am I into that?',
        'Please, I need to know.'
    ]

    return random.choice(listOfResponses)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(name="repeat")
async def repeat(ctx, arg):
    await ctx.send(arg)

@bot.event
async def on_message(message):
    if str.lower(message.content) == 'bbw?':
        await message.channel.send(getRandomResponse())

bot.run(TOKEN)