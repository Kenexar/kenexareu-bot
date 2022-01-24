import nextcord

from cogs.etc.config import current_timestamp, EMBED_ST, PREFIX


def help_embed(mode='normal'):

    embed = nextcord.Embed(title='Help Site',
                           color=EMBED_ST,
                           timestamp=current_timestamp())

    if mode == 'admin-reload':
        embed.add_field(name=f'{PREFIX}listmodules', value='Des: List all current modules in Cogs', inline=False)
        embed.add_field(name=f'{PREFIX}reload (module name)', value=f'Des: Reload giving Cog module\nExample: {PREFIX}reload cogs.casino', inline=False)

    if mode == 'qr-creator':
        pass

    return embed

