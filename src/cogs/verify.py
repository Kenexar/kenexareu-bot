import nextcord

from nextcord.ext import commands
from nextcord.utils import get


class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.guild = self.bot.get_guild(926242537713311754)

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            print(guild.id)
        print(self.guild)

    @commands.command()
    async def loop(self, amount=30):
        channel = self.bot.get_channel(926242537914634262)
        messages = []

        embed = nextcord.Embed(title='Verification',
                               description='Bitte Reagiere mit ✅ um dich zu Verifizieren!',
                               color=0x06ff95)
        m = await channel.send(embed=embed)
        await m.add_reaction('✅')
        await channel.send(m)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        print(payload)

        id = payload.user_id
        if payload.bot:
            return

        print(payload.message, payload.user)
        if str(payload.reaction) == '✅':
            role = get(payload.member.guild.roles, name='Spieler')
            await user.add_roles(role)


def setup(bot):
    bot.add_cog(Verify(bot))
