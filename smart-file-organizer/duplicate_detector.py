import hashlib
import sqlite3
from pathlib import Path
from config.settings import HASHES_DB

def get_file_hash(filepath: Path) -> str:
    """Calculate MD5 hash of a file."""
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        return ""

def init_db():
    conn = sqlite3.connect(HASHES_DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS file_hashes
                 (filepath text, md5_hash text UNIQUE)''')
    conn.commit()
    conn.close()

def is_duplicate(filepath: Path) -> bool:
    """Check if file hash already exists in DB."""
    file_hash = get_file_hash(filepath)
    if not file_hash:
        return False
        
    conn = sqlite3.connect(HASHES_DB)
    c = conn.cursor()
    c.execute("SELECT filepath FROM file_hashes WHERE md5_hash=?", (file_hash,))
    result = c.fetchone()
    conn.close()
    
    return bool(result)

def add_hash(filepath: Path):
    """Add file hash to database."""
    file_hash = get_file_hash(filepath)
    if not file_hash:
        return
        
    conn = sqlite3.connect(HASHES_DB)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO file_hashes VALUES (?, ?)", (str(filepath), file_hash))
        conn.commit()
    except sqlite3.IntegrityError:
        pass # Already exists
    conn.close()

def remove_hash(filepath: Path):
    conn = sqlite3.connect(HASHES_DB)
    c = conn.cursor()
    c.execute("DELETE FROM file_hashes WHERE filepath=?", (str(filepath),))
    conn.commit()
    conn.close()
