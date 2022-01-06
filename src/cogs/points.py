from datetime import datetime

import nextcord
from discord.ext import commands

from cogs.etc.config import PROJECT_NAME, db, colors
from cogs.etc.presets import add_points, lvl_up


class Points(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        cur = db.cursor(buffered=True)

        cur.execute("SELECT Level, Experience, Multiplier, Coins FROM points WHERE User=%s and Name=%s;", (message.author.id, PROJECT_NAME))
        fetcher = cur.fetchone()

        if not fetcher:
            cur.execute("INSERT INTO points(User, Coins, Experience, Level, Multiplier, Name) VALUES (%s, %s, %s, %s, %s, %s);",
                        (message.author.id, 100, 0, 1, 1, PROJECT_NAME))
            db.commit()
            cur.close()
            return

        add_points(message.author.id, cur, fetcher)

        if lvl_up(message.author.id, cur, fetcher):
            await message.channel.send(f'{message.author.mention} Just leveld up to {int(fetcher[0]) + 1}, yippie')

    @commands.command()
    async def top(self, ctx):
        # Top placed on the Server
        cursor = db.cursor()

        cursor.execute("SELECT User, Points FROM points WHERE Name=%s", (PROJECT_NAME,))

        fetcher = cursor.fetchall()

        for i in fetcher:
            print(i)

        cursor.close()
        pass

    @commands.command()
    async def level(self, ctx, user=None):
        # Show the Player information for the Game lulw, it returns an embed i think
        cur = db.cursor()

        cur.execute("SELECT Level, Experience, Multiplier, Coins FROM points WHERE User=%s AND Name=%s;",
                    (user.strip("<@!>") if user else ctx.message.author.id, PROJECT_NAME))

        fetcher = cur.fetchone()

        if not fetcher:
            return await ctx.send(f'{ctx.message.author.mention if not user else user} hat noch keine Nachricht auf den Server geschrieben!')

        level = fetcher[0]
        exp = fetcher[1]
        multi = fetcher[2]
        coins = fetcher[3]

        for color_range in colors:
            if level <= 100 and level in color_range:
                color = colors[color_range]
                break
            elif 1000 > level > 100 and level - int(str(level)[0]) * 100 in color_range:
                color = colors[color_range]
                break
        else:
            color = 0x9B9B9B

        username = await self.bot.fetch_user(user.strip("<@!>")) if user else ctx.message.author.name

        embed = nextcord.Embed(title=f'Level info for {username}',
                               description=f':up: Current Level: {level}\n'
                                           f':fish_cake: Current Experience: {exp}\n'
                                           f':game_die: Current Multiplier: {multi}x\n'
                                           f':coin: Current Coins: {coins}',
                               color=color,
                               timestamp=datetime.now())

        await ctx.send(embed=embed)
        cur.close()


def setup(bot):
    bot.add_cog(Points(bot))
