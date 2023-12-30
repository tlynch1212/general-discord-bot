import json
import discord
from urllib.request import Request, urlopen
from datetime import datetime
import library.globalvariables as globalvariables
from pydactyl import PterodactylClient

api = PterodactylClient(globalvariables.PTERODACTYL_ADDRESS, globalvariables.PTERODACTYL_TOKEN)

onlineString = '🟢 Online'
offlineString = '🔴 Offline'

async def update_minecraft_server_status(message):
    try:
        data = fetchData(f"https://api.mcsrvstat.us/bedrock/3/{globalvariables.PUBLIC_ADDRESS}")
         
        online = data['online']
        port = data['port']
        name = data['motd']['clean'][0].strip() 
        version = data['version']
        online_players = data['players']['online']
        max_players = data['players']['max']

        if online:
            onlineStatus = onlineString
        else:
            onlineStatus = offlineString

        embed = createDefaultEmbed(onlineStatus, 'Minecraft Server', globalvariables.MINECRAFT_BLOCK_IMAGE)
        setFooter(embed)
        
        embed.add_field(name="Name", value=name, inline=False)
        embed.add_field(name="Address", value=globalvariables.PUBLIC_ADDRESS, inline=True)
        embed.add_field(name="Port", value=port, inline=True)
        embed.add_field(name="Players", value=f"{online_players}/{max_players}", inline=False)
        embed.add_field(name="Version", value=version, inline=True)
    except Exception as ex:
        embed = createDefaultEmbed(offlineString, 'Minecraft Server', globalvariables.MINECRAFT_BLOCK_IMAGE)
        setFooter(embed)

        embed.add_field(name="Uh Oh!", value='Damn, the api must be broken again.', inline=False)
        embed.add_field(name="Error", value=ex, inline=False)

    # Send the embed to the discord channel
    await message.edit(embed=embed)


async def update_gta_server_status(message):
    await update_rockstar_game_server_status(message, 30120, 'GTA 5', globalvariables.GTA_LOGO, True)

async def update_rdr_server_status(message):
    await update_rockstar_game_server_status(message, 30500, 'RDR 2',  globalvariables.RDR_LOGO, False)

async def update_rockstar_game_server_status(message, port, serverName, logo, addConnect):
    try:
        data = fetchData(f"http://{globalvariables.PUBLIC_ADDRESS}:{port}/info.json")
        players = fetchData(f"http://{globalvariables.PUBLIC_ADDRESS}:{port}/players.json")

        name = data['vars']['sv_projectName']
        online_players = len(players)
        max_players = data['vars']['sv_maxClients']

        if data:
            onlineStatus = onlineString
        else:
            onlineStatus = offlineString

        embed = createDefaultEmbed(onlineStatus, f'{serverName} Server', logo)
        setFooter(embed)
        
        embed.add_field(name="Name", value=name, inline=False)
        embed.add_field(name="Address", value=globalvariables.PUBLIC_ADDRESS, inline=True)
        embed.add_field(name="Port", value=port, inline=True)
        embed.add_field(name="Players", value=f"{online_players}/{max_players}", inline=False)
        embed.add_field(name="F8 Connect", value=f'connect {globalvariables.PUBLIC_ADDRESS}', inline=False)
    except Exception as ex:
        embed = createDefaultEmbed(offlineString, f'{serverName} Server', logo)
        setFooter(embed)

        embed.add_field(name="Uh Oh!", value='Damn, the api must be broken again.', inline=False)
        embed.add_field(name="Error", value=ex, inline=False)

    # Send the embed to the discord channel
    if addConnect == True:
        await message.edit(embed=embed, view=ButtonView(port))
    else:
        await message.edit(embed=embed, view=None)

async def update_beam_server_status(message):
    try:
        api.client.servers.send_console_command(globalvariables.BEAM_SERVER_ID, 'status')
        data = api.client.servers.files.get_file_contents(globalvariables.BEAM_SERVER_ID, './Server.log').text[-972:].replace(' ', '')
        serverInfo = api.client.servers.get_server(globalvariables.BEAM_SERVER_ID)['relationships']['variables']['data']
              
        port = 30814
        name = 'BeamMP Server'
        online_players =  data.split("TotalPlayers:", 2)[1].split("\n", 2)[0]
        max_players = 0
        for prop in serverInfo:
            if prop['attributes']['name'] == 'Max Players':
                max_players = prop['attributes']['server_value']
                break

        if data:
            onlineStatus = onlineString
        else:
            onlineStatus = offlineString

        embed = createDefaultEmbed(onlineStatus, 'BeamMP Server', globalvariables.BEAM_LOGO)

        setFooter(embed)
        
        embed.add_field(name="Name", value=name, inline=False)
        embed.add_field(name="Address", value=globalvariables.PUBLIC_ADDRESS, inline=True)
        embed.add_field(name="Port", value=port, inline=True)
        embed.add_field(name="Players", value=f"{online_players}/{max_players}", inline=False)
    except Exception as ex:
        embed = createDefaultEmbed(offlineString, 'BeamMP Server', globalvariables.BEAM_LOGO)

        setFooter(embed)

        embed.add_field(name="Uh Oh!", value='Sorry The server is down.', inline=False)
        embed.add_field(name="Error", value=ex, inline=False)

    # Send the embed to the discord channel
    await message.edit(embed=embed)


def fetchData(url):
    request = Request(
        url=url, 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    response = urlopen(request)
    return json.load(response) 

def setFooter(embed):
    # Get the time and add as footer
    now = datetime.now()
    current_time = now.strftime("%a %d %b %H:%M")
    embed.set_footer(text=f"Last Updated: {current_time}")

def createDefaultEmbed(description, name, logo):
    embed=discord.Embed(title="Server Status", description=description, color=0x109319)
    embed.set_author(name=name, icon_url=logo)
    embed.set_thumbnail(url=logo)

    return embed

class ButtonView(discord.ui.View):
    def __init__(self, port):
        super().__init__()
        button = discord.ui.Button(label='Connect', style=discord.ButtonStyle.url, url=f'http://64.99.208.39:{port}/')
        self.add_item(button)