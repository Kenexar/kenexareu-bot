import asyncio
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
from src.cogs.etc.config import TICKET_REACTIONS
from src.cogs.etc.config import REACTIONS
from src.cogs.etc.config import TICKET_CATEGORY
from src.cogs.etc.config import TICKET_CATEGORY_CLOSED
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

    @commands.command(name='ticket')
    @has_permissions(administrator=True)
    async def _ticket(self, ctx):
        """ For the Ticket message to start the wizard """

        channel = self.bot.get_channel(ctx.channel.id)
        await channel.purge()

        embed = nextcord.Embed(title='Erstelle ein Ticket :)',
                               description='Reagiere mit ➕ um dein ticket zu erstellen',
                               color=EMBED_ST,
                               timestamp=current_timestamp())

        message = await ctx.send(embed=embed)
        await message.add_reaction('➕')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            return

        reaction = payload.emoji

        guild = self.bot.get_guild(payload.guild_id)
        category_open = self.bot.get_channel(TICKET_CATEGORY)
        category_closed = self.bot.get_channel(TICKET_CATEGORY_CLOSED)

        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        if reaction.name == '➕':
            await message.remove_reaction(reaction, payload.member)

            channel = await guild.create_text_channel(name=f'ticket-{random.randint(1000, 9999)}', category=category_open)
            await channel.set_permissions(payload.member, read_messages=True, send_messages=True)

            embed = nextcord.Embed(title='Ticket Wizard',
                                   description=f'''**Reagiere mit den Folgenden emotes um dein Ticket zu erstellen!**
                                                   1️⃣ : Support Ticket
                                                   2️⃣ : Team Bewerbung
                                                   3️⃣ : Spenden Ticket
                                                   4️⃣ : Fraktions Ticket
                                                   5️⃣ : Andere
                                                   {REACTIONS['block']} : Um das Ticket zu schliessen''',
                                   color=EMBED_ST,
                                   timestamp=current_timestamp())

            embed.set_footer(text=payload.member)
            message = await channel.send(payload.member.mention, embed=embed)

            for emote in ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', REACTIONS['block']]:
                await message.add_reaction(emote)
            return

        if reaction.name in ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣'] and 'ticket' in channel.name:
            await message.remove_reaction(reaction, payload.member)

            await channel.send(TICKET_REACTIONS[reaction.name]['message'])

            for r in ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']:
                await message.remove_reaction(r, self.bot.user)

            for member in TICKET_REACTIONS[reaction.name]['action']:
                role = get(guild.roles, id=member)
                await channel.set_permissions(role, read_messages=True, send_messages=True)

            return

        if f'<:{reaction.name}:{reaction.id}>' == REACTIONS['block']:
            await message.remove_reaction(reaction, payload.member)

            channel = self.bot.get_channel(payload.channel_id)

            if 'closed' in channel.name:
                await channel.send('Ticket will Terminate its self')
                await asyncio.sleep(3)

                try:
                    await channel.delete()
                except nextcord.errors.NotFound:
                    pass
                return

            if 'ticket' in channel.name:
                await channel.send('Ticket wird geschlossen in 3 Sekunden')
                await asyncio.sleep(3)

                await channel.move(end=True, category=category_closed)
                await channel.edit(name=f'{channel.name}-closed', sync_permissions=True)


def setup(bot):
    bot.add_cog(Ticket(bot))
