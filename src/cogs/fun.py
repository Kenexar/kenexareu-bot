import random
import uuid as u

import nextcord
from nextcord.ext import commands
from nextcord.ui import View, Button


class CreateButton(Button):
    def __init__(self, label):
        super().__init__(style=nextcord.ButtonStyle.blurple, emoji="1️⃣")

    async def callback(self, interaction):
      await interaction.response.send_message(f"{interaction.user.id}", ephemeral=True)


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
        button1 = Button(style=nextcord.ButtonStyle.blurple, emoji="1️⃣")
        button2 = Button(style=nextcord.ButtonStyle.blurple, emoji="2️⃣")
        button3 = Button(style=nextcord.ButtonStyle.blurple, emoji="3️⃣")
        button4 = Button(style=nextcord.ButtonStyle.blurple, emoji="4️⃣")

        view = View()
        view.add_item(button1)
        view.add_item(button2)
        view.add_item(button3)
        view.add_item(button4)
        await ctx.channel.purge()

        await ctx.send(f'Test: {u.uuid4()}', view=view)


def setup(bot):
    bot.add_cog(Fun(bot))
