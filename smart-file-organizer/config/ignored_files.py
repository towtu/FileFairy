IGNORED_EXTENSIONS = {
    ".crdownload", # Chrome
    ".part",       # Firefox
    ".tmp",        # Generic temp
    ".download",   # Safari
    ".opdownload", # Opera
}

IGNORED_PREFIXES = [
    ".com.google.Chrome"
]

def is_ignored(filename):
    filename_lower = filename.lower()
    for ext in IGNORED_EXTENSIONS:
        if filename_lower.endswith(ext):
            return True
            
    for prefix in IGNORED_PREFIXES:
        if filename_lower.startswith(prefix.lower()):
            return True
            
    return False
