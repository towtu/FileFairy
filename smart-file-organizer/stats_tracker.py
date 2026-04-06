import sqlite3
from datetime import datetime
from config.settings import STATS_DB

def init_db():
    conn = sqlite3.connect(STATS_DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS stats
                 (timestamp text, action text, filename text, destination text)''')
    conn.commit()
    conn.close()

def log_action(action, filename, destination):
    conn = sqlite3.connect(STATS_DB)
    c = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO stats VALUES (?, ?, ?, ?)", (now, action, filename, destination))
    conn.commit()
    conn.close()
