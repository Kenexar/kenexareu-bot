from datetime import datetime
from sys import version
import platform
import pkg_resources
from nextcord.ext import commands, tasks
from nextcord.ext.commands import CommandNotFound
from nextcord.ext.commands import MissingPermissions
from nextcord.ext.commands import has_permissions

from cogs.etc.config import MEMBER_COUNTER, GUILD_ID, db


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.log = False

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'''Bot is ready! 
Infos:
  Time: {datetime.now().strftime("%H:%M:%S")}
  System: {platform.system()}
  Python version: {version}''')

        await self.current_user.start()

    @commands.Cog.listener()
    async def on_connect(self):
        print(f'Connecting to Discord. Getting ready...')

    @tasks.loop(minutes=10)
    async def current_user(self):
        """ here comes the current user count on the server """
        guild = self.bot.get_guild(GUILD_ID)
        channel = guild.get_channel(MEMBER_COUNTER)

        # Just a lil MYSQL bitch!
        db.ping()

        await channel.edit(name=f'Member: {guild.member_count}')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):  # Function doing intense computing!
        if isinstance(error, CommandNotFound) or isinstance(error, MissingPermissions):  # error handler
            return await ctx.send("Command not found.")
        raise error

    @commands.Command
    @has_permissions(administrator=True)
    async def logging(self, ctx):
        if len(ctx.message.content.split()) > 1:
            with open('cogs/etc/logging', 'w') as f:
                f.write('cock')
            self.log = True
            return await ctx.send('Logging started!')

        with open('cogs/etc/logging', 'w') as f:
            f.truncate()

        await ctx.send('Logging stopped!')


def setup(bot):
    bot.add_cog(Admin(bot))
