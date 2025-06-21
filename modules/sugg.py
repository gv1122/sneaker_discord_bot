import discord
import datetime
import time
import json
from discord.ext import commands

with open('./data/config.json') as f:
    config = json.load(f)

EMBED_IMAGE = config['embed_img']
EMBED_COLOR = config['embed_color']
loading_gif = "https://media.tenor.com/images/a742721ea2075bc3956a2ff62c9bfeef/tenor.gif"
success_img = "https://cliply.co/wp-content/uploads/2021/03/372103860_CHECK_MARK_400px.gif"

def is_me():
    def predicate(ctx):
        return ctx.message.author.id == 123456789
    return commands.check(predicate)


class Suggestions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @is_me()
    async def logging(self, ctx, tf: bool):
        global log
        
        log = tf

        await ctx.send(log)
        

    @commands.command()
    @is_me()
    async def prompt(self, ctx):      
        channel = self.bot.get_channel(12345)

        embed = discord.Embed(title="Helper Bot Suggestions", description=f'DM me your suggestions! -> {self.bot.user.mention}', color=EMBED_COLOR,)
        embed.add_field(name=f'Use the command by typing `.sugg` `suggestion here`', value=f'Once I receive and process it, it will show up in {channel.mention}!')
        embed.set_image(url=EMBED_IMAGE)
        await ctx.send(embed=embed)

    @prompt.error
    async def permError(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("You don't have perms to send this!")



    @commands.command()
    async def sugg(self, ctx, *, message):
    
        channel = self.bot.get_channel(12345)

        log_channel = self.bot.get_channel(12345)

        if not isinstance(ctx.channel, discord.channel.DMChannel):
            await ctx.send("Please only use this command in DM's with me!")
        else:
            username = ctx.message.author.id
            
            embed = discord.Embed(
                title="There is a new suggestion!",
                color=EMBED_COLOR,
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_footer(
                text="Helper Bot",
                icon_url=EMBED_IMAGE
            )
            embed.add_field(name= "Suggestion by:", value= f"<@{username}> | " + f"{username}" )
            embed.add_field(name= "Suggestion:", value = message ,inline=False)

            loading_embed = discord.Embed(
                title=f'Please wait!',
                color=EMBED_COLOR,
                description=f'Sending to {channel.mention}'
            )
            loading_embed.set_thumbnail(url=loading_gif)

            success_embed = discord.Embed(
                title=f'Successfully Sent!',
                color=EMBED_COLOR,
                description=f'Check {channel.mention}!'
            )
            success_embed.set_thumbnail(url=success_img)

            loadingEmbed = await ctx.send(embed=loading_embed)
            time.sleep(1)

            await loadingEmbed.edit(embed=success_embed)
            msg = await channel.send(embed=embed)
            await msg.add_reaction("👍")
            await msg.add_reaction("👎")

            if log:
                await log_channel.send(f'<@&12345> - New suggestion in <#12345> by <@{username}>!')

    @sugg.error
    async def suggError(self, ctx, error):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            if isinstance(error, commands.MissingRequiredArgument):
                await ctx.send("You are missing an arugment!")
        else:
            if isinstance(error, commands.MissingRequiredArgument):
                await ctx.send("Please only DM me this command, and you are missing an argument!") 



def setup(bot):
    bot.add_cog(Suggestions(bot))