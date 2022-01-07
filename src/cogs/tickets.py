import asyncio
import concurrent
import random

import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions
from nextcord.utils import get

from cogs.etc.config import EMBED_ST, db, REACTIONS, TICKET_CATEGORY, TICKET_CATEGORY_CLOSED, TICKET_REACTIONS, \
    current_timestamp
from nextcord.ui import View, Button


async def delete_ticket(ticket_id):
    with concurrent.futures.thread.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(
            db.cursor().execute(
                "DELETE FROM tickets WHERE ticket_id=%s" %
                ticket_id),
            db.commit()
        )


async def archive_ticket(ticket_id):
    with concurrent.futures.thread.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(
            db.cursor().execute(
                "UPDATE tickets set is_archived = 1 WHERE ticket_id = %s",
                (ticket_id,)),
            db.commit()
        )


async def update_ticket(user_id, ticket_id):
    with concurrent.futures.thread.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(
            db.cursor().execute(
                "INSERT INTO tickets(user_id, ticket_id, is_archived) values (%s, %s, 0)",
                (user_id, ticket_id)),
            db.commit()
        )


async def get_open_tickets(user_id) -> int:
    with concurrent.futures.thread.ThreadPoolExecutor(max_workers=2) as executor:
        cur = db.cursor()
        executor.submit(
            cur.execute("SELECT user_id FROM tickets WHERE user_id=%s AND is_archived=false",
                        (user_id,)),
        )

        fetcher = cur.fetchall()
        return len(fetcher)


"""

 "SELECT user_id FROM tickets WHERE user_id=%s AND is_archived=false",
            (user_id,)),
"""


class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ticket')
    @has_permissions(administrator=True)
    async def _ticket(self, ctx):
        """ For the Ticket message to start the wizard """

        channel = self.bot.get_channel(ctx.channel.id)
        await channel.purge()

        embed = nextcord.Embed(title='Erstelle ein Ticket',
                               description='Zum erstellen eines **Tickets** klicke auf "**Create Ticket**"!',
                               color=EMBED_ST,
                               )

        view = View()
        view.add_item(Button(label="Create Ticket", style=nextcord.ButtonStyle.blurple, custom_id="createTicket"))

        await ctx.send(embed=embed, view=view)

    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        reaction = interaction.data["custom_id"]

        guild = self.bot.get_guild(interaction.guild_id)
        category_open = self.bot.get_channel(TICKET_CATEGORY)
        category_closed = self.bot.get_channel(TICKET_CATEGORY_CLOSED)

        channel = self.bot.get_channel(interaction.channel_id)

        member_id = interaction.user.id

        if reaction == 'createTicket':
            print("Pressed")
            if await get_open_tickets(member_id) >= 2:
                await interaction.followup.send("Du kannst nicht mehr als Zwei tickets eröffnen!",
                                                ephemeral=True)
                return

            ticket_id = random.randint(1000, 9999)

            channel = await guild.create_text_channel(name=f'ticket-{ticket_id}',
                                                      category=category_open)

            await update_ticket(member_id, ticket_id)

            await channel.set_permissions(interaction.user, read_messages=True, send_messages=True)

            button1 = Button(style=nextcord.ButtonStyle.blurple, emoji="1️⃣", custom_id="button-1")
            button2 = Button(style=nextcord.ButtonStyle.blurple, emoji="2️⃣", custom_id="button-2")
            button3 = Button(style=nextcord.ButtonStyle.blurple, emoji="3️⃣", custom_id="button-3")
            button4 = Button(style=nextcord.ButtonStyle.blurple, emoji="4️⃣", custom_id="button-4")
            button5 = Button(style=nextcord.ButtonStyle.blurple, emoji="4️⃣", custom_id="button-5")
            button6 = Button(style=nextcord.ButtonStyle.red, emoji="🔒", custom_id="button-6")

            view = View()
            view.add_item(button1)
            view.add_item(button2)
            view.add_item(button3)
            view.add_item(button4)
            view.add_item(button5)
            view.add_item(button6)

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

            embed.set_footer(text=interaction.user)
            message = await channel.send(interaction.user.mention, embed=embed, view=view)

        if reaction in ['button-1', 'button-2', 'button-3', 'button-4'] and 'ticket' in channel.name:
            button6 = Button(style=nextcord.ButtonStyle.red, emoji="🔒", custom_id="button-6")
            view = View()
            view.add_item(button6)

            await interaction.edit_original_message(view=view)

            await channel.send(TICKET_REACTIONS[reaction]['message'])

            for member in TICKET_REACTIONS[reaction]['action']:
                role = get(guild.roles, id=member)
                await channel.set_permissions(role, read_messages=True, send_messages=True)

            return

        if reaction == "button-6":

            channel = self.bot.get_channel(interaction.channel_id)

            if 'closed' in channel.name:
                await channel.send('Ticket will Terminate its self')
                await delete_ticket(int(channel.name.strip("ticket- -closed")))

                button6 = Button(style=nextcord.ButtonStyle.red, emoji="🗑️", custom_id="button-6", disabled=True)
                view = View()
                view.add_item(button6)

                await interaction.edit_original_message(view=view)

                await asyncio.sleep(3)

                try:
                    await channel.delete()
                except nextcord.errors.NotFound:
                    pass
                return

            if 'ticket' in channel.name:

                button6 = Button(style=nextcord.ButtonStyle.red, emoji="🔒", custom_id="button-6", disabled=True)
                view = View()
                view.add_item(button6)

                await interaction.edit_original_message(view=view)

                await archive_ticket(int(channel.name.strip("ticket- -closed")))
                await channel.send('Ticket wird geschlossen... ')
                await asyncio.sleep(.5)

                await channel.move(end=True, category=category_closed)
                await channel.edit(name=f'{channel.name}-closed', sync_permissions=True)

                button6 = Button(style=nextcord.ButtonStyle.red, emoji="🗑️", custom_id="button-6", disabled=False)
                view = View()
                view.add_item(button6)

                await interaction.edit_original_message(view=view)



def setup(bot):
    bot.add_cog(Ticket(bot))
