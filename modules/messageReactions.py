import discord
import json
from discord.ext import commands

with open("./data/config.json") as f:
    config = json.load(f)

LOG_CHANNEL = config['log_channel']
EMBED_COLOR = config['embed_color']
CHANNELS = [1, 2, 3]

class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in CHANNELS and message.author.id != 12345:
            await message.add_reaction("✅")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add_rchannel(self, ctx, *args: int):
        for i in args:
            CHANNELS.append(i)
        await ctx.send(f"Added **{args}** to your list! Current list is: `{CHANNELS}`")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def remove_rchannel(self, ctx, channel: int):
        if channel in CHANNELS:
            CHANNELS.remove(channel)
            await ctx.send(f"Removed **{channel}** to your list! Current list is: `{CHANNELS}`")
            
        else:
            await ctx.send(f'`{channel} is not already in your list!`')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def channels(self, ctx):
        await ctx.send(f'Current channels im reacting with `✅` in! `{CHANNELS}`')


    async def cog_command_error(self, ctx, error):
        LOG_CHAN = self.bot.get_channel(LOG_CHANNEL)
        NAME = "reactions bot"

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
            message_id = f"https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ctx.message.id}"

            embed = discord.Embed(title=f"someone made an error while using {NAME}", color=EMBED_COLOR)
            embed.add_field(name="Author", value=f"{author}")
            embed.add_field(name="Error", value=f"`{error}`")
            embed.add_field(name="Message ID", value=f"{message_id}")

            await LOG_CHAN.send(f"<@123456789>", embed=embed)


def setup(bot):
    bot.add_cog(Reactions(bot))