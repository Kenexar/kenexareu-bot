from nextcord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.log = False

    @commands.Cog.listener()
    async def on_ready(self):
        print('Ready')

    @commands.Command
    async def logging(self, ctx):
        return
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
