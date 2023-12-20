import random
import library.globalvariables as globalvariables
import library.chatbot as chatbot

async def addResponse(ctx, text, bot):
    isBlacklisted = False
    for item in globalvariables.BLACKLIST:
        if str.lower(item) in str.lower(text):
            isBlacklisted = True
            await ctx.response.send_message(f'{text} is not allowed.')
            break
    if not isBlacklisted:
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


async def talkToGynch(message):
    if 'bbw?' in str.lower(message.content) or 'gynch' in str.lower(message.content):
        await message.channel.send(chatbot.gynchChat.get_response(str.lower(message.content).replace('gynch', '')))