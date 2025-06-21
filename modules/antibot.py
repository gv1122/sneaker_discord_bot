import discord
import asyncio
import datetime
import json
from discord.ext import commands

with open("./data/antiBotData.json", encoding="utf8") as file:
    guides = json.load(file)
formatted_guides = json.dumps(guides, indent=2, ensure_ascii=False)
with open("./data/config.json") as f:
    config = json.load(f)
ANTIBOTROLE = config['antiBotRole']
ANTIBOTCHANNEL = config['antiBotChannel']
EMBED_COLOR = config['embed_color']
EMBED_IMAGE = config['embed_img']
LOG_CHANNEL = config['log_channel']

class pinger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldown = False
        self.enabled = "enabled"
        self.sites = [
            "ShopNiceKicks", 
            "Shoe Palace",
            "Kith",
            "KawsOne",
            "atmosusa",
            "concepts",
            "undefeated",
            "jimmyjazz",
            "dtlr",
            "Concepts",
            "eflash-us.doverstreetmarket",
            "TravisScott Shop"
        ]
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if not self.cooldown and message.channel.id == ANTIBOTCHANNEL:
            for embed in message.embeds:
                for i in self.sites:
                    if i.lower() in embed.author.name and "enabled" in embed.description:
                        name = embed.author.name
                        self.cooldown = True
                        await ANTIBOTCHANNEL.send(f'<@&{ANTIBOTROLE}>')
                        embed = discord.Embed(title=f'Checkpoint is up for {name}', color=EMBED_COLOR)
                        await ANTIBOTCHANNEL.send(embed=embed)
                        str = name
                        for i in guides:
                            if i.lower() in str.lower():
                                embed = discord.Embed(color=EMBED_COLOR, timestamp=datetime.datetime.utcnow())
                                embed.add_field(name="Bot Protection:", value=guides[i]["Bot Protection"])
                                embed.add_field(name="Proxy Protection", value=guides[i]["Proxy Protection"])
                                embed.add_field(name="Accounts", value=guides[i]["Accounts"])
                                embed.set_footer(text="Helper Bot", icon_url=EMBED_IMAGE)
                                await ANTIBOTCHANNEL.send(embed=embed)
                                break
                        await asyncio.sleep(3)
                        self.cooldown = False
                        break

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        member = payload.member
        guild = member.guild
        user_id = payload.user_id
        emoji = payload.emoji.name
        channel = self.bot.get_channel(payload.channel_id)
        
        first_monitor_guides = discord.Embed(title="Guides for Most Sites Being Monitored!",color=EMBED_COLOR)
        for n in guides:
            if n == "Kith":
                break
            else:
                first_monitor_guides.add_field(name="\u200b", value=f'**{n}:**', inline=False)
                first_monitor_guides.add_field(name="Bot Protection:", value=guides[n]["Bot Protection"])
                first_monitor_guides.add_field(name="Proxy Protection", value=guides[n]["Proxy Protection"])
                first_monitor_guides.add_field(name="Accounts", value=guides[n]["Accounts"])

        test_list = ["Kith", "ShopNiceKicks", "Undefeated", "AtmosUSA"]
        second_monitor_guides = discord.Embed(title="Guides for Most Sites Being Monitored!",color=EMBED_COLOR)
        for n in test_list:
            for e in guides:
                if n == e:
                    second_monitor_guides.add_field(name="\u200b", value=f'**{n}:**', inline=False)
                    second_monitor_guides.add_field(name="Bot Protection:", value=guides[n]["Bot Protection"])
                    second_monitor_guides.add_field(name="Proxy Protection", value=guides[n]["Proxy Protection"])
                    second_monitor_guides.add_field(name="Accounts", value=guides[n]["Accounts"])
                else:
                    continue       

        if user_id != self.bot.user.id:
            if emoji == "3️⃣":
                await msg.edit(embed=second_monitor_guides)
                await msg.remove_reaction("3️⃣", member)
            elif emoji == "2️⃣":
                await msg.edit(embed=first_monitor_guides)
                await msg.remove_reaction("2️⃣", member)
            elif emoji == "1️⃣":
                await msg.edit(embed=mainEmbed)
                await msg.remove_reaction("1️⃣", member)

        #await ctx.send(self.sites)
        #await ctx.send(f'```json\n{formatted_guides}\n```')

    @commands.command()
    async def sites(self, ctx):
        global mainEmbed
        mainEmbed = discord.Embed(title="Sites Being Monitoring for Anti-Bot!",color=EMBED_COLOR)
        site = 0
        for i in self.sites:
            mainEmbed.add_field(name=self.sites[site], value="✅", inline=False)
            site += 1
        global msg
        msg = await ctx.send(embed=mainEmbed)
        await msg.add_reaction("1️⃣")
        await msg.add_reaction("2️⃣")
        await msg.add_reaction("3️⃣")
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def addsite(self, ctx, site):
        if site.startswith("https://") and site.endswith("/"):
            await ctx.send(f'Site is valid! Adding {site} now!')
            self.sites.append(site)
            await ctx.send(f'Added site: {site}')
        else:
            await ctx.send("Site is not valid, make sure it is in this format - `https://site.com/`")
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def removesite(self, ctx, name):
        for i in self.sites:
            if name in i:
                self.sites.remove(name)
                await ctx.send(f'Removed site: {name}')
                        
    async def cog_command_error(self, ctx, error):
        LOG_CHAN = self.bot.get_channel(LOG_CHANNEL)
        NAME = "antibot bot"
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(color=EMBED_COLOR)
            embed.description = 'You are missing an argument!'
            await ctx.send(embed=embed)

        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(color=EMBED_COLOR)
            embed.description = 'Arguement is invalid! Need to be ID!'
            await ctx.send(embed=embed)

        else:
            author = ctx.message.author
            error = error
            message_id = f"https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ctx.message.id}"

            embed = discord.Embed(title=f"someone made an error while using {NAME}", color=EMBED_COLOR)
            embed.add_field(name="Author", value=f"{author}")
            embed.add_field(name="Error", value=f"`{error}`")
            embed.add_field(name="Message ID", value=f"{message_id}")

            await LOG_CHAN.send(f"<@123445453>", embed=embed)

def setup(bot):
    bot.add_cog(pinger(bot))
