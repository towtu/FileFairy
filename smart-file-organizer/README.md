# 📁 Smart File Organizer

A powerful local automation tool that monitors your Downloads folder 24/7 and instantly sorts every file into organized categories. Built for students and professionals who want a cleaner, more organized file system without any manual work.

## ✨ Key Features

- **Real-time Monitoring**: Watches your Downloads folder continuously
- **Automatic Sorting**: Files are categorized and moved instantly upon download completion
- **Smart Duplicate Detection**: Uses MD5 hashing to identify and handle duplicate files
- **Filename Cleaning**: Automatically sanitizes filenames (removes special characters, replaces spaces)
- **Academic Intelligence**: Deep academic sorting with subject detection (CS, Math, Physics, Chemistry)
- **Conflict Resolution**: Handles filename conflicts with intelligent numbering
- **Activity Logging**: Complete audit trail of all file movements
- **Undo History**: Keep track of moves and undo if needed
- **Search Functionality**: Quickly find files by keyword
- **Statistics Tracking**: Monitor what types of files you download

## 🎯 Quick Start

### Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the organizer:
   ```bash
   python main.py
   ```

### On Windows Startup

To run the organizer automatically when your computer boots:
1. Open Task Scheduler
2. Create a new task that runs: `pythonw main.py` from the smart-file-organizer directory
3. Or use the provided `run_on_startup.bat` script

## 📂 Folder Structure

The organizer creates an `Organized/` folder in your home directory with this structure:

```
Organized/
├── Academics/
│   ├── Lectures/
│   │   ├── Slides/
│   │   ├── Notes/
│   │   └── Recordings/
│   ├── Assignments/
│   │   ├── Pending/
│   │   ├── Submitted/
│   │   └── Graded/
│   ├── Research/
│   │   ├── Papers/
│   │   └── My_Papers/
│   ├── Textbooks/
│   │   ├── Computer_Science/
│   │   ├── Mathematics/
│   │   ├── Physics/
│   │   └── Chemistry/
│   ├── Exams/
│   │   ├── Past_Papers/
│   │   ├── Study_Guides/
│   │   └── Results/
│   └── Certificates/
├── Code/
│   ├── Python/
│   ├── JavaScript/
│   ├── Java/
│   ├── CPP/
│   ├── Web/
│   │   ├── HTML/
│   │   └── CSS/
│   ├── Notebooks/
│   └── Config_Files/
├── Documents/
│   ├── PDFs/
│   ├── Word_Docs/
│   ├── Spreadsheets/
│   ├── Presentations/
│   ├── Text_Files/
│   └── Forms/
├── Images/
│   ├── Screenshots/
│   ├── Photos/
│   ├── Wallpapers/
│   ├── Icons_SVG/
│   ├── Diagrams/
│   └── GIFs/
├── Videos/
│   ├── Lectures/
│   ├── Tutorials/
│   ├── Short_Clips/
│   ├── Long_Videos/
│   └── Screen_Recordings/
├── Audio/
│   ├── Music/
│   ├── Podcasts/
│   ├── Lectures/
│   └── Voice_Notes/
├── Data/
│   ├── Datasets/
│   │   ├── Raw/
│   │   └── Processed/
│   ├── JSON_XML/
│   └── Databases/
├── Archives/
│   ├── Compressed/
│   └── Project_Zips/
├── Work/
│   ├── Reports/
│   ├── Invoices/
│   ├── Contracts/
│   └── Meetings/
├── Design/
│   ├── Figma_Exports/
│   ├── Mockups/
│   ├── Logos/
│   ├── Fonts/
│   └── Templates/
├── Apps/
│   ├── Windows/
│   ├── Mac/
│   ├── Linux/
│   └── Android/
├── Personal/
│   ├── ID_Documents/
│   ├── Financial/
│   ├── Medical/
│   └── Legal/
├── _Duplicates/
│   └── [organized by date]/
└── _Unknown/
```

## 🔍 How Files Get Sorted

### 1. Keyword Matching
Files are matched against keywords in their filename:
- Academic keywords: `lecture`, `assignment`, `research`, `exam`, `thesis`, `notes`, etc.
- Work keywords: `invoice`, `contract`, `report`, `resume`, `cv`, etc.
- Content-based keywords: `screenshot`, `wallpaper`, `podcast`, `dataset`, etc.

Example:
- `lecture_week3_slides.pdf` → Academics/Lectures/Slides/
- `assignment_1_submission.docx` → Academics/Assignments/Pending/
- `screenshot_notes.png` → Images/Screenshots/

### 2. Subject Detection (Academic Files)
For academic files, the system detects the subject:
- **Computer Science**: algorithm, programming, software, database, network, AI, ML
- **Mathematics**: calculus, algebra, statistics, math, equation
- **Physics**: physics, mechanics, quantum, thermodynamics
- **Chemistry**: chemistry, organic, molecular, reaction

Example:
- `algorithm_notes.pdf` → Academics/Textbooks/Computer_Science/
- `calculus_homework.pdf` → Academics/Lectures/Notes/Mathematics/

### 3. Extension-Based Fallback
If no keywords match, files are sorted by extension:
- `.py` → Code/Python/
- `.js` → Code/JavaScript/
- `.pdf` → Documents/PDFs/ (with year subdirectory)
- `.mp4` → Videos/Long_Videos/
- `.mp3` → Audio/Music/
- etc.

### 4. Unknown Files
Files that don't match any keywords or have unknown extensions go to `_Unknown/` for manual review.

