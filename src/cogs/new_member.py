from nextcord.ext import commands


class NewMember(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(NewMember(bot))
