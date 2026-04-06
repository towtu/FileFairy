import sys
from pathlib import Path
from config.settings import OUTPUT_FOLDER

def search(query: str):
    print(f"Search: {query}")
    print("Found:")
    found = False
    for filepath in OUTPUT_FOLDER.rglob("*"):
        if filepath.is_file() and query.lower() in filepath.name.lower():
            try:
                rel_path = filepath.relative_to(OUTPUT_FOLDER.parent)
                print(f"  → {rel_path}")
                found = True
            except ValueError:
                print(f"  → {filepath}")
                found = True
                
    if not found:
        print("  (No files found)")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        search(sys.argv[1])
    else:
        print("Usage: python search.py <keyword>")
