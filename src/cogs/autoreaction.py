import nextcord
from nextcord.ext import commands


class AutoResponse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.CHANNEL = 926242538472501370

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.CHANNEL:
            await message.add_reaction("<:check:926545063641747506>")
            await message.add_reaction("<:block:926545051172077579>")


def setup(bot):
    bot.add_cog(AutoResponse(bot))
