from discord.ext import commands

class misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def clean(self, ctx, limit: int):
            await ctx.channel.purge(limit=limit)
            await ctx.send('Cleared by {}'.format(ctx.author.mention))
            await ctx.message.delete()

    @clean.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You cant do that!")

def setup(bot):
    bot.add_cog(misc(bot))