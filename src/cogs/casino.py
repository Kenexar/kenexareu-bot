from nextcord.ext import commands


class Casino(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Command
    async def blackjack(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Casino(bot))
