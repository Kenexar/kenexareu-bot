from nextcord.ext import commands


class Casino(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Casino(bot))
