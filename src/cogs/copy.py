from nextcord.ext import commands


class Copy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        with open('cogs/etc/logging', 'r') as f:
            self.LOGGING = f.read()  #Trufy, Falsy, for myself i forgot things fast

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        with open('cogs/etc/logging', 'r') as f:  # yeah
            self.LOGGING = f.read()

        if not self.LOGGING:
            return

        await message.channel.send('coggers')


def setup(bot):
    bot.add_cog(Copy(bot))
