import time
import hashlib
import aiohttp
import discord
import library.globalvariables as globalvariables

async def get_player_data(player_id, ctx):
    secret = 'tB87#kPtkxqOS2'
    timestamp = str(int(time.time() * 1000))

    # Base form
    base_form = f"fid={player_id}&time={timestamp}"
    sign = hashlib.md5((base_form + secret).encode('utf-8')).hexdigest()

    # Request body
    post_data = {
        "sign": sign,
        "fid": str(player_id),
        "time": timestamp
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(globalvariables.WOS_API, data=post_data, headers=headers) as response:
                response.raise_for_status()
                json_data = await response.json()

                if json_data.get('code') != 0:
                    print(f"API Error: {json_data.get('msg', 'Unknown error')}")
                    await ctx.response.send_message('Player not found')

                player = json_data['data']

                embed = discord.Embed(
                    title=f"Player Added to List!",
                    color=discord.Color.blue()
                )
                embed.set_thumbnail(url=player['avatar_image'])
                embed.add_field(name="ID", value=player['fid'], inline=True)
                embed.add_field(name="State", value=player['kid'], inline=True)
                embed.add_field(name="Name", value=player['nickname'], inline=False)

                # Furnace Level label as a field
                embed.add_field(name="Furnace Level", value="", inline=False)

                # Actual rendered image (full width)
                embed.set_image(url=player['stove_lv_content'])

                await ctx.response.send_message(embed=embed)


        except aiohttp.ClientError as e:
            print(f"Request failed: {e}")
            await ctx.response.send_message('Player not found')

