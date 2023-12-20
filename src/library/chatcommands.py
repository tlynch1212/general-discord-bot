import random
import globalvariables

async def addResponse(ctx, text, bot):
    responseText = text
    channel = bot.get_channel(globalvariables.BOT_REPLIES_CHANNEL_ID)
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

async def removeResponse(ctx, text, bot):
    responseText = text
    channel = bot.get_channel(globalvariables.BOT_REPLIES_CHANNEL_ID)
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

async def getRandomResponse(bot):
    channel = bot.get_channel(globalvariables.BOT_REPLIES_CHANNEL_ID)
    messages = [message async for message in channel.history(limit=200)]
    
    return random.choice(messages).content

async def checkIfAndSendRandomResponse(message, bot):
    if 'bbw?' in str.lower(message.content) or 'gynch' in str.lower(message.content):
        await message.channel.send(await getRandomResponse(bot))