import sqlite3
conn=sqlite3.connect('aqua.db')
cur=conn.cursor()


cur.execute('''CREATE TABLE IF NOT EXISTS slides(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
length INTEGER,
description TEXT,
UNIQUE(name)
)''')
            
cur.execute('''CREATE TABLE IF NOT EXISTS requests(  
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
number TEXT NOT NULL,
UNIQUE(number)
)''')

cur.execute('''CREATE TABLE IF NOT EXISTS admins(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            UNIQUE(user_id)
            )
            ''')
 
conn.commit()

def add_reqests(name, number):
    cur.execute('INSERT INTO requests(name, number) VALUES (?, ?)', [name, number])
    conn.commit()

def add_admin(user_id):
        cur.execute('INSERT INTO admins(user_id) VALUES (?)', [user_id])
        conn.commit()
def add_slide(name, lenght, desc):
    cur.execute('INSERT INTO slides(name, length, description) VALUES (?, ?, ?)', [name, lenght, desc])
    conn.commit()