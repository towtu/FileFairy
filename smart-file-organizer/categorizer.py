from pathlib import Path
from datetime import datetime
from config.settings import ACADEMIC_MODE, OUTPUT_FOLDER, DATE_SORTING
from config.categories import (
    EXTENSION_MAP, ACADEMIC_KEYWORDS, WORK_KEYWORDS, 
    IMAGE_KEYWORDS, VIDEO_KEYWORDS, AUDIO_KEYWORDS, DATA_KEYWORDS
)
from academic_sorter import detect_subject

def categorize_file(filepath: Path) -> Path:
    filename = filepath.name.lower()
    ext = filepath.suffix.lower()
    
    date_str = ""
    if DATE_SORTING == "year":
        date_str = str(datetime.now().year)
    elif DATE_SORTING == "month":
        date_str = datetime.now().strftime("%Y-%m")
    
    # 1. Academic Keywords
    if ACADEMIC_MODE:
        subfolder = check_keywords(filename, [ACADEMIC_KEYWORDS])
        if subfolder:
            subject = detect_subject(filename)
            if subject:
                parts = Path(subfolder).parts
                if len(parts) >= 2:
                    subfolder = str(Path(parts[0]) / parts[1] / subject / Path(*parts[2:]))
                else:
                    subfolder = str(Path(subfolder) / subject)
            
            if "Research/Papers" in subfolder:
                subfolder = str(Path(subfolder) / date_str)
                
            return OUTPUT_FOLDER / subfolder

    # 2. Other Keywords
    other_subfolder = check_keywords(filename, [
        WORK_KEYWORDS, IMAGE_KEYWORDS, VIDEO_KEYWORDS, 
        AUDIO_KEYWORDS, DATA_KEYWORDS
    ])
    
    if other_subfolder:
        return OUTPUT_FOLDER / other_subfolder
        
    # 3. Extension base logic
    if ext in EXTENSION_MAP:
        base_path = EXTENSION_MAP[ext]
        if "Documents/PDFs" in base_path:
            base_path = str(Path(base_path) / date_str)
        return OUTPUT_FOLDER / base_path
        
    # 4. Unknown
    return OUTPUT_FOLDER / "_Unknown"

def check_keywords(filename: str, keyword_dicts: list) -> str:
    for kw_dict in keyword_dicts:
        for kw, path in kw_dict.items():
            if kw in filename:
                return path
    return ""
