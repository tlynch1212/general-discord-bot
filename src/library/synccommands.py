import globalvariables

async def sync(ctx, bot):
    print("sync command")
    if ctx.author.id == globalvariables.OWNER_USER_ID:
        await bot.tree.sync()
        await ctx.send('Command tree synced.')
    else:
        await ctx.send('You must be the owner to use this command!')