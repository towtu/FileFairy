from config.categories import SUBJECT_KEYWORDS

def detect_subject(filename: str) -> str:
    filename_lower = filename.lower()
    for subject, keywords in SUBJECT_KEYWORDS.items():
        for kw in keywords:
            if kw in filename_lower:
                return subject
    return ""
