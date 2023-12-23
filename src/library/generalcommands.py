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
    if ctx.author.id == globalvariables.OWNER_USER_ID:
        if activity == "game":
            await bot.change_presence(activity=discord.Game(name=text))
        elif activity == "listen":
            await bot.change_presence(activity=discord.ActivityType.listening, name=text)
        elif activity == "watching":
            await bot.change_presence(activity=discord.ActivityType.watching, name=text)
        else:
            await ctx.send('Invalid activity type.')
    else:
        await ctx.send('You must be the owner to use this command!')
