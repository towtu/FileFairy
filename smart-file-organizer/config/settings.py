import os
from pathlib import Path

# Paths
WATCH_FOLDER = Path.home() / "Downloads"
OUTPUT_FOLDER = Path.home() / "Downloads" / "Organized"

# General Settings
DATE_SORTING = "year" # "year" or "month"
MIN_FILE_SIZE_KB = 10
ADD_DATE_PREFIX = False
LOWERCASE_FILENAMES = True
REPLACE_SPACES = True
RUN_ON_STARTUP = True
ACADEMIC_MODE = True
SUBJECT_DETECTION = True

# Internal DB Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"

HASHES_DB = DATA_DIR / "hashes.db"
HISTORY_DB = DATA_DIR / "history.db"
STATS_DB = DATA_DIR / "stats.db"
LOG_FILE = LOGS_DIR / "organizer.log"

# Create necessary internal directories
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)
