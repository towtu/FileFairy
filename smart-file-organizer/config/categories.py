# smart-file-organizer/config/categories.py

EXTENSION_MAP = {
    # Academics (base extensions, keywords take precedence)
    
    # Code
    ".py": "Code/Python/",
    ".ipynb": "Code/Notebooks/",
    ".js": "Code/JavaScript/",
    ".ts": "Code/JavaScript/",
    ".jsx": "Code/JavaScript/",
    ".tsx": "Code/JavaScript/",
    ".html": "Code/Web/HTML/",
    ".htm": "Code/Web/HTML/",
    ".css": "Code/Web/CSS/",
    ".scss": "Code/Web/CSS/",
    ".java": "Code/Java/",
    ".cpp": "Code/CPP/",
    ".c": "Code/CPP/",
    ".h": "Code/CPP/",
    ".sh": "Code/Shell_Scripts/",
    ".bash": "Code/Shell_Scripts/",
    ".yaml": "Code/Config_Files/",
    ".yml": "Code/Config_Files/",
    ".toml": "Code/Config_Files/",
    ".ini": "Code/Config_Files/",
    ".env": "Code/Config_Files/",
    
    # Documents
    ".pdf": "Documents/PDFs/", # Base if not academic
    ".doc": "Documents/Word_Docs/",
    ".docx": "Documents/Word_Docs/",
    ".xls": "Documents/Spreadsheets/",
    ".xlsx": "Documents/Spreadsheets/",
    ".ppt": "Documents/Presentations/",
    ".pptx": "Documents/Presentations/",
    ".txt": "Documents/Text_Files/",
    ".md": "Documents/Text_Files/",
    ".rtf": "Documents/Text_Files/",
    ".odt": "Documents/Word_Docs/",
    
    # Images
    ".png": "Images/Photos/", # Base
    ".jpg": "Images/Photos/",
    ".jpeg": "Images/Photos/",
    ".svg": "Images/Icons_SVG/",
    ".ico": "Images/Icons_SVG/",
    ".gif": "Images/GIFs/",
    ".webp": "Images/Photos/",
    ".raw": "Images/Photos/",
    ".tiff": "Images/Photos/",
    
    # Videos
    ".mp4": "Videos/Long_Videos/",
    ".mkv": "Videos/Long_Videos/",
    ".mov": "Videos/Long_Videos/",
    ".avi": "Videos/Short_Clips/",
    ".flv": "Videos/Long_Videos/",
    ".wmv": "Videos/Long_Videos/",
    
    # Audio
    ".mp3": "Audio/Music/",
    ".flac": "Audio/Music/",
    ".m4a": "Audio/Music/",
    ".wav": "Audio/Voice_Notes/",
    ".ogg": "Audio/Music/",
    ".aac": "Audio/Music/",
    ".wma": "Audio/Music/",
    
    # Data
    ".csv": "Data/Datasets/Raw/",
    ".json": "Data/JSON_XML/",
    ".xml": "Data/JSON_XML/",
    ".db": "Data/Databases/",
    ".sqlite": "Data/Databases/",
    ".sql": "Data/Databases/",
    ".tsv": "Data/Spreadsheet_Data/",
    
    # Archives
    ".zip": "Archives/Compressed/",
    ".rar": "Archives/Compressed/",
    ".tar": "Archives/Compressed/",
    ".gz": "Archives/Compressed/",
    ".7z": "Archives/Compressed/",
    ".bz2": "Archives/Compressed/",
    ".exe": "Apps/Windows/",
    ".msi": "Apps/Windows/",
    ".dmg": "Apps/Mac/",
    ".pkg": "Apps/Mac/",
    ".deb": "Apps/Linux/",
    ".rpm": "Apps/Linux/",
    ".apk": "Apps/Android/",
    
    # Design
    ".fig": "Design/Figma_Exports/",
    ".xd": "Design/Mockups/",
    ".psd": "Design/Mockups/",
    ".ai": "Design/Logos/",
    ".ttf": "Design/Fonts/",
    ".otf": "Design/Fonts/",
    ".sketch": "Design/Mockups/",
}

ACADEMIC_KEYWORDS = {
    "lecture": "Academics/Lectures/Slides/",
    "slides": "Academics/Lectures/Slides/",
    "assignment": "Academics/Assignments/Pending/",
    "research": "Academics/Research/Papers/",
    "paper": "Academics/Research/Papers/",
    "exam": "Academics/Exams/Past_Papers/",
    "past": "Academics/Exams/Past_Papers/",
    "study": "Academics/Exams/Study_Guides/",
    "guide": "Academics/Exams/Study_Guides/",
    "textbook": "Academics/Textbooks/",
    "certificate": "Academics/Certificates/",
    "thesis": "Academics/Research/My_Papers/",
    "lab": "Academics/Assignments/Pending/",
    "report": "Academics/Assignments/Pending/",
    "notes": "Academics/Lectures/Notes/"
}

SUBJECT_KEYWORDS = {
    "Computer_Science": ["algorithm", "programming", "software", "database", "network", "ai", "ml"],
    "Mathematics": ["calculus", "algebra", "statistics", "math", "equation"],
    "Physics": ["physics", "mechanics", "quantum", "thermodynamics"],
    "Chemistry": ["chemistry", "organic", "molecular", "reaction"]
}

WORK_KEYWORDS = {
    "invoice": "Work/Invoices/",
    "receipt": "Work/Invoices/",
    "contract": "Work/Contracts/",
    "agreement": "Work/Contracts/",
    "report": "Work/Reports/",
    "agenda": "Work/Meetings/",
    "minutes": "Work/Meetings/",
    "resume": "Personal/",
    "cv": "Personal/"
}

IMAGE_KEYWORDS = {
    "screenshot": "Images/Screenshots/",
    "snip": "Images/Screenshots/",
    "capture": "Images/Screenshots/",
    "wallpaper": "Images/Wallpapers/",
    "background": "Images/Wallpapers/",
    "logo": "Images/Icons_SVG/",
    "icon": "Images/Icons_SVG/",
    "favicon": "Images/Icons_SVG/",
    "diagram": "Images/Diagrams/",
    "flowchart": "Images/Diagrams/",
    "uml": "Images/Diagrams/",
    "wireframe": "Images/Diagrams/"
}

VIDEO_KEYWORDS = {
    "lecture": "Videos/Lectures/",
    "class": "Videos/Lectures/",
    "lesson": "Videos/Lectures/",
    "tutorial": "Videos/Tutorials/",
    "howto": "Videos/Tutorials/",
    "guide": "Videos/Tutorials/",
    "recording": "Videos/Screen_Recordings/",
    "obs": "Videos/Screen_Recordings/",
    "loom": "Videos/Screen_Recordings/",
    "clip": "Videos/Short_Clips/",
    "short": "Videos/Short_Clips/",
    "reel": "Videos/Short_Clips/"
}

AUDIO_KEYWORDS = {
    "podcast": "Audio/Podcasts/",
    "episode": "Audio/Podcasts/",
    "voice": "Audio/Voice_Notes/",
    "memo": "Audio/Voice_Notes/",
    "note": "Audio/Voice_Notes/",
    "lecture": "Audio/Lectures/",
    "class": "Audio/Lectures/",
    "song": "Audio/Music/",
    "music": "Audio/Music/",
    "album": "Audio/Music/"
}

DATA_KEYWORDS = {
    "dataset": "Data/Datasets/Raw/",
    "data": "Data/Datasets/Raw/",
    "raw": "Data/Datasets/Raw/",
    "processed": "Data/Datasets/Processed/",
    "cleaned": "Data/Datasets/Processed/"
}
