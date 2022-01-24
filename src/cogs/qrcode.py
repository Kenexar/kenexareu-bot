from datetime import datetime

import nextcord
from nextcord.ext import commands

from cogs.etc.config import ESCAPE, PREFIX


class QRCode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(QRCode(bot))
