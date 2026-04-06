"""
FileFairy Dashboard - Real-time monitoring GUI for the AI file organizer.
"""

import tkinter as tk
from tkinter import ttk, font as tkfont
import sqlite3
from pathlib import Path
from datetime import datetime
from config.settings import STATS_DB, OUTPUT_FOLDER, AI_ENABLED
import threading
import os
import subprocess


# -- Color palette --
BG = "#0f0f0f"
SURFACE = "#1a1a2e"
SURFACE_LIGHT = "#222244"
ACCENT = "#6c63ff"
ACCENT_DIM = "#4a42cc"
GREEN = "#00e676"
YELLOW = "#ffca28"
RED = "#ff5252"
TEXT = "#e0e0e0"
TEXT_DIM = "#888899"
TEXT_BRIGHT = "#ffffff"
BORDER = "#2a2a4a"

CATEGORY_COLORS = {
    "Academics": "#6c63ff",
    "Code": "#00e676",
    "Documents": "#29b6f6",
    "Images": "#ff7043",
    "Videos": "#ab47bc",
    "Audio": "#ffca28",
    "Data": "#26a69a",
    "Work": "#ef5350",
    "Archives": "#78909c",
    "Apps": "#8d6e63",
    "Design": "#ec407a",
    "Personal": "#5c6bc0",
}


class FileFairyDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("FileFairy Dashboard")
        self.root.geometry("1100x750")
        self.root.minsize(900, 600)
        self.root.configure(bg=BG)

        try:
            self.root.state("zoomed")
        except tk.TclError:
            pass

        self.is_running = True
        self._build_ui()

        self.update_thread = threading.Thread(target=self._bg_update, daemon=True)
        self.update_thread.start()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    # ------------------------------------------------------------------ UI
    def _build_ui(self):
        # Header
        header = tk.Frame(self.root, bg=SURFACE, height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        title = tk.Label(
            header, text="FileFairy", font=("Segoe UI", 22, "bold"),
            bg=SURFACE, fg=TEXT_BRIGHT,
        )
        title.pack(side=tk.LEFT, padx=24, pady=16)

        self.ai_badge = tk.Label(
            header, text="  AI ACTIVE  " if AI_ENABLED else "  RULES ONLY  ",
            font=("Segoe UI", 9, "bold"),
            bg=GREEN if AI_ENABLED else YELLOW,
            fg="#000000", padx=8, pady=2,
        )
        self.ai_badge.pack(side=tk.LEFT, pady=22)

        self.clock_label = tk.Label(
            header, text="", font=("Segoe UI", 10),
            bg=SURFACE, fg=TEXT_DIM,
        )
        self.clock_label.pack(side=tk.RIGHT, padx=24)

        # Body
        body = tk.Frame(self.root, bg=BG)
        body.pack(fill=tk.BOTH, expand=True, padx=20, pady=14)

        # -- Stat cards row --
        self.stat_cards = {}
        cards_row = tk.Frame(body, bg=BG)
        cards_row.pack(fill=tk.X, pady=(0, 14))

        card_defs = [
            ("total", "Total Organized", "0", ACCENT),
            ("today", "Today", "0", GREEN),
            ("duplicates", "Duplicates", "0", YELLOW),
            ("unknown", "Needs Review", "0", RED),
        ]
        for key, label, default, color in card_defs:
            self.stat_cards[key] = self._make_card(cards_row, label, default, color)

        # -- Middle: categories + activity side by side --
        mid = tk.Frame(body, bg=BG)
        mid.pack(fill=tk.BOTH, expand=True)
        mid.columnconfigure(0, weight=2)
        mid.columnconfigure(1, weight=3)
        mid.rowconfigure(0, weight=1)

        self._build_categories_panel(mid)
        self._build_activity_panel(mid)

        # -- Bottom bar --
        bottom = tk.Frame(self.root, bg=SURFACE, height=50)
        bottom.pack(fill=tk.X, side=tk.BOTTOM)
        bottom.pack_propagate(False)

        btn_style = dict(
            font=("Segoe UI", 10, "bold"), fg=TEXT_BRIGHT,
            relief=tk.FLAT, cursor="hand2", padx=16, pady=6,
            activeforeground=TEXT_BRIGHT, bd=0,
        )

        open_btn = tk.Button(
            bottom, text="Open Folder", bg=ACCENT, activebackground=ACCENT_DIM,
            command=self._open_folder, **btn_style,
        )
        open_btn.pack(side=tk.LEFT, padx=16, pady=10)

        refresh_btn = tk.Button(
            bottom, text="Refresh", bg=SURFACE_LIGHT, activebackground=BORDER,
            command=self._refresh, **btn_style,
        )
        refresh_btn.pack(side=tk.LEFT, pady=10)

        self.status_label = tk.Label(
            bottom, text="", font=("Segoe UI", 9), bg=SURFACE, fg=TEXT_DIM,
        )
        self.status_label.pack(side=tk.RIGHT, padx=20)

    # -- Card widget --
    def _make_card(self, parent, label, default, color):
        card = tk.Frame(parent, bg=SURFACE, highlightbackground=BORDER, highlightthickness=1)
        card.pack(side=tk.LEFT, padx=6, expand=True, fill=tk.BOTH, ipady=10)

        accent_bar = tk.Frame(card, bg=color, height=3)
        accent_bar.pack(fill=tk.X, side=tk.TOP)

        tk.Label(
            card, text=label, font=("Segoe UI", 10), bg=SURFACE, fg=TEXT_DIM,
        ).pack(pady=(12, 2))

        val = tk.Label(
            card, text=default, font=("Segoe UI", 28, "bold"), bg=SURFACE, fg=color,
        )
        val.pack(pady=(0, 10))
        return val

    # -- Categories panel --
    def _build_categories_panel(self, parent):
        panel = tk.Frame(parent, bg=SURFACE, highlightbackground=BORDER, highlightthickness=1)
        panel.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=0)

        tk.Label(
            panel, text="Categories", font=("Segoe UI", 13, "bold"),
            bg=SURFACE, fg=TEXT_BRIGHT, anchor="w",
        ).pack(fill=tk.X, padx=16, pady=(14, 8))

        container = tk.Frame(panel, bg=SURFACE)
        container.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 14))

        canvas = tk.Canvas(container, bg=SURFACE, highlightthickness=0, bd=0)
        scroll = tk.Frame(canvas, bg=SURFACE)

        scroll.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll, anchor="nw")
        canvas.pack(fill=tk.BOTH, expand=True)

        self.cat_frame = scroll
        self.cat_canvas = canvas

    # -- Activity panel --
    def _build_activity_panel(self, parent):
        panel = tk.Frame(parent, bg=SURFACE, highlightbackground=BORDER, highlightthickness=1)
        panel.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=0)

        tk.Label(
            panel, text="Recent Activity", font=("Segoe UI", 13, "bold"),
            bg=SURFACE, fg=TEXT_BRIGHT, anchor="w",
        ).pack(fill=tk.X, padx=16, pady=(14, 8))

        container = tk.Frame(panel, bg=SURFACE)
        container.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 14))

        canvas = tk.Canvas(container, bg=SURFACE, highlightthickness=0, bd=0)
        scroll = tk.Frame(canvas, bg=SURFACE)

        scroll.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll, anchor="nw")
        canvas.pack(fill=tk.BOTH, expand=True)

        self.act_frame = scroll
        self.act_canvas = canvas

    # ------------------------------------------------------------------ DATA
    def _query(self, sql, params=()):
        if not STATS_DB.exists():
            return []
        try:
            conn = sqlite3.connect(str(STATS_DB))
            rows = conn.execute(sql, params).fetchall()
            conn.close()
            return rows
        except Exception:
            return []

    def _count(self, action, today_only=False):
        sql = "SELECT COUNT(*) FROM stats WHERE action=?"
        params = [action]
        if today_only:
            sql += " AND timestamp LIKE ?"
            params.append(f"{datetime.now().strftime('%Y-%m-%d')}%")
        rows = self._query(sql, params)
        return rows[0][0] if rows else 0

    def _get_categories(self):
        if not OUTPUT_FOLDER.exists():
            return {}
        cats = {}
        try:
            for d in OUTPUT_FOLDER.iterdir():
                if d.is_dir() and not d.name.startswith("_"):
                    n = sum(1 for _ in d.rglob("*") if _.is_file())
                    if n:
                        cats[d.name] = n
        except Exception:
            pass
        return dict(sorted(cats.items(), key=lambda x: x[1], reverse=True))

    def _get_activity(self, limit=20):
        return self._query(
            "SELECT timestamp, action, filename, destination FROM stats ORDER BY timestamp DESC LIMIT ?",
            (limit,),
        )

    # ------------------------------------------------------------------ RENDER
    def _refresh(self):
        self._update_display()

    def _update_display(self):
        try:
            total = self._count("MOVED")
            today = self._count("MOVED", today_only=True)
            dupes = self._count("DUPLICATE")
            unknown_dir = OUTPUT_FOLDER / "_Unknown"
            unknown = sum(1 for _ in unknown_dir.rglob("*") if _.is_file()) if unknown_dir.exists() else 0

            self.stat_cards["total"].config(text=f"{total:,}")
            self.stat_cards["today"].config(text=str(today))
            self.stat_cards["duplicates"].config(text=str(dupes))
            self.stat_cards["unknown"].config(text=str(unknown))

            self._render_categories()
            self._render_activity()

            now = datetime.now().strftime("%H:%M:%S")
            self.clock_label.config(text=f"Live  |  {datetime.now().strftime('%b %d, %Y')}")
            self.status_label.config(text=f"Last refresh: {now}  |  Auto-updating every 5s")
        except Exception:
            pass

    def _render_categories(self):
        for w in self.cat_frame.winfo_children():
            w.destroy()

        cats = self._get_categories()
        total = sum(cats.values()) or 1

        if not cats:
            tk.Label(
                self.cat_frame, text="No files organized yet.",
                font=("Segoe UI", 10), bg=SURFACE, fg=TEXT_DIM,
            ).pack(pady=30)
            return

        for name, count in cats.items():
            pct = count / total * 100
            color = CATEGORY_COLORS.get(name, ACCENT)

            row = tk.Frame(self.cat_frame, bg=SURFACE)
            row.pack(fill=tk.X, pady=5)

            tk.Label(
                row, text=name, font=("Segoe UI", 10, "bold"),
                bg=SURFACE, fg=TEXT, width=14, anchor="w",
            ).pack(side=tk.LEFT)

            bar_bg = tk.Frame(row, bg=BORDER, height=14)
            bar_bg.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(8, 8))
            bar_bg.pack_propagate(False)

            bar_fill = tk.Frame(bar_bg, bg=color, height=14)
            bar_fill.place(relwidth=max(pct / 100, 0.02), relheight=1.0)

            tk.Label(
                row, text=f"{count}", font=("Segoe UI", 10, "bold"),
                bg=SURFACE, fg=color, width=5, anchor="e",
            ).pack(side=tk.RIGHT)

    def _render_activity(self):
        for w in self.act_frame.winfo_children():
            w.destroy()

        activity = self._get_activity()
        if not activity:
            tk.Label(
                self.act_frame, text="No activity recorded yet.",
                font=("Segoe UI", 10), bg=SURFACE, fg=TEXT_DIM,
            ).pack(pady=30)
            return

        for timestamp, action, filename, destination in activity:
            # Resolve the full file path for click-to-open
            file_path = self._resolve_path(destination)

            row = tk.Frame(self.act_frame, bg=SURFACE_LIGHT, highlightbackground=BORDER, highlightthickness=1)
            row.pack(fill=tk.X, pady=3, ipady=6)

            # Make the entire row clickable
            self._bind_click(row, file_path)

            # Action badge
            if action == "MOVED":
                badge_text, badge_bg = "ORGANIZED", GREEN
            elif action == "DUPLICATE":
                badge_text, badge_bg = "DUPLICATE", YELLOW
            else:
                badge_text, badge_bg = action, TEXT_DIM

            badge = tk.Label(
                row, text=f" {badge_text} ", font=("Segoe UI", 8, "bold"),
                bg=badge_bg, fg="#000000",
            )
            badge.pack(side=tk.LEFT, padx=(10, 8), pady=4)
            self._bind_click(badge, file_path)

            # File info
            info = tk.Frame(row, bg=SURFACE_LIGHT)
            info.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))
            self._bind_click(info, file_path)

            # Clean filename display
            display_name = filename if len(filename) <= 40 else filename[:37] + "..."
            name_lbl = tk.Label(
                info, text=display_name, font=("Segoe UI", 10, "bold"),
                bg=SURFACE_LIGHT, fg=TEXT_BRIGHT, anchor="w", cursor="hand2",
            )
            name_lbl.pack(anchor="w")
            self._bind_click(name_lbl, file_path)

            # Friendly destination
            friendly = self._friendly_path(destination)
            dest_lbl = tk.Label(
                info, text=friendly, font=("Segoe UI", 9),
                bg=SURFACE_LIGHT, fg=TEXT_DIM, anchor="w", cursor="hand2",
            )
            dest_lbl.pack(anchor="w")
            self._bind_click(dest_lbl, file_path)

            # Time
            time_str = self._friendly_time(timestamp)
            time_lbl = tk.Label(
                row, text=time_str, font=("Segoe UI", 9),
                bg=SURFACE_LIGHT, fg=TEXT_DIM,
            )
            time_lbl.pack(side=tk.RIGHT, padx=12)
            self._bind_click(time_lbl, file_path)

    # ------------------------------------------------------------------ HELPERS
    def _bind_click(self, widget, file_path):
        """Bind click event to open file location in Explorer."""
        hover_bg = "#2d2d52"
        original_bg = widget.cget("bg")

        def on_enter(e):
            try:
                widget.config(bg=hover_bg)
            except Exception:
                pass

        def on_leave(e):
            try:
                widget.config(bg=original_bg)
            except Exception:
                pass

        def on_click(e):
            self._open_file_location(file_path)

        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
        widget.bind("<Button-1>", on_click)
        widget.config(cursor="hand2")

    def _resolve_path(self, destination):
        """Resolve a logged destination string to an absolute file path."""
        dest = destination.replace("/", "\\")

        # If it's already absolute, return as-is
        if Path(dest).is_absolute():
            return Path(dest)

        # Try relative to OUTPUT_FOLDER parent (how watcher logs it)
        candidate = OUTPUT_FOLDER.parent / dest
        if candidate.exists():
            return candidate

        # Try relative to OUTPUT_FOLDER itself
        candidate = OUTPUT_FOLDER / dest
        if candidate.exists():
            return candidate

        return OUTPUT_FOLDER.parent / dest

    @staticmethod
    def _open_file_location(file_path):
        """Open Explorer and select the file, or open its folder."""
        path = Path(file_path)
        try:
            if path.exists():
                # Select the file in Explorer
                subprocess.Popen(f'explorer /select,"{path}"')
            elif path.parent.exists():
                # File gone but folder exists -- open the folder
                os.startfile(str(path.parent))
            else:
                os.startfile(str(OUTPUT_FOLDER))
        except Exception:
            pass

    @staticmethod
    def _friendly_path(raw_dest):
        """Convert raw destination path to a user-friendly label."""
        raw = raw_dest.replace("\\", "/")

        # Strip everything up to and including "Organized/"
        marker = "Organized/"
        idx = raw.find(marker)
        if idx >= 0:
            rel = raw[idx + len(marker):]
        else:
            rel = raw

        parts = [p for p in rel.strip("/").split("/") if p]
        if not parts:
            return raw_dest

        # Build friendly string
        category = parts[0]
        rest = parts[1:]

        # Remove the filename from the path if present (has a dot extension)
        if rest and "." in rest[-1]:
            rest = rest[:-1]

        if rest:
            return f"{category}  >  {' > '.join(rest)}"
        return category

    @staticmethod
    def _friendly_time(timestamp_str):
        """Convert timestamp to relative or short time."""
        try:
            ts = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            now = datetime.now()
            diff = now - ts

            if diff.days == 0:
                secs = diff.seconds
                if secs < 60:
                    return "Just now"
                elif secs < 3600:
                    return f"{secs // 60}m ago"
                else:
                    return f"{secs // 3600}h ago"
            elif diff.days == 1:
                return "Yesterday"
            elif diff.days < 7:
                return f"{diff.days}d ago"
            else:
                return ts.strftime("%b %d")
        except Exception:
            return timestamp_str[:16]

    # ------------------------------------------------------------------ LIFECYCLE
    def _bg_update(self):
        while self.is_running:
            try:
                self.root.after(0, self._update_display)
                threading.Event().wait(5)
            except Exception:
                pass

    def _open_folder(self):
        if OUTPUT_FOLDER.exists():
            os.startfile(OUTPUT_FOLDER)

    def _on_close(self):
        self.is_running = False
        self.root.destroy()


def main():
    root = tk.Tk()
    FileFairyDashboard(root)
    root.mainloop()


if __name__ == "__main__":
    main()
