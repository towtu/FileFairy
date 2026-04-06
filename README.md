# FileFairy

AI-powered file organizer that monitors your Downloads folder and automatically sorts files using Google Gemini. Falls back to rule-based categorization when AI is unavailable.

## Features

- **AI Categorization** -- Gemini 2.5 Flash analyzes filenames to determine the best folder, cached locally to minimize API calls
- **Real-time Monitoring** -- Watchdog-based file system listener organizes files seconds after download
- **Duplicate Detection** -- MD5 hashing identifies identical files and moves them to a dedicated folder
- **Academic Mode** -- Specialized sorting for lectures, assignments, research papers, and exams with subject detection
- **GUI Dashboard** -- Dark-themed monitoring interface with live stats, category breakdown, and human-readable activity feed
- **Filename Cleaning** -- Normalizes filenames by removing special characters and standardizing formatting
- **Undo Support** -- Revert any file move operation
- **Auto-Startup** -- Runs silently on Windows boot via startup batch script

## Setup

```bash
git clone https://github.com/towtu/FileFairy.git
cd FileFairy/smart-file-organizer
pip install -r requirements.txt
```

Get a free Gemini API key at https://aistudio.google.com/apikey, then create a `.env` file:

```
GEMINI_API_KEY=your_key_here
```

## Usage

Start the organizer:
```bash
python main.py
```

Open the GUI dashboard:
```bash
python gui_dashboard.py
```

Search for files:
```bash
python search.py "lecture"
```

Run tests:
```bash
python -m unittest discover -s tests
```

## How It Works

```
New file in Downloads
    |
    v
Watchdog detects file --> Wait for download to complete
    |
    v
Check for duplicates (MD5) --> Move to _Duplicates/ if match
    |
    v
Clean filename --> Ask Gemini AI for category
    |                    |
    | (AI unavailable)   | (AI responds)
    v                    v
Rule-based fallback   Use AI result (high/medium confidence only)
    |                    |
    v                    v
Move file to Organized/<Category>/
    |
    v
Cache result + Log action + Send notification
```

## Folder Structure

```
Downloads/Organized/
  Academics/    Lectures, Assignments, Research, Exams, Textbooks
  Code/         Python, JavaScript, Java, CPP, Web, Config
  Documents/    PDFs, Word, Spreadsheets, Presentations, Text
  Images/       Photos, Screenshots, Wallpapers, Diagrams
  Videos/       Lectures, Tutorials, Screen Recordings, Clips
  Audio/        Music, Podcasts, Voice Notes
  Data/         Datasets, JSON/XML, Databases
  Work/         Invoices, Contracts, Reports, Meetings
  Archives/     Compressed files
  Apps/         Installers by platform
  Design/       Mockups, Fonts, Logos
  _Duplicates/  Identical files (by MD5)
  _Unknown/     Unrecognized file types
```

## Auto-Startup

1. Press `Win`, type `shell:startup`, press Enter
2. Copy `smart-file-organizer/run_on_startup.bat` into that folder
3. Restart your computer

## Configuration

Edit `smart-file-organizer/config/settings.py`:

| Setting | Default | Description |
|---|---|---|
| `AI_ENABLED` | `True` | Use Gemini AI for categorization |
| `ACADEMIC_MODE` | `True` | Enable academic sub-categories |
| `MIN_FILE_SIZE_KB` | `10` | Ignore files smaller than this |
| `DATE_SORTING` | `"year"` | Sort PDFs/research by year or month |

## Architecture

| File | Role |
|---|---|
| `main.py` | Entry point, starts watchdog observer |
| `ai_categorizer.py` | Gemini AI integration, caching, rate limit handling |
| `watcher.py` | File system event handler |
| `categorizer.py` | AI-first categorization with rule-based fallback |
| `config/categories.py` | Extension maps and keyword dictionaries |
| `gui_dashboard.py` | Real-time GUI monitoring dashboard |
| `duplicate_detector.py` | MD5 duplicate detection |
| `filename_cleaner.py` | Filename normalization |
| `stats_tracker.py` | SQLite activity logging |
| `undo_manager.py` | Move reversal |

## Requirements

- Windows 7+
- Python 3.8+
- Free Gemini API key (optional, falls back to rules without it)
