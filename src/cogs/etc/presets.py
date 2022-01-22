import mysql.connector.cursor
import nextcord

from cogs.etc.config import db
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
