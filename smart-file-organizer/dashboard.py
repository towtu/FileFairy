"""
Real-time Monitoring Dashboard for Smart File Organizer
Displays live statistics and activity from your organized files
"""

import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from config.settings import STATS_DB, OUTPUT_FOLDER
import time
import os

class MonitoringDashboard:
    def __init__(self):
        self.stats_db = STATS_DB
        self.output_folder = OUTPUT_FOLDER
        
    def get_total_files_organized(self):
        """Get total count of organized files."""
        if not self.stats_db.exists():
            return 0
        
        try:
            conn = sqlite3.connect(self.stats_db)
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM stats WHERE action='MOVED'")
            count = c.fetchone()[0]
            conn.close()
            return count
        except:
            return 0
    
    def get_today_count(self):
        """Get count of files organized today."""
        if not self.stats_db.exists():
            return 0
            
        try:
            conn = sqlite3.connect(self.stats_db)
            c = conn.cursor()
            today = datetime.now().strftime("%Y-%m-%d")
            c.execute("SELECT COUNT(*) FROM stats WHERE action='MOVED' AND timestamp LIKE ?", (f"{today}%",))
            count = c.fetchone()[0]
            conn.close()
            return count
        except:
            return 0
    
    def get_duplicates_found(self):
        """Get count of duplicate files detected."""
        if not self.stats_db.exists():
            return 0
            
        try:
            conn = sqlite3.connect(self.stats_db)
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM stats WHERE action='DUPLICATE'")
            count = c.fetchone()[0]
            conn.close()
            return count
        except:
            return 0
    
    def get_category_breakdown(self):
        """Get file count by major category."""
        if not self.output_folder.exists():
            return {}
        
        categories = {}
        try:
            for item in self.output_folder.iterdir():
                if item.is_dir() and not item.name.startswith('_'):
                    # Count files recursively
                    file_count = sum(1 for _ in item.rglob('*') if _.is_file())
                    if file_count > 0:
                        categories[item.name] = file_count
        except:
            pass
        
        return dict(sorted(categories.items(), key=lambda x: x[1], reverse=True))
    
    def get_recent_activity(self, limit=10):
        """Get recent file organization activity."""
        if not self.stats_db.exists():
            return []
        
        try:
            conn = sqlite3.connect(self.stats_db)
            c = conn.cursor()
            c.execute("""
                SELECT timestamp, action, filename, destination 
                FROM stats 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (limit,))
            activities = c.fetchall()
            conn.close()
            return activities
        except:
            return []
    
    def get_unknown_files(self):
        """Get count of unknown files needing review."""
        unknown_dir = self.output_folder / "_Unknown"
        if not unknown_dir.exists():
            return 0
        
        try:
            return sum(1 for _ in unknown_dir.rglob('*') if _.is_file())
        except:
            return 0
    
    def get_duplicates_size(self):
        """Get total size of duplicate files."""
        dup_dir = self.output_folder / "_Duplicates"
        if not dup_dir.exists():
            return 0
        
        try:
            total_size = sum(f.stat().st_size for f in dup_dir.rglob('*') if f.is_file())
            return total_size / (1024 * 1024)  # Convert to MB
        except:
            return 0
    
    def print_dashboard(self):
        """Print formatted dashboard to terminal."""
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print("\n")
        print("=" * 80)
        print(" SMART FILE ORGANIZER - MONITORING DASHBOARD ".center(80))
        print("=" * 80)
        print()
        
        # Get all stats
        total = self.get_total_files_organized()
        today = self.get_today_count()
        duplicates = self.get_duplicates_found()
        unknown = self.get_unknown_files()
        dup_size = self.get_duplicates_size()
        categories = self.get_category_breakdown()
        recent = self.get_recent_activity(5)
        
        # Display statistics
        print("STATISTICS")
        print("-" * 80)
        print(f"  Total Files Organized:  {total:,}")
        print(f"  Files Organized Today:  {today}")
        print(f"  Duplicates Detected:    {duplicates}")
        print(f"  Unknown Files:          {unknown}  [!]" if unknown > 0 else f"  Unknown Files:          {unknown}")
        print(f"  Storage Saved by Dupes: {dup_size:.1f} MB")
        print()
        
        # Display category breakdown
        print("TOP CATEGORIES")
        print("-" * 80)
        if categories:
            for i, (category, count) in enumerate(list(categories.items())[:8], 1):
                percent = int(count / sum(categories.values()) * 100) if categories else 0
                bar = "#" * (percent // 5) + "-" * (20 - percent // 5)
                print(f"  {i}. {category:20} {count:4} files [{bar}] {percent:3}%")
        else:
            print("  (No files organized yet)")
        print()
        
        # Display recent activity
        print("RECENT ACTIVITY")
        print("-" * 80)
        if recent:
            for timestamp, action, filename, destination in recent:
                action_marker = "[OK]" if action == "MOVED" else "[!]" if action == "DUPLICATE" else "[?]"
                print(f"  {action_marker} [{timestamp}] {action:10} {filename[:20]:20} -> {destination[:35]}")
        else:
            print("  (No recent activity)")
        print()
        
        # Display status
        print("STATUS")
        print("-" * 80)
        if today > 0:
            print(f"  [OK] Running - {today} file(s) organized today")
        else:
            print(f"  [OK] Running - Ready to organize files")
        
        if unknown > 0:
            print(f"  [!] {unknown} file(s) in _Unknown folder - manual review needed")
        
        if duplicates > 0:
            print(f"  [i] {duplicates} duplicate(s) detected - moved to _Duplicates/")
        
        print()
        print("📍 Location: " + str(self.output_folder))
        print(f"🕐 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        print("Press Ctrl+C to exit, or wait for auto-refresh...")
        print()


def run_dashboard(refresh_interval=5):
    """Run the monitoring dashboard with auto-refresh."""
    dashboard = MonitoringDashboard()
    
    try:
        while True:
            dashboard.print_dashboard()
            time.sleep(refresh_interval)
    except KeyboardInterrupt:
        print("\n✅ Dashboard closed.")
        exit(0)


if __name__ == "__main__":
    print("Starting Smart File Organizer Dashboard...")
    print("(This will refresh every 5 seconds)")
    print()
    run_dashboard(refresh_interval=5)
