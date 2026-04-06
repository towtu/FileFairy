import json
import sqlite3
import time
from pathlib import Path
from config.settings import DATA_DIR

CACHE_DB = DATA_DIR / "ai_cache.db"

_model = None
_available = None
_cooldown_until = 0  # timestamp when rate limit cooldown ends


def _init_cache():
    conn = sqlite3.connect(str(CACHE_DB))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS ai_cache (
            filename TEXT PRIMARY KEY,
            category TEXT NOT NULL,
            confidence TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def _get_cached(filename: str) -> str:
    try:
        conn = sqlite3.connect(str(CACHE_DB))
        row = conn.execute(
            "SELECT category FROM ai_cache WHERE filename = ?", (filename,)
        ).fetchone()
        conn.close()
        return row[0] if row else ""
    except Exception:
        return ""


def _set_cache(filename: str, category: str, confidence: str):
    try:
        conn = sqlite3.connect(str(CACHE_DB))
        conn.execute(
            "INSERT OR REPLACE INTO ai_cache (filename, category, confidence) VALUES (?, ?, ?)",
            (filename, category, confidence),
        )
        conn.commit()
        conn.close()
    except Exception:
        pass


def _get_model():
    global _model, _available
    if _available is False:
        return None
    if _model is not None:
        return _model

    try:
        from config.settings import GEMINI_API_KEY

        if not GEMINI_API_KEY:
            _available = False
            print("[AI] No Gemini API key configured. Using rule-based categorization.")
            return None

        from google import genai

        client = genai.Client(api_key=GEMINI_API_KEY)
        _model = client
        _available = True
        print("[AI] Gemini AI categorizer initialized successfully.")
        return _model
    except ImportError:
        _available = False
        print("[AI] google-genai not installed. Using rule-based categorization.")
        return None
    except Exception as e:
        _available = False
        print(f"[AI] Failed to initialize Gemini: {e}. Using rule-based categorization.")
        return None


SYSTEM_PROMPT = """You are a file categorization engine. Given a filename and its extension, determine the best category folder path for organizing this file.

You must respond with ONLY valid JSON in this exact format:
{"category": "Category/Subcategory/", "confidence": "high"}

confidence must be one of: "high", "medium", "low"

Available top-level categories and their subcategories:
- Academics/Lectures/Slides/, Academics/Lectures/Notes/, Academics/Assignments/Pending/, Academics/Research/Papers/, Academics/Research/My_Papers/, Academics/Exams/Past_Papers/, Academics/Exams/Study_Guides/, Academics/Textbooks/, Academics/Certificates/
- Code/Python/, Code/Notebooks/, Code/JavaScript/, Code/Web/HTML/, Code/Web/CSS/, Code/Java/, Code/CPP/, Code/Shell_Scripts/, Code/Config_Files/
- Documents/PDFs/, Documents/Word_Docs/, Documents/Spreadsheets/, Documents/Presentations/, Documents/Text_Files/
- Images/Photos/, Images/Screenshots/, Images/Wallpapers/, Images/Icons_SVG/, Images/GIFs/, Images/Diagrams/
- Videos/Long_Videos/, Videos/Lectures/, Videos/Tutorials/, Videos/Screen_Recordings/, Videos/Short_Clips/
- Audio/Music/, Audio/Podcasts/, Audio/Voice_Notes/, Audio/Lectures/
- Data/Datasets/Raw/, Data/Datasets/Processed/, Data/JSON_XML/, Data/Databases/, Data/Spreadsheet_Data/
- Archives/Compressed/
- Apps/Windows/, Apps/Mac/, Apps/Linux/, Apps/Android/
- Design/Figma_Exports/, Design/Mockups/, Design/Logos/, Design/Fonts/
- Work/Invoices/, Work/Contracts/, Work/Reports/, Work/Meetings/
- Personal/

Rules:
1. Analyze the filename for contextual clues (keywords, abbreviations, patterns)
2. Consider the file extension for type information
3. If academic content is detected, prefer Academics/ categories
4. If the file cannot be confidently categorized, use the most reasonable match based on extension
5. Only use _Unknown/ if truly unrecognizable
6. Respond with ONLY the JSON object, no other text"""


def ai_categorize(filename: str, extension: str) -> str:
    """Use Gemini AI to categorize a file. Returns folder path or empty string on failure."""
    global _cooldown_until

    _init_cache()

    cached = _get_cached(filename)
    if cached:
        return cached

    # Skip API call if in cooldown period
    if time.time() < _cooldown_until:
        return ""

    client = _get_model()
    if client is None:
        return ""

    try:
        prompt = f"{SYSTEM_PROMPT}\n\nCategorize this file:\nFilename: {filename}\nExtension: {extension}"
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config={"temperature": 0.1, "max_output_tokens": 150},
        )

        text = response.text.strip()
        # Handle markdown code blocks in response
        if text.startswith("```"):
            text = text.split("\n", 1)[1] if "\n" in text else text[3:]
            text = text.rsplit("```", 1)[0].strip()

        result = json.loads(text)
        category = result.get("category", "")
        confidence = result.get("confidence", "low")

        if category and confidence in ("high", "medium"):
            _set_cache(filename, category, confidence)
            print(f"[AI] Categorized '{filename}' -> {category} (confidence: {confidence})")
            return category

        if category and confidence == "low":
            print(f"[AI] Low confidence for '{filename}', falling back to rules.")
            return ""

        return ""

    except json.JSONDecodeError:
        print(f"[AI] Invalid response for '{filename}', falling back to rules.")
        return ""
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower():
            _cooldown_until = time.time() + 60
            print(f"[AI] Rate limited. Cooling down for 60s, using rules in the meantime.")
        else:
            print(f"[AI] Error categorizing '{filename}': {e}. Falling back to rules.")
        return ""


def is_ai_available() -> bool:
    """Check if AI categorization is available."""
    return _get_model() is not None
