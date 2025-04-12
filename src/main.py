import discord
import library.globalvariables as globalvariables
import library.generalcommands as generalcommands
import library.chatbot as chatbot
import library.checkplayerinfo as checkplayerinfo

from discord.ext import commands, tasks

description = '''I am the bot for the Valhalla Discord. I am not very good though so dont get your hopes up.'''
bot = commands.Bot(command_prefix="/", description=description, intents=discord.Intents.all())

@bot.event
async def on_ready():
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
    if bot.user in message.mentions:
        await chatbot.talkToOdin(message)

@bot.command()
async def sync(ctx):
   await generalcommands.sync(ctx, bot)

@bot.tree.command(name="set-status", description='Sets my status to custom text')
async def set_status(ctx, text: str, activity: str):
    await generalcommands.setStatus(ctx, bot, text, activity)

@bot.tree.command(name="send_message_as_odin", description='Sends a custom message as the odin')
async def send_message_as_odin(ctx, text: str):
    await generalcommands.sendMessageAsOdin(ctx, bot, text)

@bot.tree.command(name="train-odin", description='Re-Trains me. It takes a couple days')
async def train_odin(ctx):
    chatbot.startTraining()
    check_train_thread.start()
    await ctx.response.send_message('Training has started.')

@bot.tree.command(name="add-response", description='adds a response for a certain input')
async def add_response(ctx, input: str, response: str):
    chatbot.addResponse(input, response)
    await ctx.response.send_message('Response Added.')

@bot.tree.command(name="check-player", description='checks player info in WOS')
async def check_player(ctx, playerid: str):
    await checkplayerinfo.get_player_data(playerid, ctx)

@tasks.loop(seconds=10.0)
async def check_train_thread():
    channel = bot.get_channel(globalvariables.BOT_TESTING_CHANNEL_ID)
    isDone = await chatbot.isTrainingDone(channel)
    if isDone:
        check_train_thread.cancel()

bot.run(globalvariables.TOKEN)