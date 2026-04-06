import re
from pathlib import Path
from config.settings import LOWERCASE_FILENAMES, REPLACE_SPACES

def clean_filename(filename: str) -> str:
    path_obj = Path(filename)
    name = path_obj.stem
    ext = path_obj.suffix
    
    if LOWERCASE_FILENAMES:
        name = name.lower()
        ext = ext.lower()
        
    if REPLACE_SPACES:
        name = name.replace(" ", "_")
        
    name = re.sub(r'[^a-zA-Z0-9_-]', '', name)
    name = re.sub(r'_+', '_', name)
    name = re.sub(r'-+', '-', name)
    
    if not name:
        name = "file"
        
    return f"{name}{ext}"
