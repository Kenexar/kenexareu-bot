import nextcord
import pytz

from datetime import datetime

from nextcord.ext import commands
from nextcord.ext.commands import has_permissions, MissingPermissions
from nextcord.ext.commands import CommandNotFound

from src.cogs.etc.config import (TICKET_CHANNEL,
                                 EMBED_ST,
                                 current_timestamp,
                                 MEMBER_COUNTER,
                                 GUILD_ID)


#todo:
# Support tickets,
# Team bewerbungen,
# spenden tickets,
# fraktions tickets,
#  specific team roles gets pinged


class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ticket')
    @has_permissions(administrator=True)
    async def _ticket(self, ctx):
        """ For the Ticket message to start the wizard """

        tz = pytz.timezone('Europe/Berlin')
        berlin_now = datetime.now(tz)

        embed = nextcord.Embed(title='Create your Ticket here :)',
                               color=EMBED_ST,
                               timestamp=current_timestamp())

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Ticket(bot))
