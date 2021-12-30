from nextcord.ext import commands

#todo:
# Support tickets,
# Team bewerbungen,
# spenden tickets,
# fraktions tickets


class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Ticket(bot))
