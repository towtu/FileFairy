import time
import shutil
from pathlib import Path
from watchdog.events import FileSystemEventHandler
from config.ignored_files import is_ignored
from config.settings import MIN_FILE_SIZE_KB, OUTPUT_FOLDER, DATE_SORTING
from duplicate_detector import is_duplicate, add_hash
from filename_cleaner import clean_filename
from conflict_resolver import resolve_conflict
from categorizer import categorize_file
from stats_tracker import log_action
from undo_manager import record_move
from notifier import send_notification
from datetime import datetime

class DownloadHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            self.process_file(Path(event.src_path))
            
    def on_moved(self, event):
        if not event.is_directory:
            self.process_file(Path(event.dest_path))

    def process_file(self, filepath: Path):
        if is_ignored(filepath.name):
            return
            
        if not self.wait_for_download(filepath):
            return
            
        try:
            if filepath.stat().st_size < (MIN_FILE_SIZE_KB * 1024):
                return
        except FileNotFoundError:
            return
            
        if is_duplicate(filepath):
            date_str = datetime.now().strftime("%Y-%m")
            dest_dir = OUTPUT_FOLDER / "_Duplicates" / date_str
            dest_dir.mkdir(parents=True, exist_ok=True)
            new_path = resolve_conflict(dest_dir, filepath.name)
            self.move_file(filepath, new_path, "DUPLICATE")
            send_notification("Duplicate Found", f"Moved {filepath.name} to duplicates.")
            return

        clean_name = clean_filename(filepath.name)
        curr_filepath = filepath
        if clean_name != filepath.name:
            new_filepath = filepath.parent / clean_name
            try:
                curr_filepath = filepath.rename(new_filepath)
            except FileExistsError:
                curr_filepath = resolve_conflict(filepath.parent, clean_name)
                curr_filepath = filepath.rename(curr_filepath)

        dest_dir = categorize_file(curr_filepath)
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        final_path = resolve_conflict(dest_dir, curr_filepath.name)
        
        self.move_file(curr_filepath, final_path, "MOVED")
        
        add_hash(final_path)
        
        if "_Unknown" in str(final_path):
            send_notification("Unknown File", f"Could not categorize {final_path.name}")
        else:
            send_notification("File Organized", f"{final_path.name} moved to {dest_dir.name}")

    def wait_for_download(self, filepath: Path, timeout=60) -> bool:
        historic_size = -1
        retries = 0
        while retries < timeout:
            if not filepath.exists():
                return False
                
            try:
                current_size = filepath.stat().st_size
            except FileNotFoundError:
                return False
                
            if current_size == historic_size and current_size > 0:
                time.sleep(2)
                return True
                
            historic_size = current_size
            time.sleep(1)
            retries += 1
            
        return False
        
    def move_file(self, src: Path, dest: Path, action: str):
        try:
            shutil.move(str(src), str(dest))
            # try to make path relative to parent folder
            rel_dest = str(dest.relative_to(OUTPUT_FOLDER.parent)) if OUTPUT_FOLDER.parent in dest.parents else str(dest)
            log_action(action, src.name, rel_dest)
            record_move(src, dest)
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {action.ljust(9)} | {src.name[:30].ljust(30)} → {rel_dest}")
        except Exception as e:
            print(f"Error moving {src.name}: {e}")
