"""
GUI Dashboard for Smart File Organizer
Beautiful graphical interface to monitor file organization
"""

import tkinter as tk
from tkinter import ttk
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from config.settings import STATS_DB, OUTPUT_FOLDER
import threading
import os
import subprocess

class GUIDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart File Organizer - Dashboard")
        self.root.geometry("1200x800")
        self.root.state('zoomed')  # Start maximized
        self.root.resizable(True, True)
        
        # Set color scheme
        self.bg_color = "#f5f5f5"
        self.header_color = "#2c3e50"
        self.accent_color = "#3498db"
        self.success_color = "#27ae60"
        self.warning_color = "#e74c3c"
        self.card_bg = "#ffffff"
        
        self.root.configure(bg=self.bg_color)
        
        # Configure styles
        self.setup_styles()
        
        # Create UI
        self.create_header()
        self.create_main_content()
        
        # Start update loop in background thread
        self.is_running = True
        self.update_thread = threading.Thread(target=self.background_update, daemon=True)
        self.update_thread.start()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_styles(self):
        """Setup ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Header.TLabel', font=('Arial', 16, 'bold'), background=self.header_color, foreground='white')
        style.configure('Title.TLabel', font=('Arial', 14, 'bold'), background=self.bg_color)
        style.configure('Normal.TLabel', font=('Arial', 10), background=self.bg_color)
    
    def create_header(self):
        """Create header with title"""
        header = tk.Frame(self.root, bg=self.header_color, height=100)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        title = tk.Label(
            header, 
            text="📊 Smart File Organizer Dashboard",
            font=("Arial", 28, "bold"),
            bg=self.header_color,
            fg="white"
        )
        title.pack(pady=20)
        
        subtitle = tk.Label(
            header,
            text="Real-time File Organization Monitoring",
            font=("Arial", 12),
            bg=self.header_color,
            fg="#ecf0f1"
        )
        subtitle.pack()
    
    def create_main_content(self):
        """Create main content area"""
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Top row - Statistics
        self.create_stats_section(main_frame)
        
        # Middle row - Categories and Activity
        middle_frame = tk.Frame(main_frame, bg=self.bg_color)
        middle_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.create_categories_section(middle_frame)
        self.create_activity_section(middle_frame)
        
        # Bottom row - Controls
        self.create_control_section(main_frame)
    
    def create_stats_section(self, parent):
        """Create statistics display"""
        stats_frame = tk.Frame(parent, bg=self.bg_color)
        stats_frame.pack(fill=tk.X, pady=10)
        
        self.stat_boxes = {}
        stats = [
            ("Total Organized", "total", "📁", self.success_color),
            ("Today", "today", "📅", self.accent_color),
            ("Duplicates", "duplicates", "🔄", self.warning_color),
            ("Unknown", "unknown", "❓", "#95a5a6")
        ]
        
        for label, key, emoji, color in stats:
            box = tk.Frame(stats_frame, bg=self.card_bg, relief=tk.FLAT, bd=0)
            box.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.BOTH, ipady=20)
            
            # Shadow effect
            shadow = tk.Frame(box, bg="#ddd", height=2)
            shadow.pack(side=tk.BOTTOM, fill=tk.X)
            
            # Content
            content = tk.Frame(box, bg=self.card_bg)
            content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
            
            emoji_label = tk.Label(content, text=emoji, font=("Arial", 32), bg=self.card_bg)
            emoji_label.pack()
            
            title = tk.Label(content, text=label, font=("Arial", 11), bg=self.card_bg, fg="#7f8c8d")
            title.pack(pady=5)
            
            value = tk.Label(content, text="0", font=("Arial", 24, "bold"), bg=self.card_bg, fg=color)
            value.pack(pady=5)
            
            self.stat_boxes[key] = value
    
    def create_categories_section(self, parent):
        """Create category breakdown section"""
        cat_frame = tk.Frame(parent, bg=self.card_bg, relief=tk.FLAT, bd=0)
        cat_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        title = tk.Label(cat_frame, text="📁 Category Breakdown", font=("Arial", 12, "bold"), bg=self.card_bg, fg=self.header_color)
        title.pack(anchor="w", padx=15, pady=12)
        
        # Canvas with scrollbar
        canvas_frame = tk.Frame(cat_frame, bg=self.card_bg)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        canvas = tk.Canvas(canvas_frame, bg=self.card_bg, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.card_bg)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self.categories_frame = scrollable_frame
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_activity_section(self, parent):
        """Create recent activity section"""
        activity_frame = tk.Frame(parent, bg=self.card_bg, relief=tk.FLAT, bd=0)
        activity_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        title = tk.Label(activity_frame, text="📝 Recent Activity", font=("Arial", 12, "bold"), bg=self.card_bg, fg=self.header_color)
        title.pack(anchor="w", padx=15, pady=12)
        
        # Canvas with scrollbar
        canvas_frame = tk.Frame(activity_frame, bg=self.card_bg)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        canvas = tk.Canvas(canvas_frame, bg=self.card_bg, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.card_bg)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self.activity_frame = scrollable_frame
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_control_section(self, parent):
        """Create control buttons"""
        button_frame = tk.Frame(parent, bg=self.bg_color)
        button_frame.pack(fill=tk.X, pady=15)
        
        refresh_btn = tk.Button(
            button_frame,
            text="🔄 Refresh Now",
            command=self.manual_update,
            bg=self.accent_color,
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=12,
            relief=tk.FLAT,
            cursor="hand2",
            activebackground="#2980b9"
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        open_btn = tk.Button(
            button_frame,
            text="📂 Open Folder",
            command=self.open_organized_folder,
            bg=self.success_color,
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=12,
            relief=tk.FLAT,
            cursor="hand2",
            activebackground="#229954"
        )
        open_btn.pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = tk.Label(
            button_frame, 
            text="⚫ Updating in real-time... (Last update: Just now)",
            font=("Arial", 10),
            bg=self.bg_color,
            fg="#27ae60"
        )
        self.status_label.pack(side=tk.RIGHT, padx=20)
    
    def get_total_organized(self):
        """Get total files organized"""
        if not STATS_DB.exists():
            return 0
        try:
            conn = sqlite3.connect(STATS_DB)
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM stats WHERE action='MOVED'")
            count = c.fetchone()[0]
            conn.close()
            return count
        except:
            return 0
    
    def get_today_count(self):
        """Get files organized today"""
        if not STATS_DB.exists():
            return 0
        try:
            conn = sqlite3.connect(STATS_DB)
            c = conn.cursor()
            today = datetime.now().strftime("%Y-%m-%d")
            c.execute("SELECT COUNT(*) FROM stats WHERE action='MOVED' AND timestamp LIKE ?", (f"{today}%",))
            count = c.fetchone()[0]
            conn.close()
            return count
        except:
            return 0
    
    def get_duplicates(self):
        """Get duplicate count"""
        if not OUTPUT_FOLDER.exists():
            return 0
        dup_folder = OUTPUT_FOLDER / "_Duplicates"
        if not dup_folder.exists():
            return 0
        try:
            return len(list(dup_folder.rglob("*")))
        except:
            return 0
    
    def get_unknown(self):
        """Get unknown files count"""
        if not OUTPUT_FOLDER.exists():
            return 0
        unknown_folder = OUTPUT_FOLDER / "_Unknown"
        if not unknown_folder.exists():
            return 0
        try:
            return len(list(unknown_folder.glob("*")))
        except:
            return 0
    
    def get_categories(self):
        """Get category breakdown"""
        if not OUTPUT_FOLDER.exists():
            return {}
        
        categories = {}
        try:
            for folder in OUTPUT_FOLDER.iterdir():
                if folder.is_dir() and not folder.name.startswith("_"):
                    count = len(list(folder.rglob("*")))
                    if count > 0:
                        categories[folder.name] = count
        except:
            pass
        
        return dict(sorted(categories.items(), key=lambda x: x[1], reverse=True)[:8])
    
    def get_recent_activity(self):
        """Get recent file movements"""
        if not STATS_DB.exists():
            return []
        try:
            conn = sqlite3.connect(STATS_DB)
            c = conn.cursor()
            c.execute("SELECT filename, destination, timestamp FROM stats WHERE action='MOVED' ORDER BY timestamp DESC LIMIT 15")
            results = c.fetchall()
            conn.close()
            return results
        except:
            return []
    
    def manual_update(self):
        """Manually update dashboard"""
        self.update_display()
        self.status_label.config(text="⚫ Updated! (Updating every 5 seconds)")
    
    def background_update(self):
        """Background thread for updates"""
        while self.is_running:
            try:
                self.root.after(0, self.update_display)
                threading.Event().wait(5)  # Wait 5 seconds
            except:
                pass
    
    def update_display(self):
        """Update all dashboard displays"""
        try:
            # Update stats
            total = self.get_total_organized()
            today = self.get_today_count()
            duplicates = self.get_duplicates()
            unknown = self.get_unknown()
            
            self.stat_boxes["total"].config(text=str(total))
            self.stat_boxes["today"].config(text=str(today))
            self.stat_boxes["duplicates"].config(text=str(duplicates))
            self.stat_boxes["unknown"].config(text=str(unknown))
            
            # Update categories
            self.update_categories()
            
            # Update activity
            self.update_activity()
            
            # Update status
            now = datetime.now().strftime("%H:%M:%S")
            self.status_label.config(text=f"🟢 Real-time monitoring active (Last update: {now})")
        except:
            pass
    
    def update_categories(self):
        """Update category display"""
        # Clear existing
        for widget in self.categories_frame.winfo_children():
            widget.destroy()
        
        categories = self.get_categories()
        total = sum(categories.values())
        
        if not categories:
            label = tk.Label(self.categories_frame, text="No files organized yet", bg=self.card_bg, fg="#95a5a6", font=("Arial", 10))
            label.pack(pady=30)
            return
        
        for cat, count in categories.items():
            percentage = (count / total * 100) if total > 0 else 0
            
            row = tk.Frame(self.categories_frame, bg=self.card_bg)
            row.pack(fill=tk.X, pady=8, padx=10)
            
            # Name
            name = tk.Label(row, text=f"📁 {cat}", font=("Arial", 10, "bold"), bg=self.card_bg, fg=self.header_color, width=20, anchor="w")
            name.pack(side=tk.LEFT)
            
            # Progress bar
            bar_container = tk.Frame(row, bg="#ecf0f1", height=24, relief=tk.FLAT, bd=1)
            bar_container.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
            bar_container.pack_propagate(False)
            
            bar = tk.Frame(bar_container, bg=self.accent_color, height=24)
            bar.pack(side=tk.LEFT, fill=tk.Y)
            bar.pack_propagate(False)
            bar.pack_configure(expand=False)
            
            # Set width based on percentage (this is approximate)
            bar.config(width=int(percentage * 2) if percentage > 2 else 0)
            
            # Count
            count_label = tk.Label(row, text=f"{count} ({percentage:.0f}%)", font=("Arial", 9), bg=self.card_bg, fg=self.accent_color, width=15, anchor="e")
            count_label.pack(side=tk.RIGHT)
    
    def update_activity(self):
        """Update activity display"""
        # Clear existing
        for widget in self.activity_frame.winfo_children():
            widget.destroy()
        
        activity = self.get_recent_activity()
        
        if not activity:
            label = tk.Label(self.activity_frame, text="No recent activity", bg=self.card_bg, fg="#95a5a6", font=("Arial", 10))
            label.pack(pady=30)
            return
        
        for filename, destination, timestamp in activity:
            row = tk.Frame(self.activity_frame, bg=self.card_bg)
            row.pack(fill=tk.X, pady=6, padx=5)
            
            # Status indicator
            indicator = tk.Label(row, text="✓", font=("Arial", 11, "bold"), bg=self.card_bg, fg=self.success_color, width=3)
            indicator.pack(side=tk.LEFT)
            
            # File info
            info = tk.Label(row, text=f"{filename[:30]}...\n→ {destination[-30:]}", font=("Arial", 9), bg=self.card_bg, fg="#2c3e50", justify=tk.LEFT, anchor="nw")
            info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
            
            # Timestamp
            time_label = tk.Label(row, text=timestamp[11:19], font=("Arial", 8), bg=self.card_bg, fg="#95a5a6", anchor="e")
            time_label.pack(side=tk.RIGHT, padx=5)
    
    def open_organized_folder(self):
        """Open the organized folder"""
        if OUTPUT_FOLDER.exists():
            os.startfile(OUTPUT_FOLDER)
        else:
            tk.messagebox.showwarning("Folder Not Found", "Organized folder doesn't exist yet!")
    
    def on_closing(self):
        """Handle window close"""
        self.is_running = False
        self.root.destroy()


def main():
    root = tk.Tk()
    dashboard = GUIDashboard(root)
    root.mainloop()


if __name__ == "__main__":
    main()
    def __init__(self, root):
        self.root = root
        self.root.title("Smart File Organizer - Dashboard")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Set color scheme
        self.bg_color = "#f0f0f0"
        self.header_color = "#2c3e50"
        self.accent_color = "#3498db"
        self.success_color = "#27ae60"
        self.warning_color = "#e74c3c"
        
        self.root.configure(bg=self.bg_color)
        
        # Create UI
        self.create_header()
        self.create_stats_frame()
        self.create_categories_frame()
        self.create_activity_frame()
        self.create_button_frame()
        
        # Start update loop
        self.update_data()
    
    def create_header(self):
        """Create header with title"""
        header = tk.Frame(self.root, bg=self.header_color, height=80)
        header.pack(fill=tk.X, padx=0, pady=0)
        
        title = tk.Label(
            header, 
            text="📊 Smart File Organizer",
            font=("Arial", 24, "bold"),
            bg=self.header_color,
            fg="white"
        )
        title.pack(pady=15)
        
        subtitle = tk.Label(
            header,
            text="Real-time File Organization Dashboard",
            font=("Arial", 10),
            bg=self.header_color,
            fg="#ecf0f1"
        )
        subtitle.pack()
    
    def create_stats_frame(self):
        """Create statistics display"""
        stats_frame = tk.Frame(self.root, bg=self.bg_color)
        stats_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Create 4 stat boxes
        self.stat_boxes = {}
        
        stats = [
            ("Total Organized", "total", "📁"),
            ("Today", "today", "📅"),
            ("Duplicates", "duplicates", "🔄"),
            ("Unknown", "unknown", "❓")
        ]
        
        for label, key, emoji in stats:
            box = tk.Frame(stats_frame, bg="white", relief=tk.RIDGE, bd=2)
            box.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.BOTH)
            
            emoji_label = tk.Label(box, text=emoji, font=("Arial", 24), bg="white")
            emoji_label.pack(pady=5)
            
            title = tk.Label(box, text=label, font=("Arial", 10), bg="white", fg="#7f8c8d")
            title.pack()
            
            value = tk.Label(box, text="0", font=("Arial", 20, "bold"), bg="white", fg=self.accent_color)
            value.pack(pady=10)
            
            self.stat_boxes[key] = value
    
    def create_categories_frame(self):
        """Create category breakdown"""
        cat_frame = tk.LabelFrame(self.root, text="📁 Top Categories", font=("Arial", 12, "bold"), bg=self.bg_color, padx=20, pady=15)
        cat_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Canvas for scrolling
        canvas = tk.Canvas(cat_frame, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(cat_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self.categories_frame = scrollable_frame
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_activity_frame(self):
        """Create recent activity"""
        activity_frame = tk.LabelFrame(self.root, text="📝 Recent Activity", font=("Arial", 12, "bold"), bg=self.bg_color, padx=20, pady=15)
        activity_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Canvas for scrolling
        canvas = tk.Canvas(activity_frame, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(activity_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self.activity_frame = scrollable_frame
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_button_frame(self):
        """Create control buttons"""
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(fill=tk.X, padx=20, pady=15)
        
        refresh_btn = tk.Button(
            button_frame,
            text="🔄 Refresh Now",
            command=self.update_data,
            bg=self.accent_color,
            fg="white",
            font=("Arial", 10),
            padx=15,
            pady=8,
            relief=tk.FLAT,
            cursor="hand2"
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        open_btn = tk.Button(
            button_frame,
            text="📂 Open Organized Folder",
            command=self.open_organized_folder,
            bg=self.success_color,
            fg="white",
            font=("Arial", 10),
            padx=15,
            pady=8,
            relief=tk.FLAT,
            cursor="hand2"
        )
        open_btn.pack(side=tk.LEFT, padx=5)
        
        status_label = tk.Label(button_frame, text="Auto-updating every 5 seconds...", font=("Arial", 9), bg=self.bg_color, fg="#7f8c8d")
        status_label.pack(side=tk.RIGHT)
    
    def get_total_organized(self):
        """Get total files organized"""
        if not STATS_DB.exists():
            return 0
        try:
            conn = sqlite3.connect(STATS_DB)
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM stats WHERE action='MOVED'")
            count = c.fetchone()[0]
            conn.close()
            return count
        except:
            return 0
    
    def get_today_count(self):
        """Get files organized today"""
        if not STATS_DB.exists():
            return 0
        try:
            conn = sqlite3.connect(STATS_DB)
            c = conn.cursor()
            today = datetime.now().strftime("%Y-%m-%d")
            c.execute("SELECT COUNT(*) FROM stats WHERE action='MOVED' AND timestamp LIKE ?", (f"{today}%",))
            count = c.fetchone()[0]
            conn.close()
            return count
        except:
            return 0
    
    def get_duplicates(self):
        """Get duplicate count"""
        if not OUTPUT_FOLDER.exists():
            return 0
        dup_folder = OUTPUT_FOLDER / "_Duplicates"
        if not dup_folder.exists():
            return 0
        return len(list(dup_folder.rglob("*"))) // 2  # Rough estimate
    
    def get_unknown(self):
        """Get unknown files count"""
        if not OUTPUT_FOLDER.exists():
            return 0
        unknown_folder = OUTPUT_FOLDER / "_Unknown"
        if not unknown_folder.exists():
            return 0
        return len(list(unknown_folder.glob("*")))
    
    def get_categories(self):
        """Get category breakdown"""
        if not OUTPUT_FOLDER.exists():
            return {}
        
        categories = {}
        for folder in OUTPUT_FOLDER.iterdir():
            if folder.is_dir() and not folder.name.startswith("_"):
                count = len(list(folder.rglob("*")))
                if count > 0:
                    categories[folder.name] = count
        
        return dict(sorted(categories.items(), key=lambda x: x[1], reverse=True)[:8])
    
    def get_recent_activity(self):
        """Get recent file movements"""
        if not STATS_DB.exists():
            return []
        try:
            conn = sqlite3.connect(STATS_DB)
            c = conn.cursor()
            c.execute("SELECT filename, destination, timestamp FROM stats WHERE action='MOVED' ORDER BY timestamp DESC LIMIT 10")
            results = c.fetchall()
            conn.close()
            return results
        except:
            return []
    
    def update_data(self):
        """Update all dashboard data"""
        # Update stats
        total = self.get_total_organized()
        today = self.get_today_count()
        duplicates = self.get_duplicates()
        unknown = self.get_unknown()
        
        self.stat_boxes["total"].config(text=str(total))
        self.stat_boxes["today"].config(text=str(today))
        self.stat_boxes["duplicates"].config(text=str(duplicates))
        self.stat_boxes["unknown"].config(text=str(unknown))
        
        # Update categories
        self.update_categories()
        
        # Update activity
        self.update_activity()
        
        # Schedule next update
        self.root.after(5000, self.update_data)
    
    def update_categories(self):
        """Update category display"""
        # Clear existing
        for widget in self.categories_frame.winfo_children():
            widget.destroy()
        
        categories = self.get_categories()
        total = sum(categories.values())
        
        if not categories:
            label = tk.Label(self.categories_frame, text="No files organized yet", bg=self.bg_color, fg="#95a5a6")
            label.pack(pady=20)
            return
        
        for cat, count in categories.items():
            percentage = (count / total * 100) if total > 0 else 0
            
            row = tk.Frame(self.categories_frame, bg=self.bg_color)
            row.pack(fill=tk.X, pady=8)
            
            name = tk.Label(row, text=f"📁 {cat}", font=("Arial", 10), bg=self.bg_color, width=20, anchor="w")
            name.pack(side=tk.LEFT)
            
            # Progress bar
            bar = tk.Canvas(row, height=20, bg="white", relief=tk.RIDGE, bd=1)
            bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
            
            bar_width = bar.winfo_width() if bar.winfo_width() > 1 else 200
            fill_width = (percentage / 100) * bar_width
            bar.create_rectangle(0, 0, fill_width, 20, fill=self.accent_color, outline="")
            
            count_label = tk.Label(row, text=f"{count} ({percentage:.0f}%)", font=("Arial", 9), bg=self.bg_color, width=12, anchor="e")
            count_label.pack(side=tk.RIGHT)
    
    def update_activity(self):
        """Update activity display"""
        # Clear existing
        for widget in self.activity_frame.winfo_children():
            widget.destroy()
        
        activity = self.get_recent_activity()
        
        if not activity:
            label = tk.Label(self.activity_frame, text="No recent activity", bg=self.bg_color, fg="#95a5a6")
            label.pack(pady=20)
            return
        
        for filename, destination, timestamp in activity:
            row = tk.Frame(self.activity_frame, bg="white", relief=tk.FLAT, bd=0)
            row.pack(fill=tk.X, pady=5)
            
            # Checkbox indicator
            indicator = tk.Label(row, text="✓", font=("Arial", 12), bg="white", fg=self.success_color, width=3)
            indicator.pack(side=tk.LEFT, padx=10)
            
            # File info
            info_frame = tk.Frame(row, bg="white")
            info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            filename_label = tk.Label(info_frame, text=filename, font=("Arial", 10, "bold"), bg="white", anchor="w")
            filename_label.pack(anchor="w")
            
            dest_label = tk.Label(info_frame, text=f"→ {destination}", font=("Arial", 9), bg="white", fg="#7f8c8d", anchor="w")
            dest_label.pack(anchor="w")
            
            # Timestamp
            time_label = tk.Label(row, text=timestamp[:16], font=("Arial", 9), bg="white", fg="#95a5a6", width=20, anchor="e")
            time_label.pack(side=tk.RIGHT, padx=10)
    
    def open_organized_folder(self):
        """Open the organized folder"""
        if OUTPUT_FOLDER.exists():
            os.startfile(OUTPUT_FOLDER)
        else:
            tk.messagebox.showwarning("Folder Not Found", "Organized folder doesn't exist yet. Download some files to organize them!")


def main():
    root = tk.Tk()
    dashboard = GUIDashboard(root)
    root.mainloop()


if __name__ == "__main__":
    main()
