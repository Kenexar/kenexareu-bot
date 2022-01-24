import concurrent
import random
import uuid as u
from time import time

import nextcord
from nextcord.ext import commands
from nextcord.ui import View, Button

from cogs.etc.config import db


class CreateButton(Button):
    def __init__(self, label):
        super().__init__(style=nextcord.ButtonStyle.blurple, emoji="1️⃣")

    async def callback(self, interaction):
        await interaction.response.send_message(f"{interaction.user.id}", ephemeral=True)


async def delete_ticket(ctx, ticket_id):
    with concurrent.futures.thread.ThreadPoolExecutor(max_workers=1) as executor:
        tic = time()
        executor.submit(
            db.cursor().execute(
                "DELETE FROM tickets WHERE ticket_id=%s" %
                int(ticket_id))
        )
        executor.submit(db.commit())
        toc = time()
        print("was to execute " + "DELETE FROM tickets WHERE ticket_id=%s" % int(ticket_id))
        await ctx.send(f'Time: {toc - tic}')


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """
    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        select = nextcord.ui.Select(
            placeholder="Choose up to 2 options",
            max_values=1,
            min_values=1,
            options=[
                nextcord.SelectOption(label="11", description="1"),
                nextcord.SelectOption(label="22", description="2"),
                nextcord.SelectOption(label="33", description="3")
            ]
        )

        view = View()
        view.add_item(select)

        await interaction.followup.send("Peter hat einen hasen der huan", view=view)
"""

    @commands.Command
    async def roll(self, ctx):
        await delete_ticket(ctx, "1234")



def setup(bot):
    bot.add_cog(Fun(bot))
