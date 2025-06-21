import discord
import json
from discord.ext import commands

with open("./data/config.json") as f:
    config = json.load(f)

EMBED_COLOR = config['embed_color']
LOG_CHANNEL = config['log_channel']


class Pinger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channelPinger = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        for i in self.channelPinger.keys():
            if i == message.channel.id and message.author.id != 123455:
                roleId = self.channelPinger[message.channel.id]
                await message.channel.send(f"<@&{roleId}>")
            
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add_pinger(self, ctx, channel:int, role_id:int):
        self.channelPinger[channel] = role_id
        embed = discord.Embed(title="Current Channels I'm Pinging In!")
        
        for i in self.channelPinger.keys():
            embed.add_field(name=f"<#{i}>", value=f"<@&{self.channelPinger[i]}>", inline=True)

        await ctx.send(f"Added **{channel}** to your list! Current list is: ")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def remove_pinger(self, ctx, channel: int):
        if channel in self.channelPinger.keys():
            self.channelPinger.pop(channel)
            try:
                embed = discord.Embed(title="Current Channels I'm Pinging In!")
                
                for i in self.channelPinger.keys():
                    embed.add_field(name=f"<#{i}>", value=f"<@&{self.channelPinger[i]}>", inline=False)

                await ctx.send(f"Removed **{channel}** to your list! Current list is: ")
                await ctx.send(embed=embed)
            except:
                await ctx.send("I'm not pinging anywhere right now!")
        else:
            await ctx.send(f'`{channel} is not already in your list!`')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def pingers(self, ctx):
        embed = discord.Embed(title="Current Channels I'm Pinging In!")
        for i in self.channelPinger.keys():
            embed.add_field(name=f"<#{i}>", value=f"<@&{self.channelPinger[i]}>", inline=True)
        
        await ctx.send(embed=embed)
    
    async def cog_command_error(self, ctx, error):
        LOG_CHAN = self.bot.get_channel(LOG_CHANNEL)
        NAME = "pinger bot"
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

            await LOG_CHAN.send(f"<@123456789>", embed=embed)

def setup(bot):
    bot.add_cog(Pinger(bot))