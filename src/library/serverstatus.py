import json
import discord
from urllib.request import Request, urlopen
from datetime import datetime
import library.globalvariables as globalvariables

async def update_minecraft_server_status(message):
    try:
        request = Request(
            url=f"https://api.mcsrvstat.us/bedrock/3/{globalvariables.MINECRAFT_ADDRESS}", 
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
        
        embed.set_author(name="Minecraft Server", icon_url=globalvariables.MINECRAFT_BLOCK_IMAGE)
        embed.set_thumbnail(url=globalvariables.MINECRAFT_BLOCK_IMAGE)
        
        # Get the time and add as footer
        now = datetime.now()
        current_time = now.strftime("%a %d %b %H:%M")
        embed.set_footer(text=f"Last Updated: {current_time}")
        
        embed.add_field(name="Name", value=name, inline=False)
        embed.add_field(name="Address", value=globalvariables.MINECRAFT_ADDRESS, inline=True)
        embed.add_field(name="Port", value=port, inline=True)
        embed.add_field(name="Players", value=f"{online_players}/{max_players}", inline=False)
        embed.add_field(name="Version", value=version, inline=True)
    except Exception as ex:
        embed=discord.Embed(title="Server Status", description='Error', color=0x109319)
        
        embed.set_author(name="Minecraft Server", icon_url=globalvariables.MINECRAFT_BLOCK_IMAGE)
        embed.set_thumbnail(url=globalvariables.MINECRAFT_BLOCK_IMAGE)
        
        # Get the time and add as footer
        now = datetime.now()
        current_time = now.strftime("%a %d %b %H:%M")
        embed.set_footer(text=f"Last Updated: {current_time}")

        embed.add_field(name="Uh Oh!", value='Damn, the api must be broken again.', inline=False)
        embed.add_field(name="Error", value=ex, inline=False)

    # Send the embed to the discord channel
    await message.edit(embed=embed)