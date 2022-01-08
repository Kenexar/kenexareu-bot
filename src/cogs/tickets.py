import asyncio
import random
from concurrent.futures.thread import ThreadPoolExecutor

import nextcord
from cogs.etc.config import EMBED_ST, db, REACTIONS, TICKET_CATEGORY, TICKET_CATEGORY_CLOSED, TICKET_REACTIONS, \
    current_timestamp
from cogs.etc.config import TICKET_CHANNEL
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions
from nextcord.ui import View, Button
from nextcord.utils import get


# Todo:
#   Ticket reactivation

async def delete_ticket(ticket_id):
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(
            db.cursor().execute("DELETE FROM tickets WHERE ticket_id=%s", (ticket_id,)),
            db.commit()
        )


async def archive_ticket(ticket_id):
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(
            db.cursor().execute("UPDATE tickets set is_archived = 1 WHERE ticket_id=%s", (ticket_id,)),
            db.commit()
        )


async def re_archive_ticket(ticket_id):
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(
            db.cursor().execute("UPDATE tickets set is_archived=0 WHERE ticket_id=%s", (ticket_id,)),
            db.commit()
        )


async def update_ticket(user_id, ticket_id):
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(
            db.cursor().execute(
                "INSERT INTO tickets(user_id, ticket_id, is_archived) values (%s, %s, 0)",
                (user_id, ticket_id)),
            db.commit()
        )


async def get_open_tickets(user_id) -> int:
    with ThreadPoolExecutor(max_workers=2) as executor:
        cur = db.cursor()
        executor.submit(
            cur.execute("SELECT user_id FROM tickets WHERE user_id=%s AND is_archived=false",
                        (user_id,)),
        )

        fetcher = cur.fetchall()
        return len(fetcher)


async def create_ticket():
    embed = nextcord.Embed(title='Erstelle ein Ticket',
                           description='Zum erstellen eines **Tickets** klicke auf "**Create Ticket**"!',
                           color=EMBED_ST,
                           timestamp=current_timestamp())

    view = View()
    view.add_item(Button(label="Create Ticket", style=nextcord.ButtonStyle.blurple, custom_id="createTicket"))

    return embed, view


class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ticket')
    @has_permissions(administrator=True)
    async def _ticket(self, ctx):
        """ For the Ticket message to start the wizard """

        channel = self.bot.get_channel(ctx.channel.id)
        await channel.purge()

        createticket = await create_ticket()

        await ctx.send(embed=createticket[0], view=createticket[1])

    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(TICKET_CHANNEL)
        await channel.purge()

        createticket = await create_ticket()

        await channel.send(embed=createticket[0], view=createticket[1])

    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        reaction = interaction.data["custom_id"]

        guild = self.bot.get_guild(interaction.guild_id)
        category_open = self.bot.get_channel(TICKET_CATEGORY)
        category_closed = self.bot.get_channel(TICKET_CATEGORY_CLOSED)

        channel = self.bot.get_channel(interaction.channel_id)

        member_id = interaction.user.id

        if reaction == 'createTicket':
            if await get_open_tickets(member_id) >= 2:
                await interaction.followup.send("Du kannst nicht mehr als Zwei tickets eröffnen!",
                                                ephemeral=True)
                return

            ticket_id = random.randint(1000, 9999)

            channel = await guild.create_text_channel(name=f'ticket-{ticket_id}',
                                                      category=category_open)

            await update_ticket(member_id, ticket_id)

            await channel.set_permissions(interaction.user, read_messages=True, send_messages=True)

            view = View()
            button_list = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "🔒"]

            for button in button_list:
                button1 = Button(style=nextcord.ButtonStyle.blurple,
                                 emoji=button,
                                 custom_id=f"button-{button_list.index(button) + 1}")
                view.add_item(button1)

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

        if reaction in ['button-1', 'button-2', 'button-3', 'button-4', 'button-5'] and 'ticket' in channel.name:
            button6 = Button(style=nextcord.ButtonStyle.red, emoji="🔒", custom_id="button-6")
            view = View()
            view.add_item(button6)

            await interaction.edit_original_message(view=view)

            await channel.send(TICKET_REACTIONS[reaction]['message'])

            for member in TICKET_REACTIONS[reaction]['action']:
                role = get(guild.roles, id=member)
                await channel.set_permissions(role, read_messages=True, send_messages=True)

            return

        if reaction == "button-7":
            channel = self.bot.get_channel(interaction.channel_id)

            await re_archive_ticket(int(channel.name.strip("ticket- -closed")))

            view = View()
            view.add_item(Button(style=nextcord.ButtonStyle.red, emoji="🔒", custom_id="button-8", disabled=False))

            cur = db.cursor()
            cur.execute("select user_id from tickets where ticket_id=%s", (int(channel.name.strip("ticket- -closed")),))

            memberid = cur.fetchone()
            print(memberid[0])
            cur.close()

            await channel.move(end=True, category=category_open)
            await channel.edit(name=channel.name.strip("-closed"))

            await channel.set_permissions(self.bot.get_user(memberid[0]), read_messages=True, send_messages=True)

            try:
                await interaction.edit_original_message(view=view)
            except nextcord.errors.NotFound:
                print('notfound')
            return

        if reaction in ("button-6",):
            channel = self.bot.get_channel(interaction.channel_id)

            if 'closed' in channel.name:
                await channel.send('Ticket will Terminate its self')
                await delete_ticket(int(channel.name.strip("ticket- -closed")))

                button6 = Button(style=nextcord.ButtonStyle.red, emoji="🗑️", custom_id="button-6", disabled=True)

                view = View()
                view.add_item(button6)

                try:
                    await interaction.edit_original_message(view=view)
                except nextcord.errors.NotFound:
                    print('notfound')

                await asyncio.sleep(.5)

                try:
                    await channel.delete()
                except nextcord.errors.NotFound:
                    pass
                return

            if 'ticket' in channel.name:
                button6 = Button(style=nextcord.ButtonStyle.red, emoji="🔒", custom_id="button-6", disabled=True)

                view = View()
                view.add_item(button6)

                try:
                    await interaction.edit_original_message(view=view)
                except nextcord.errors.NotFound:
                    print('notfound')

                await archive_ticket(int(channel.name.strip("ticket- -closed")))

                await channel.send('Ticket wird geschlossen... ')
                await asyncio.sleep(.5)

                await channel.move(end=True, category=category_closed)
                await channel.edit(name=channel.name + '-closed', sync_permissions=True)

                button6 = Button(style=nextcord.ButtonStyle.red, emoji="🗑️", custom_id="button-6", disabled=False)
                button7 = Button(style=nextcord.ButtonStyle.red, emoji="📝", custom_id="button-7", disabled=False)

                view = View()
                view.add_item(button6)
                view.add_item(button7)

                await interaction.edit_original_message(view=view)



def setup(bot):
    bot.add_cog(Ticket(bot))
