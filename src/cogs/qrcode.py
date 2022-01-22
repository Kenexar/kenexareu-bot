import nextcord
from nextcord.ext import commands

from cogs.etc.config import ESCAPE, PREFIX


class QRCode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Command
    async def createqr(self, ctx, *args):  # with my own argparse function
        if not len(args):
            return await ctx.send(f'{PREFIX}createqr Needs an Argument, Try -h for help!')

        colores = []
        bgcolores = []
        vdata = []

        color = (0, 0, 0)
        bgcolor = (255, 255, 255)
        box = 6

        options = ['b', 'c', 'bg', 'd', 'h', 'm']

        mod = 0

        async def parser(rounds, option, validate, limit):
            var = 0
            while var != rounds:
                var += 1
                try:
                    val = int(args[args.index(f'{ESCAPE}{option}') + var].strip(','))
                except ValueError:
                    await ctx.send('One Argument is not an Integer')
                    break

                if type(val) == int and not val >= limit + 1:  # Double check
                    validate.append(val)
                else:
                    await ctx.send(f'One Argument is not under or {limit}')
                    break

            def converter(list_):
                return (*list_,)

            return converter(validate)

        for option in options:
            if f'{ESCAPE}{option}' in list(args):
                if 'c' == option:  # color argparser
                    color = await parser(3, 'c', colores, 255)

                elif 'bg' == option:  # back-color argparser
                    bgcolor = await parser(3, 'bg', bgcolores, 255)

                elif 'd' == option:  # data argparser
                    for i in args[args.index(f'{ESCAPE}d') + 1:]:
                        if not [i for t in options if f'{ESCAPE}{t}' == i]:
                            vdata.append(i)
                        else:
                            break

                elif 'b' == option:  # box-size argparser
                    try:
                        box_size = int(args[args.index(f'{ESCAPE}b') + 1].strip(','))
                        if box_size >= 100:
                            await ctx.send('The box Argument is too Large, please take a Number under 100')
                            break
                        else:
                            box = box_size

                    except ValueError:
                        break

                elif 'm' == option:
                    mode = args[args.index(f'{ESCAPE}m'):args.index(f'{ESCAPE}m') + 2]
                    if len(mode) == 2:
                        for i in self.mode:
                            if mode[1] == i:
                                mode_end = self.mode[i]
                                mod = 1
                                break

                elif 'h' == option or 'help' == option:
                    embed = nextcord.Embed(title=f'Help site for the Qr Code generator',
                                           timestamp=datetime.now(),
                                           color=0x3498DB) \
                        .add_field(name=f'{ESCAPE}d | *Data Argument',
                                   value=f'Usage: {ESCAPE}d *Data',
                                   inline=False) \
                        .add_field(name=f'{ESCAPE}c | Color Argument takes an RGB input',
                                   value=f'Usage: {ESCAPE}c R, G, B',
                                   inline=False) \
                        .add_field(name=f'{ESCAPE}bg | Background Color Argument Color Argument takes an RGB input',
                                   value=f'Usage: {ESCAPE}bg R, G, B',
                                   inline=False) \
                        .add_field(name=f'{ESCAPE}m | Set the Desgin for the, Currently only in BaW*',
                                   value=f'Usage: {ESCAPE}m vertical/horizontal/rounded. When you use the Arg you can\'t take any color!',
                                   inline=False) \
                        .set_thumbnail(
                        url='https://cdn.discordapp.com/attachments/887032886006530111/894227663072395284/embed_pic.png') \
                        .set_footer(text='*<arg> is an duty argument, BaW = Black and White')
                    await ctx.send(embed=embed)
                    mod = 'exit'

        data = str(vdata).translate({ord(i): None for i in "[',]"})
        if mod == 0:

            now = f'etc/{datetime.now().strftime("%Y-%m-%d_%H-%M-%S"), random.randint(1, 9999999)}.png'

            create_code_c(str(data), now, color, bgcolor, box)
            await ctx.send(file=nextcord.File(now))

            os.remove(now)
        elif mod == 1:

            now = f'etc/{datetime.now().strftime("%Y-%m-%d_%H-%M-%S"), random.randint(1, 9999999)}.png'

            create_code_b(str(data), now, mode_end)
            await ctx.send(file=nextcord.File(now))

            os.remove(now)
        else:
            pass

def setup(bot):
    bot.add_cog(QRCode(bot))
