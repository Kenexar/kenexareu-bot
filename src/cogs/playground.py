from src.cogs.etc.config import db

with db.cursor as cur:
    cur.execute('select * from users;')
    print(cur.fetchall())
