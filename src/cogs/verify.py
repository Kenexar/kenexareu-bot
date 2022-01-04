import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions
from nextcord.utils import get

from cogs.etc.config import VERIFY_CHANNEL, EMBED_ST, current_timestamp, REACTIONS


class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @has_permissions(administrator=True)
    async def _verify(self, ctx):
        channel = self.bot.get_channel(VERIFY_CHANNEL)
        await channel.purge()

        embed = nextcord.Embed(title='SunSide Regelwerk `v2.0`',
                               description='''
                                Um erfolgreich durch die Passkontrolle zu gelangen müssen Sie das Regelwerk von SunSide Roleplay gelesen und verstanden haben!
                                Dann einfach auf ✅ reagieren und es kann losgehen.

                                Zum Neuem SunSide Regelwerk V2📜
                                Stand: 22.12.21 12:20 Uhr
                                https://docs.google.com/document/d/16acjtyQXc-ToTQoWlll7iiBALNpwscoJif9EmYSFiCc/edit?usp=sharing
                                
                                
                                Willkommen auf SunSide RolePlay.
                                
                                Mit freundlichen Grüßen
                                euer SunSide-Team''',
                               color=EMBED_ST,
                               timestamp=current_timestamp())
        m = await channel.send(embed=embed)

        await m.add_reaction(REACTIONS.get('check'))

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            return

        id = payload.emoji.id
        name = payload.emoji.name

        if f'<:{name}:{id}>' == REACTIONS.get('check') and payload.channel_id == VERIFY_CHANNEL:
            role = get(self.bot.get_guild(int(payload.guild_id)).roles, name='Spieler')
            await payload.member.add_roles(role)


def setup(bot):
    bot.add_cog(Verify(bot))
