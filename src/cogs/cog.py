import nextcord
from nextcord.ext import commands


class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Command
    async def tests(self, ctx):
        print('loaded')


def setup(bot):
    bot.add_cog(Cog(bot))
