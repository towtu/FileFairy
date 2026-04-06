# FileFairy

An AI-powered file organization system that automatically monitors your Downloads folder and intelligently categorizes files into organized directory structures. FileFairy uses Google Gemini AI for context-aware file classification, combined with real-time file system monitoring to detect new files, analyze their content and metadata, and organize them into appropriate categories while detecting and managing duplicates.

## Overview

FileFairy is a Python-based AI automation tool designed to eliminate manual file organization. It runs continuously in the background, watching your Downloads folder and automatically sorting incoming files using Google Gemini AI to understand file context beyond simple extension matching. When AI is unavailable, the system gracefully falls back to rule-based categorization using file type, naming conventions, and keyword analysis. The system includes academic-specific organization modes, duplicate detection using MD5 hashing, filename normalization, AI result caching, and real-time statistics tracking.

## Key Features

- **AI-Powered Categorization**: Google Gemini AI analyzes filenames and context to intelligently determine the best category, going beyond simple extension matching
- **Intelligent Fallback**: When AI is unavailable or rate-limited, the system automatically falls back to rule-based categorization with zero downtime
- **AI Result Caching**: Previously categorized files are cached in a local SQLite database to avoid redundant API calls and reduce latency
- **Rate Limit Handling**: Automatic cooldown management when API quotas are reached, with seamless fallback to rule-based classification
- **Real-time Monitoring**: Continuous file system monitoring using watchdog library for immediate file organization upon download completion
- **Intelligent Categorization**: Automatic classification of files into categories including Academics, Code, Documents, Images, Videos, Audio, and Data
- **Duplicate Detection**: MD5-based duplicate file identification and organization into a dedicated duplicates folder
- **Filename Normalization**: Automatic cleaning and standardization of filenames to remove special characters and improve readability
- **Academic Mode**: Specialized organization for academic documents with subcategories for lectures, assignments, and research materials
- **Live Dashboard**: Real-time statistics tracking showing total files organized, daily statistics, category breakdown, and recent activity logs
- **Undo Capability**: Full undo functionality for reverting file organization operations
- **Automatic Startup**: Optional Windows Task Scheduler integration for automatic daemon operation on system boot
- **Search Functionality**: Built-in search tool for locating files by keyword or pattern
- **Activity Logging**: Comprehensive logging of all file operations for audit and troubleshooting purposes

## System Requirements

