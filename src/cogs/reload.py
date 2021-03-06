import asyncio
import os

import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions

from cogs.etc.config import EMBED_ST, PREFIX
from cogs.etc.config import current_timestamp
from cogs.etc.config import current_cog_modules

from cogs.etc.embeds import help_embed


class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Command
    @has_permissions(administrator=True)
    async def reload(self, ctx, cog_module=None):
        if not cog_module:
            return await ctx.send(embed=help_embed('admin-reload'))

        if not cog_module in current_cog_modules():
            return await ctx.send('The giving module is not Loaded!')

        self.bot.unload_extension(cog_module)
        await asyncio.sleep(1)

        self.bot.load_extension(cog_module)
        await ctx.send(f'{cog_module} Reloaded!')

    @commands.Command
    @has_permissions(administrator=True)
    async def listmodules(self, ctx):
        embed = nextcord.Embed(title='All Cogs that are loaded are listed here!',
                               description='\n'.join(current_cog_modules()),
                               color=EMBED_ST,
                               timestamp=current_timestamp())

        embed.add_field(name=f'To reload cog modules, write `{PREFIX}reload (cog_module)`',
                        value=f'Example: `{PREFIX}reload cogs.casino`',
                        inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Reload(bot))
