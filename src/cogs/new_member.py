from nextcord.ext import commands

from src.cogs.etc.config import NEW_MEMBER_CHANNEL


class NewMember(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
def setup(bot):
    bot.add_cog(NewMember(bot))
