import random

import nextcord
import pytz

from datetime import datetime

from nextcord import Interaction
from nextcord.ui import view
from nextcord import Button, ButtonStyle

from nextcord.ext import commands
from nextcord.ext.commands import has_permissions, MissingPermissions
from nextcord.ext.commands import CommandNotFound
from nextcord.utils import get

from src.cogs.etc.config import TICKET_CHANNEL
from src.cogs.etc.config import TICKET_CATEGORY
from src.cogs.etc.config import EMBED_ST
from src.cogs.etc.config import current_timestamp
from src.cogs.etc.config import MEMBER_COUNTER
from src.cogs.etc.config import GUILD_ID


#todo:
# Support tickets,
# Team bewerbungen,
# spenden tickets,
# fraktions tickets,
#  specific team roles gets pinged


class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Command
    async def print_cog(self, ctx):
        print(ctx.message)

    @commands.command(name='ticket')
    @has_permissions(administrator=True)
    async def _ticket(self, ctx):
        """ For the Ticket message to start the wizard """

        channel = self.bot.get_channel(ctx.channel.id)
        await channel.purge()

        embed = nextcord.Embed(title='Create your Ticket here :)',
                               description='React with ➕ to create a Ticket!',
                               color=EMBED_ST,
                               timestamp=current_timestamp())

        view.ButtonComponent()
        message = await ctx.send(embed=embed)
        await message.add_reaction('➕')

    def ticket_wizard(self, ctx):
        pass

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            return

        guild = self.bot.get_guild(payload.guild_id)
        category = self.bot.get_channel(TICKET_CATEGORY)
        print()

        if payload.emoji.name == '➕':
            channel = await guild.create_text_channel(name=f'ticket-{random.randint(1000, 9999)}', category=category)
            await channel.set_permissions(payload.member, read_messages=True, send_messages=True)


def setup(bot):
    bot.add_cog(Ticket(bot))
