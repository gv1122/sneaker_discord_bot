import discord
import requests
import json
import datetime
from discord.ext import commands

with open("./data/config.json") as f:
    config = json.load(f)

EMBED_COLOR = config['embed_color']
EMBED_IMAGE = config['embed_img']
LOG_CHANNEL = config['log_channel']

class AtcGen(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command()
    async def atc(self, ctx, url):
        vars = []
        titles = []
        site = url[:url.index(".com")]
        jsonLink = url + ".json"

        r = requests.get(jsonLink)
        r = r.json()
        
        img = r['product']['image']['src']
        prodname = r["product"]["title"]
        

        for i in r["product"]["variants"]:
            id = i['id']
            vars.append(id)
            title = i['title']
            titles.append(title)
        embed = discord.Embed(title=prodname, url=url, color=EMBED_COLOR, timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=img)
        x = 0
        for i in titles:
            #stock = r["product"]["variants"][x]["inventory_quantity"]
            if "inventory_quantity" in r["product"]["variants"][x]:
                
                stock = r["product"]["variants"][x]["inventory_quantity"]
                if stock == 0:
                    embed.add_field(name=f"Size {i}" , value=f'[~~OOS~~]({site + ".com/cart/" + str(vars[x]) + ":1"})', inline=False)
                else:
                    embed.add_field(name=f"Size {i}" , value=f'[Click Here]({site + ".com/cart/" + str(vars[x]) + ":1"})', inline=False)
            else:
                embed.add_field(name=f"Size {i}" , value=f'[Click Here]({site + ".com/cart/" + str(vars[x]) + ":1"})', inline=False)
            x = x+1
        embed.set_footer(icon_url=EMBED_IMAGE, text=f"Helper Bot")
        await ctx.send(embed=embed)


    @atc.error
    async def var_error(self, ctx, error):
        LOG_CHAN = self.bot.get_channel(LOG_CHANNEL)
        NAME = "atc generator bot"
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
    bot.add_cog(AtcGen(bot))