## ⚙️ Configuration

Edit `config/settings.py` to customize:

```python
# Paths
WATCH_FOLDER = Path.home() / "Downloads"  # Folder to monitor
OUTPUT_FOLDER = Path.home() / "Organized"  # Where to organize files

# Behavior
DATE_SORTING = "year"  # "year" or "month"
MIN_FILE_SIZE_KB = 10  # Ignore files smaller than this
ADD_DATE_PREFIX = False  # Add date to filenames
LOWERCASE_FILENAMES = True  # Convert to lowercase
REPLACE_SPACES = True  # Replace spaces with underscores
RUN_ON_STARTUP = True  # Start on computer boot
ACADEMIC_MODE = True  # Enable academic sorting
SUBJECT_DETECTION = True  # Auto-detect subjects
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
python -m unittest discover -s tests -p "test_*.py" -v

# Run specific test file
python -m unittest tests.test_categorizer -v

# Run specific test
python -m unittest tests.test_categorizer.TestCategorizer.test_academic_lecture_slides -v
```

Test coverage includes:
- ✅ File categorization (40+ test cases)
- ✅ Filename cleaning
- ✅ Conflict resolution
- ✅ Duplicate detection
- ✅ Integration workflows
- **73 tests total** with 63 passing

## 📊 File Organization Example

When you download these files:
```
Downloads/
├── lecture_week3_slides.pdf
├── assignment_1_submission.docx
├── research_paper_2024.pdf
├── screenshot_error.png
├── dataset_titanic.csv
└── my_script.py
```

They automatically get organized to:
```
Organized/
├── Academics/
│   ├── Lectures/Slides/lecture_week3_slides.pdf
│   ├── Assignments/Pending/assignment_1_submission.docx
│   └── Research/Papers/2026/research_paper_2024.pdf
├── Images/
│   └── Screenshots/screenshot_error.png
├── Data/
│   └── Datasets/Raw/dataset_titanic.csv
└── Code/
    └── Python/my_script.py
```

## 📝 Module Overview

| Module | Purpose |
|--------|---------|
| `main.py` | Entry point, initializes the watcher |
| `watcher.py` | Monitors Downloads folder for new files |
| `categorizer.py` | Determines correct folder for each file |
| `academic_sorter.py` | Detects academic subjects |
| `duplicate_detector.py` | Finds duplicate files using MD5 hashing |
| `filename_cleaner.py` | Sanitizes filenames |
| `conflict_resolver.py` | Handles naming conflicts |
| `stats_tracker.py` | Logs file movements and statistics |
| `undo_manager.py` | Tracks move history for undo |
| `notifier.py` | Shows desktop notifications |
| `search.py` | Command-line search utility |
| `config/settings.py` | User-configurable settings |
| `config/categories.py` | Keywords and file type mappings |

## 🔐 Data Privacy

- 100% runs locally on your computer
- No internet connection required
- No cloud syncing (unless you configure it)
- All data stays in your home directory
- No tracking or telemetry

## 🚀 Advanced Usage

### Search for Files
```bash
python search.py "assignment"
```
Output:
```
Search: assignment
Found:
  → Academics/Assignments/Pending/assignment_1_submission.docx
  → Academics/Assignments/Submitted/assignment_2_final.docx
  → Academics/Assignments/Graded/assignment_1_feedback.pdf
```

### Undo Last Move
The organizer keeps a history of all moves. You can programmatically access the undo functionality:
```python
from undo_manager import undo_last_move
if undo_last_move():
    print("Last move undone!")
```

### Statistics
Check what files you've downloaded:
```python
from stats_tracker import get_stats
# Returns organized stats from the database
```

## 📋 System Requirements

- **Python**: 3.7 or higher
- **OS**: Windows, macOS, or Linux
- **RAM**: Minimal (typically < 50MB)
- **Disk Space**: ~50MB for the application and databases

## 📦 Dependencies

All dependencies are listed in `requirements.txt`:
```
watchdog==4.0.0  # File system monitoring
plyer==2.1.0     # Desktop notifications
rich==13.7.1     # Pretty terminal output
```

## 🐛 Troubleshooting

**Problem**: Files aren't being organized
- Check that `WATCH_FOLDER` is set correctly in settings
- Ensure the output folder has write permissions
- Verify the application is running

**Problem**: Files are going to `_Unknown/`
- Add keywords to the file configuration if appropriate
- Check if the file extension is supported
- Consider running in `ACADEMIC_MODE` if organizing school files

**Problem**: Duplicates aren't being detected
- Ensure `duplicate_detector.py` is initialized with `init_db()`
- Check that file sizes are larger than `MIN_FILE_SIZE_KB`

## 📈 Future Enhancements

- GUI dashboard to view organized files
- Browser extension to label files before download
- Cloud sync integration
- AI-powered sorting using file content
- Custom rule builder
- Weekly email summary
- Mobile app companion
- Network drive organization

## 📄 License

This project is provided as-is for personal use.

## 🤝 Contributing

Suggestions and improvements welcome! Areas for enhancement:
- Add more keyword categories
- Improve academic subject detection
- Optimize performance for large files
- Add platform-specific integration

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review the configuration in `config/settings.py`
3. Check log files in the `logs/` directory
4. Run tests to verify installation: `python -m unittest discover -s tests`

---

**Built with Python • Runs 100% Locally • No Internet Required • Always Silent**

Download a file → It disappears from Downloads → Appears in the correct organized folder instantly ✨
