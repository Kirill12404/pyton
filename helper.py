import sqlite3
conn=sqlite3.connect('Tk.dp')

cur.execute('''CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tg_id INTEGER,
           highscore INTEGER
            ''')

cur.execute('''CREATE TABLE IF NOT EXISTS queshens(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            queshens TEXT 
            ''')

conn.commit()

def save_user(id,score):
    cur.execute('''
    INSERT INTO users(
                    tg_id, highscore) VALUES(?,?)
    ''',[id,score])
    conn.commit()