- Windows 7 or later
- Python 3.8 or higher
- 50 MB free disk space
- Google Gemini API key (free tier available at https://aistudio.google.com/apikey)
- Dependencies listed in requirements.txt

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/towtu/FileFairy.git
cd FileFairy/smart-file-organizer
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs required packages including:
- watchdog: Real-time file system event monitoring
- google-genai: Google Gemini AI SDK for intelligent file categorization
- python-dotenv: Environment variable management for secure API key storage
- SQLite3: Local database for duplicate detection, AI caching, and statistics tracking

### Step 3: Configure the Gemini API Key

1. Visit https://aistudio.google.com/apikey and create a free API key
2. Create a `.env` file in the `smart-file-organizer/` directory:

```bash
cp .env.example .env
```

3. Open the `.env` file and replace the placeholder with your actual API key:

```
GEMINI_API_KEY=your_actual_api_key_here
```

The free tier provides 15 requests per minute and 1,500 requests per day, which is sufficient for typical file organization workloads.

### Step 4: Configuration (Optional)

No additional configuration is required. The system uses default settings targeting your Downloads folder. For custom configuration, edit `config/settings.py`:

```python
WATCH_FOLDER = Path.home() / "Downloads"  # Folder to monitor
OUTPUT_FOLDER = WATCH_FOLDER / "Organized"  # Organization output directory
ACADEMIC_MODE = True  # Enable academic categorization
MIN_FILE_SIZE = 10000  # Minimum file size in bytes (ignores temp files)
```

## Quick Start

### Running the Organizer

Open Command Prompt and execute:

```bash
cd path\to\FileFairy\smart-file-organizer
python main.py
```

Expected output:
```
Starting Smart File Organizer...
Watching: C:\Users\YourUsername\Downloads
Output to: C:\Users\YourUsername\Downloads\Organized
Academic Mode: Enabled
Running in background... (Press Ctrl+C to stop)
```

### Testing the Installation

In a separate Command Prompt window:

```bash
echo test content > C:\Users\YourUsername\Downloads\test_lecture.pdf
```

Wait 5-10 seconds and verify the file appears in:
```
C:\Users\YourUsername\Downloads\Organized\Academics\Lectures\
```

## Directory Structure

FileFairy creates the following organized folder hierarchy:

```
Downloads\Organized\
├── Academics\
│   ├── Lectures\          (PDF files with lecture keywords)
│   ├── Assignments\       (Files with assignment keywords)
│   └── Research\          (Academic research papers)
├── Code\
│   ├── Python\            (.py files)
│   ├── JavaScript\        (.js files)
│   ├── Java\              (.java files)
│   └── ...other languages
├── Documents\             (Word, Excel, text, PDF documents)
├── Images\
│   ├── Photos\            (JPG, PNG, BMP photos)
│   └── Screenshots\       (Screenshot files)
├── Videos\                (MP4, AVI, MKV, WebM)
├── Audio\                 (MP3, WAV, FLAC, podcasts)
├── Data\                  (CSV, JSON, XML, database files)
├── _Duplicates\           (Files with identical MD5 hash)
└── _Unknown\              (Unrecognized file types)
```

## Usage Examples

### File Organization Examples

| Source File | Destination Path |
|---|---|
| lecture_notes.pdf | Academics/Lectures/ |
| assignment_spring_2025.docx | Academics/Assignments/ |
| my_script.py | Code/Python/ |
| photo_vacation.jpg | Images/Photos/ |
| data_analysis.csv | Data/ |
| music_track.mp3 | Audio/ |
| tutorial_video.mp4 | Videos/ |

### Command Reference

Start the organizer in the background:
```bash
python main.py
```

View real-time statistics and activity:
```bash
python dashboard.py
```

Search for files by keyword:
```bash
python search.py "lecture"
```

View complete activity history:
```bash
python history.py
```

View application logs:
```bash
type ..\logs\organizer.log
```

Run automated tests:
```bash
python -m unittest discover -s tests
```

## Automatic Startup Configuration

To enable FileFairy to run automatically when Windows starts:

1. Press Windows key and type `shell:startup` then press Enter
2. Navigate to the FileFairy directory and locate `run_on_startup.bat`
3. Copy `run_on_startup.bat` to the startup folder opened in step 1
4. Restart your computer

After system restart, FileFairy will automatically begin monitoring your Downloads folder.

### Disabling Automatic Startup

1. Press Windows key and type `shell:startup` then press Enter
2. Locate and delete `run_on_startup.bat` from the startup folder
3. The organizer will no longer launch at system startup

## Dashboard Monitoring

Launch the real-time dashboard to monitor organization activity:

```bash
python dashboard.py
```

The dashboard displays:
- Total number of files organized across all sessions
- Files organized during the current session
- Count of duplicate files detected
- Category-wise file distribution
- Live activity log with timestamps
- Auto-refreshes every 5 seconds

Press Ctrl+C to exit the dashboard.

## Troubleshooting

### Issue: Organized folder not appearing in Downloads

**Solution**: Ensure the organizer is running and has processed at least one file. The Organized folder is created when the first file is moved, not during initialization. Wait 30 seconds after starting the organizer and placing a test file in Downloads.

### Issue: Files not being organized

**Diagnosis checklist**:
1. Verify the organizer is running: `python main.py` window should display active monitoring
2. Confirm files are in the correct watch folder: `C:\Users\YourUsername\Downloads\`
3. Check file size: Files under 10 KB are ignored (temporary/incomplete files). Adjust `MIN_FILE_SIZE` in config if needed
4. Allow processing time: The organizer checks for new files every 5-10 seconds after file system event detection

### Issue: Threading or compatibility errors

**Solution**: Ensure watchdog library is properly installed:
```bash
pip install --upgrade watchdog
```

This is required for Python 3.13 compatibility.

### Issue: Duplicate detection not working

**Solution**: The system uses MD5 hashing for duplicate detection. Ensure the `data/` directory has write permissions. Verify database connectivity by checking `logs/organizer.log`.

## How the AI Categorization Works

FileFairy uses a multi-tier categorization strategy:

1. **AI Classification (Primary)**: When enabled and available, each new file is sent to Google Gemini AI with its filename and extension. The AI analyzes contextual clues, abbreviations, and patterns to determine the optimal category with a confidence score.

2. **Cache Lookup**: Before making an API call, the system checks a local SQLite cache. If the same filename has been categorized before, the cached result is returned instantly with no API usage.

3. **Confidence Filtering**: Only "high" and "medium" confidence AI results are accepted. Low-confidence results are discarded and the system falls back to rule-based logic.

4. **Rule-Based Fallback**: If the AI is unavailable (no API key, rate limited, network error), the system uses keyword matching and extension-based rules to categorize files with zero downtime.

5. **Rate Limit Management**: When API quota is exceeded, a 60-second cooldown is activated. During cooldown, all files are categorized using rules. The system automatically resumes AI classification once the cooldown expires.

## Project Architecture

FileFairy is organized into modular components:

- `main.py`: Application entry point and event loop orchestration
- `ai_categorizer.py`: Google Gemini AI integration with caching, rate limiting, and fallback logic
- `watcher.py`: File system event handler and monitoring logic
- `categorizer.py`: File classification engine (AI-first with rule-based fallback)
- `duplicate_detector.py`: MD5-based duplicate identification with database persistence
- `filename_cleaner.py`: Filename normalization and sanitization
- `stats_tracker.py`: Statistics accumulation and persistence
- `undo_manager.py`: Operation reversal and history management
- `dashboard.py`: Real-time statistics display interface
- `search.py`: File search functionality
- `config/settings.py`: Central configuration management
- `tests/`: Comprehensive test suite

## Database

FileFairy uses SQLite for local data persistence:

- `data/duplicates.db`: MD5 hashes and file records for duplicate detection
- `data/ai_cache.db`: Cached AI categorization results to minimize API calls
- `data/stats.db`: File organization statistics and activity logs
- `data/undo.db`: Operation history for undo functionality

## Logs

Application logs are written to `logs/organizer.log` containing:
- File operations with timestamps
- Errors and exceptions
- Categorization decisions
- Duplicate detection results
- Performance metrics

## Advanced Configuration

Edit `config/settings.py` to customize:

```python
# Watch folder location
WATCH_FOLDER = Path.home() / "Downloads"

# Output organization folder
OUTPUT_FOLDER = WATCH_FOLDER / "Organized"

# AI categorization (requires GEMINI_API_KEY in .env)
AI_ENABLED = True

# Enable academic-specific organization
ACADEMIC_MODE = True

# Minimum file size threshold (bytes)
MIN_FILE_SIZE = 10000

# File monitoring polling interval (seconds)
POLLING_INTERVAL = 5
```

To disable AI categorization and use only rule-based sorting, set `AI_ENABLED = False` in `config/settings.py`.

## Performance Considerations

- The organizer uses minimal CPU resources with lazy processing
- File size has negligible impact on performance
- Database operations are optimized with indexed queries
- Memory footprint remains under 50 MB for typical usage
- Scales efficiently with thousands of files

## Contributing

Contributions are welcome. Please ensure:
- All tests pass before submission
- Code follows existing style conventions
- New features include corresponding test cases
- Documentation is updated to reflect changes

## License

This project is provided as-is for personal and commercial use.

## Support

For issues, questions, or feature requests, please refer to the troubleshooting section above or review `logs/organizer.log` for detailed diagnostic information.

## Version History

**Current Version**: 1.0.0
- Watchdog threading compatibility fixed for Python 3.13
- File organization output moved to Downloads/Organized/ structure
- Real-time monitoring and statistics tracking
- Duplicate detection with MD5 hashing
- Academic mode for specialized file organization
- Complete undo capability for file operations
