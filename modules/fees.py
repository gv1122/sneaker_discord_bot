import discord
import json
import datetime
from decimal import Decimal
from discord.ext import commands

with open("./data/config.json") as f:
    config = json.load(f)

EMBED_IMAGE = config['embed_img']
EMBED_COLOR = config['embed_color']
LOG_CHANNEL = config['log_channel']

class Selling_Rates(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Latency: {round (self.bot.latency * 1000)}')

    @commands.command()
    async def test(self, ctx):
        await ctx.send(msg_id)

    @commands.command()
    async def fee(self, ctx, amnt: float):

        author = ctx.message.author.id

        stockx = round(amnt * .13, 2)
        stockx2 = round(amnt * .125, 2)
        stockx3 = round(amnt * .12, 2)
        stockx4 = round(amnt * .115, 2)
        stockx5 = round(amnt * .11, 2)

        firstFee = amnt * .095 + 5
        tot = amnt - firstFee
        prcFee = tot * .029
        goatUS = firstFee + prcFee

        firstFeeunder = amnt * .15 + 5
        totunder = amnt - firstFeeunder
        prcFeeunder = totunder * .029
        goatUSunder = firstFeeunder + prcFeeunder

        firstCAfee = amnt * .095 + 20
        totCA = amnt - firstCAfee
        prcFeeCA = totCA * .029
        goatCA = firstCAfee + prcFeeCA

        firstCAfeeunder = amnt * .15 + 20
        totCAunder = amnt - firstCAfeeunder
        prcFeeCAunder = totCAunder * .029
        goatCAunder = firstCAfeeunder + prcFeeCAunder

        stadGoods = amnt * .20

        grailed = amnt * .09

        mercari = amnt * .10

        flightClub = amnt * .095 + 5
        FCtot = amnt - flightClub
        FCprcFee = FCtot * .029
        flcbFee = flightClub + FCprcFee

        embed = discord.Embed(title='Helper Bot Fee Calculator', timestamp=datetime.datetime.utcnow(), color=EMBED_COLOR)
        embed.add_field(name='StockX', value='React with 1️⃣ to see your StockX fees!')
        embed.add_field(name='Goat', value='React with 2️⃣ to see your Goat fees!',inline=False)        
        embed.add_field(name='Misc', value='React with 3️⃣ to see your Misc fees!',inline=False)        

        embed.set_footer(text='Helper Bot Fees | React with 1 first, then 2, then 3', icon_url=EMBED_IMAGE)

        global stockxEmbed

        stockxEmbed = discord.Embed(title='Stockx:', color=EMBED_COLOR)

        stockxEmbed.add_field(name='StockX Level 1:', value=f"${format(amnt - stockx, '.2f')}", inline=False)
        stockxEmbed.add_field(name='StockX Level 2:', value=f"${format(amnt - stockx2, '.2f')}", inline=False)
        stockxEmbed.add_field(name='StockX Level 3:', value=f"${format(amnt - stockx3, '.2f')}", inline=False)
        stockxEmbed.add_field(name='StockX Level 4:', value=f"${format(amnt - stockx4, '.2f')}", inline=False)
        stockxEmbed.add_field(name='StockX Level 5:', value=f"${format(amnt - stockx5, '.2f')}", inline=False)

        stockxEmbed.set_footer(text='Helper Bot Fees', icon_url=EMBED_IMAGE)

        global goatEmbed

        goatEmbed = discord.Embed(title='Goat:', color=EMBED_COLOR)

        goatEmbed.add_field(name='Goat US (Rating >= 100):', value=f"${round(amnt - goatUS, 2) + .01} + optional photos", inline=False)
        goatEmbed.add_field(name='Goat US (Rating >= 90):', value=f"${round(amnt - goatUS, 2) + .01}", inline=False)
        goatEmbed.add_field(name='Goat US (Rating >= 70 and <= 89):', value=f"${round(amnt - goatUSunder, 2) + .01}", inline=False)
        goatEmbed.add_field(name='Goat CA (Rating >= 100):', value=f"${round(amnt- goatCA, 2) + .01} + optional photos", inline=False)
        goatEmbed.add_field(name='Goat CA (Rating >= 90):', value=f"${round(amnt- goatCA, 2) + .01}", inline=False)
        goatEmbed.add_field(name='Goat CA (Rating >= 70 and <= 89):', value=f"${round(amnt - goatCAunder, 2) + .01}", inline=False)

        goatEmbed.set_footer(text='Helper Bot Fees', icon_url=EMBED_IMAGE)

        global miscEmbed

        miscEmbed = discord.Embed(title='Misc Fees', color=EMBED_COLOR)

        miscEmbed.add_field(name='Ebay:', value=f"Free on sales > 100", inline=False)
        miscEmbed.add_field(name='Stadium Goods:', value=f"${round(amnt- stadGoods, 2)}", inline=False)
        miscEmbed.add_field(name='Flight Club:', value=f"${round(amnt- flcbFee, 2)}", inline=False)
        miscEmbed.add_field(name='Grailed:', value=f"${round(amnt- grailed, 2)}", inline=False)
        miscEmbed.add_field(name='Mercari:', value=f"${round(amnt- mercari, 2)}", inline=False)

        miscEmbed.set_footer(text='Helper Bot Fees', icon_url=EMBED_IMAGE)

        endEmbed = discord.Embed(title='Time limit exceeded, please reuse this command!', color=EMBED_COLOR)

        global msg_id

        global msg

        msg = await ctx.send(embed=embed)
        
        msg_id = msg.id

        await msg.add_reaction('1️⃣')
        await msg.add_reaction('2️⃣')
        await msg.add_reaction('3️⃣')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        try:
            if msg_id == payload.message_id and payload.user_id != 12343524234:
                if payload.emoji.name == "1️⃣" :
                    await msg.edit(embed=stockxEmbed)
                    await msg.remove_reaction('1️⃣', member = payload.member)
                elif payload.emoji.name == "2️⃣" :
                    await msg.edit(embed=goatEmbed)
                    await msg.remove_reaction('2️⃣', member = payload.member)
                elif payload.emoji.name == "3️⃣":
                    await msg.edit(embed=miscEmbed)
                    await msg.remove_reaction('3️⃣', member = payload.member)
        except:
            pass


    @fee.error
    async def fee_error(self, ctx, error):
        LOG_CHAN = self.bot.get_channel(LOG_CHANNEL)
        NAME = "fees bot"
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
    bot.add_cog(Selling_Rates(bot))