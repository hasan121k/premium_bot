import sqlite3, time

db = sqlite3.connect("users.db", check_same_thread=False)
cur = db.cursor()

# Users table
cur.execute("""
CREATE TABLE IF NOT EXISTS users(
 uid INTEGER PRIMARY KEY,
 device TEXT,
 expire INTEGER,
 paid INTEGER
)
""")
db.commit()

def add_user(uid, device, minutes):
    exp = int(time.time()) + minutes*60
    cur.execute("REPLACE INTO users VALUES(?,?,?,1)", (uid, device, exp))
    db.commit()

def remove_user(uid):
    cur.execute("DELETE FROM users WHERE uid=?", (uid,))
    db.commit()

def get_user(uid):
    cur.execute("SELECT * FROM users WHERE uid=?", (uid,))
    return cur.fetchone()

def list_users():
    cur.execute("SELECT * FROM users")
    return cur.fetchall()
