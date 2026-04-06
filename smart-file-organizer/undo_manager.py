import sqlite3
import shutil
from pathlib import Path
from config.settings import HISTORY_DB

def init_db():
    conn = sqlite3.connect(HISTORY_DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  original_path text, 
                  new_path text, 
                  timestamp text)''')
    conn.commit()
    conn.close()

def record_move(original_path: Path, new_path: Path):
    conn = sqlite3.connect(HISTORY_DB)
    c = conn.cursor()
    from datetime import datetime
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO history (original_path, new_path, timestamp) VALUES (?, ?, ?)", 
              (str(original_path), str(new_path), now))
    conn.commit()
    conn.close()

def undo_last_move() -> bool:
    conn = sqlite3.connect(HISTORY_DB)
    c = conn.cursor()
    c.execute("SELECT id, original_path, new_path FROM history ORDER BY id DESC LIMIT 1")
    row = c.fetchone()
    if not row:
        conn.close()
        return False
        
    id_, orig_path_str, new_path_str = row
    
    orig_path = Path(orig_path_str)
    new_path = Path(new_path_str)
    
    try:
        if new_path.exists():
            shutil.move(str(new_path), str(orig_path))
            c.execute("DELETE FROM history WHERE id=?", (id_,))
            conn.commit()
            success = True
        else:
            success = False
    except Exception:
        success = False
        
    conn.close()
    return success
