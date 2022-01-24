from nextcord.ext import commands


class Casino(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.bj_cards = {
            'hearts': {'ace': '🂱', 2: '🂲', 3: '🂳', 4: '🂴', 5: '🂵', 6: '🂶', 7: '🂷', 8: '🂸', 9: '🂹', 10: '🂺',
                       'jack': '🂻', 'queen': '🂽', 'king': '🂾'},

            'pik': {'ace': '🂡', 2: '🂢', 3: '🂣', 4: '🂤', 5: '🂥', 6: '🂦', 7: '🂧', 8: '🂨', 9: '🂩', 10: '🂪',
                    'jack': '🂫', 'queen': '🂭', 'king': '🂮'},

            'caro': {'ace': '🃁', 2: '🃂', 3: '🃃', 4: '🃄', 5: '🃅', 6: '🃆', 7: '🃇', 8: '🃈', 9: '🃉', 10: '🃊',
                     'jack': '🃋', 'queen': '🃍', 'king': '🃎'},

            'tree': {'ace': '🃑', 2: '🃒', 3: '🃓', 4: '🃔', 5: '🃕', 6: '🃖', 7: '🃗', 8: '🃘', 9: '🃙', 10: '🃚',
                     'jack': '🃛', 'queen': '🃝', 'king': '🃞'},
            'back': '🂠'}

    @commands.command(aliases=['bj'])
    async def blackjack(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Casino(bot))
