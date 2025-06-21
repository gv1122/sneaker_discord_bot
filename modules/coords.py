import discord
import requests
import datetime
import json
import urllib.parse
from discord.ext import commands

with open('./data/config.json') as file:
    config = json.load(file)

API_KEY = config['api-key']
BASE_URL = config['base_api_url']
EMBED_IMAGE = config['embed_img']
EMBED_COLOR = config['embed_color']
LOG_CHANNEL = config['log_channel']

class Coordinates(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cords(self, ctx, *, arg):

        params = {
            "key": API_KEY,
            "address": arg
        }

        response = requests.get(BASE_URL, params=params).json()
        status = response['status']

        name = response['results'][0]['formatted_address']
        geo = response['results'][0]["geometry"]
        lat = geo['location']['lat']
        lon = geo['location']['lng']
        final = str(lat) + "," + str(lon)
        final = urllib.parse.quote(final)

        embed = discord.Embed(title="Coords for:", description=f'[{name}](https://www.google.com/maps/search/?api=1&query={final})', timestamp=datetime.datetime.utcnow(), color=EMBED_COLOR)
        embed.add_field(name='Latitude:', value=lat)
        embed.add_field(name='Longitude:', value=lon)
        embed.add_field(name=f'Copy/Paste into Google Maps', value=f'```{lat} , {lon}```', inline=False)
        embed.set_footer(text='Helper Bot', icon_url=EMBED_IMAGE)
        await ctx.send(embed=embed)

    @cords.error
    async def cords_error(self, ctx, error):
        LOG_CHAN = self.bot.get_channel(LOG_CHANNEL)
        NAME = "coords bot"
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(color=EMBED_COLOR)
            embed.description = 'You are missing an argument!'
            await ctx.send(embed=embed)
        else:
            author = ctx.message.author
            error = error
            message_id = f"https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ctx.message.id}"

            embed = discord.Embed(title=f"someone made an error while using {NAME}", color=EMBED_COLOR)
            embed.add_field(name="Author", value=f"{author}")
            embed.add_field(name="Error", value=f"`{error}`")
            embed.add_field(name="Message ID", value=f"{message_id}")

            await LOG_CHAN.send(f"<@123456789>", embed=embed)


def setup(bot):
    bot.add_cog(Coordinates(bot))

