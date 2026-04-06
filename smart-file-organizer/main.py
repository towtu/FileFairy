import time
from watchdog.observers import Observer
from config.settings import WATCH_FOLDER, OUTPUT_FOLDER, ACADEMIC_MODE, AI_ENABLED
import duplicate_detector
import stats_tracker
import undo_manager
from watcher import DownloadHandler

def main():
    print(f"Starting Smart File Organizer...")
    
    # Load .env file if present
    try:
        from dotenv import load_dotenv
        load_dotenv()
        # Re-read API key after loading .env
        import os
        import config.settings as settings
        settings.GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", settings.GEMINI_API_KEY)
    except ImportError:
        pass
    
    WATCH_FOLDER.mkdir(parents=True, exist_ok=True)
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
    duplicate_detector.init_db()
    stats_tracker.init_db()
    undo_manager.init_db()
    
    print(f"Watching: {WATCH_FOLDER}")
    print(f"Output to: {OUTPUT_FOLDER}")
    print(f"Academic Mode: {'Enabled' if ACADEMIC_MODE else 'Disabled'}")
    
    if AI_ENABLED:
        from ai_categorizer import is_ai_available
        if is_ai_available():
            print(f"AI Categorization: Enabled (Gemini)")
        else:
            print(f"AI Categorization: Unavailable (falling back to rules)")
    else:
        print(f"AI Categorization: Disabled")
    
    print("Running in background... (Press Ctrl+C to stop)")
    
    observer = Observer()
    event_handler = DownloadHandler()
    observer.schedule(event_handler, str(WATCH_FOLDER), recursive=False)
    
    try:
        observer.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopping...")
    finally:
        observer.join()

if __name__ == "__main__":
    main()
