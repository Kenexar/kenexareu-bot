import random

from nextcord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Command
    async def roll(self, ctx):
        await ctx.send(f'{ctx.message.author.mention} you rolled a: {random.randint(1, 100)}!')


def setup(bot):
    bot.add_cog(Fun(bot))
