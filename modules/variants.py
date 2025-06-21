import discord
from discord import message
import requests
import json
import datetime
from discord.ext import commands

with open("./data/config.json") as f:
    config = json.load(f)

EMBED_COLOR = config['embed_color']
EMBED_IMAGE = config['embed_img']
LOG_CHANNEL = config['log_channel']

class Variants(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def var(self, ctx, url):
        allVars = ''
        allSizes = ''
        

        if url.startswith("https://") and ".com" in url:

            s = requests.session()
                
            new_url= url + ".json"
            response = s.get(new_url).json()
            allInfo = response['product']['variants']
            
            price = response['product']['variants'][0]['price']
            img = response['product']['image']['src']

            for variants in allInfo:
                id = variants['id']
                allVars += "\n" + str(id)
            
            for sizes in allInfo:
                size = sizes['title']
                allSizes += "\n" + str(size)

            formattedSizes = '```' + f'{allSizes}' + '```'
            formattedVars ='```' + f'{allVars}' + '```'

            embed = discord.Embed(title = response['product']['title'], url = url, description='Price: ' + f'**{price}**', color=EMBED_COLOR, timestamp=datetime.datetime.utcnow())
            embed.set_thumbnail(url=img)
            embed.add_field(name='Sizes', value=formattedSizes)
            embed.add_field(name='Variants', value=formattedVars)
            embed.set_footer(icon_url=EMBED_IMAGE, text=f"Helper Bot")

            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(color=EMBED_COLOR)
            embed.description = 'This is not a proper url!'
            await ctx.send(embed=embed)

    @var.error
    async def var_error(self, ctx, error):
        LOG_CHAN = self.bot.get_channel(LOG_CHANNEL)
        NAME = "variant bot"
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
    bot.add_cog(Variants(bot))