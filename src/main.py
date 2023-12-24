import discord
import library.serverstatus as serverstatus
import library.globalvariables as globalvariables
import library.generalcommands as generalcommands
import library.chatbot as chatbot

from discord.ext import commands, tasks

description = '''I am the bot for the EBDB Discord. I am not very good though so dont get your hopes up.'''
bot = commands.Bot(command_prefix="/", description=description, intents=discord.Intents.all())

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
    if message.author == bot.user:
        return

    await bot.process_commands(message)
    await chatbot.talkToGynch(message)

@bot.command()
async def sync(ctx):
   await generalcommands.sync(ctx, bot)

@bot.tree.command(name="setStatus", description='Sets my status to custom text')
async def setStatus(ctx, text: str, activity: str):
    await generalcommands.setStatus(ctx, bot, text, activity)


@tasks.loop(seconds=60.0)
async def update_minecraft_status():
    channel = bot.get_channel(globalvariables.SERVER_STATUS_CHANNEL_ID)
    message = await channel.fetch_message(globalvariables.MINECRAFT_MESSAGE_ID)

    await serverstatus.update_minecraft_server_status(message)

bot.run(globalvariables.TOKEN)