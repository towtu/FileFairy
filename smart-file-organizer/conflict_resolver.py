from pathlib import Path

def resolve_conflict(destination_dir: Path, target_filename: str) -> Path:
    target_path = destination_dir / target_filename
    if not target_path.exists():
        return target_path
        
    name = target_path.stem
    ext = target_path.suffix
    counter = 2
    
    while True:
        new_name = f"{name}_{counter}{ext}"
        new_path = destination_dir / new_name
        if not new_path.exists():
            return new_path
        counter += 1
