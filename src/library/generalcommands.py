import library.globalvariables as globalvariables
import discord

async def sync(ctx, bot):
    print("sync command")
    if ctx.author.id == globalvariables.OWNER_USER_ID:
        await bot.tree.sync()
        await ctx.send('Command tree synced.')
    else:
        await ctx.send('You must be the owner to use this command!')

async def setStatus(ctx, bot, text, activity):
    print("setStatus command")
    activityType = '0'
    if ctx.user.id == globalvariables.OWNER_USER_ID:
        if activity == "playing":
            activityType = discord.Game(name=text)
        elif activity == "listening":
            activityType = discord.Activity(type=discord.ActivityType.listening, name=text)
        elif activity == "watching":
            activityType = discord.Activity(type=discord.ActivityType.watching, name=text)
        else:
            await ctx.response.send_message('Invalid activity type.')
        if activityType != '0':
            await bot.change_presence(activity=activityType)
            await ctx.response.send_message('Status set.')
    else:
        await ctx.response.send_message('You must be the owner to use this command!')


async def sendMessageAsGynch(ctx, bot, text):
    print("sendMessageAsGynch command")
    if ctx.user.id == globalvariables.OWNER_USER_ID:
        channel = bot.get_channel(globalvariables.BOT_TESTING_CHANNEL_ID)
        await channel.send(text)
        await ctx.response.send_message('message sent to general chat.')
    else:
        await ctx.response.send_message('You must be the owner to use this command!')
