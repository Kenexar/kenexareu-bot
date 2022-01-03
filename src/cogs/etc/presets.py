import mysql.connector.cursor
import nextcord

from src.cogs.etc.config import EMBED_ST
from src.cogs.etc.config import PROJECT_NAME
from src.cogs.etc.config import db
from mysql.connector.errors import ProgrammingError
from nextcord import Embed


def parser(rounds=int, toparse=list, option=list) -> list or str:
    """ This is a small self written Argparser

    This Function parse given Arguments for administration

    :param rounds:int: Insert the max number of words for the return
    :param toparse:list: Gives the Arg to Parse
    :param option:list: Insert option for parsing

    :return: list
    """

    return_list = []

    for key in toparse:
        if toparse[toparse.index(key)] in option:
            for i in range(rounds):
                try:
                    return_list.append(toparse[i])
                except IndexError:
                    return 'Index out of range'
            return return_list
        return return_list


def whitelist(mode=str, payload=dict) -> Embed or str:
    """Whitelist function whitelist a member

    :param mode:str-add: Add a Member to the Whitelist for Administration
    :param mode:str-list: List all members on the whitelist
    :param mode:str-remove: Remove a Member from the Whitelist
    :param member: Serve the member

    :returns: String or nextord.Embed object
    """

    cur_db = db.cursor()

    if mode == 'list':
        cur_db.execute(
            f"SELECT user_name, rank FROM whitelist WHERE name=%s", (PROJECT_NAME,))
        fetcher = cur_db.fetchall()
        cur_db.close()
        embed = nextcord.Embed(title='Whitelist', color=EMBED_ST)

        if fetcher:
            for i in fetcher:
                embed.add_field(name=i[0],
                                value=f'Rank: {WHITELIST_RANKS[i[1]]}',
                                inline=False)
        else:
            return 'Cannot find any entries'
        return embed

    if mode == 'add':
        member = payload.get('member')
        rank = payload.get('rank')
        username = payload.get('name')

        cur_db.execute(
            "INSERT INTO whitelist(name, uid, rank, user_name) VALUES (%s, %s, %s, %s)",
            (PROJECT_NAME, member, rank, username))
        db.commit()
        cur_db.close()
        return f'Added <@{member}> to the [BOT]whitelist'

    if mode == 'remove':
        member = payload.get('user')
        cur_db.execute("DELETE FROM whitelist WHERE uid=%s and name=%s;",
                       (member, PROJECT_NAME))

        db.commit()
        cur_db.close()
        return f'Removed <@{member}> from [BOT]whitelist'

    return f'`{mode}` is not available'


def get_perm(user) -> int:
    """ ger_perm or fetch_perm (old) is for authorization purposes

    :param user: takes an nextcord.Member.id and provide it to the database where you become an numberic value back.

    """
    cur_db = db.cursor(buffered=True)
    cur_db.execute('SELECT rank FROM whitelist WHERE uid=%s;', (user,))
    try:
        r = cur_db.fetchone()[0]
    except TypeError:
        return 0
    cur_db.close()
    return r  # fetch from the result the tuples first index


def lvl_up(user, cur, fetcher):
    """ Yeah 8====D """
    if not isinstance(cur, mysql.connector.cursor.MySQLCursor):
        raise ProgrammingError('Cur Argument is not an MySQLCursor Object')

    current_lvl = fetcher[0]
    exp = fetcher[1]
    coins = int(fetcher[3]) + 200

    if current_lvl < int(exp ** (1 / 4)):
        cur.execute("UPDATE points SET Level=%s, Coins=%s WHERE User=%s;", (int(exp ** (1 / 4)), coins, user))
        db.commit()

        cur.close()
        return True


def add_points(user, cur, payload):
    if not isinstance(cur, mysql.connector.cursor.MySQLCursor):
        raise ProgrammingError('Cur Argument is not an MySQLCursor Object')

    current_exp = payload[1] + (2 * float(payload[2]))  # EXP Addition

    cur.execute("UPDATE points SET Experience=%s WHERE User=%s;", (current_exp, user))
    db.commit()
    return
