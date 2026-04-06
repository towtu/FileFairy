import unittest
from pathlib import Path
from categorizer import categorize_file
from config.settings import OUTPUT_FOLDER


def normalize_path(p):
    """Normalize path separators for comparison."""
    return str(p).replace("\\", "/")


class TestCategorizer(unittest.TestCase):
    """Test file categorization logic."""

    def test_academic_lecture_slides(self):
        """Test academic lecture slides are categorized correctly."""
        path = Path("lecture_week3_slides.pdf")
        dest = categorize_file(path)
        self.assertIn("Academics/Lectures/Slides", normalize_path(dest))

    def test_academic_assignment(self):
        """Test academic assignments are categorized correctly."""
        path = Path("assignment_1_submission.docx")
        dest = categorize_file(path)
        self.assertIn("Academics/Assignments/Pending", normalize_path(dest))

    def test_academic_research_paper(self):
        """Test research papers are categorized correctly."""
        path = Path("research_paper_2024.pdf")
        dest = categorize_file(path)
        self.assertIn("Academics/Research/Papers", normalize_path(dest))

    def test_academic_textbook(self):
        """Test textbooks are categorized correctly."""
        path = Path("textbook_algorithms.pdf")
        dest = categorize_file(path)
        self.assertIn("Academics/Textbooks", normalize_path(dest))

    def test_academic_exam_past_paper(self):
        """Test past exam papers are categorized correctly."""
        path = Path("past_exam_2023.pdf")
        dest = categorize_file(path)
        self.assertIn("Academics/Exams/Past_Papers", normalize_path(dest))

    def test_academic_study_guide(self):
        """Test study guides are categorized correctly."""
        path = Path("study_guide_finals.pdf")
        dest = categorize_file(path)
        self.assertIn("Academics/Exams/Study_Guides", normalize_path(dest))

    def test_academic_notes(self):
        """Test notes are categorized correctly."""
        path = Path("course_notes_math.txt")
        dest = categorize_file(path)
        self.assertIn("Academics/Lectures/Notes", normalize_path(dest))

    def test_academic_certificate(self):
        """Test certificates are categorized correctly."""
        path = Path("certificate_python.pdf")
        dest = categorize_file(path)
        self.assertIn("Academics/Certificates", normalize_path(dest))

    def test_academic_thesis(self):
        """Test thesis documents are categorized correctly."""
        path = Path("thesis_draft_v2.docx")
        dest = categorize_file(path)
        self.assertIn("Academics/Research/My_Papers", normalize_path(dest))

    def test_code_python(self):
        """Test Python files are categorized correctly."""
        path = Path("my_test_script.py")
        dest = categorize_file(path)
        self.assertIn("Code/Python", normalize_path(dest))

    def test_code_javascript(self):
        """Test JavaScript files are categorized correctly."""
        path = Path("app.js")
        dest = categorize_file(path)
        self.assertIn("Code/JavaScript", normalize_path(dest))

    def test_code_html(self):
        """Test HTML files are categorized correctly."""
        path = Path("index.html")
        dest = categorize_file(path)
        self.assertIn("Code/Web/HTML", normalize_path(dest))

    def test_code_css(self):
        """Test CSS files are categorized correctly."""
        path = Path("styles.css")
        dest = categorize_file(path)
        self.assertIn("Code/Web/CSS", normalize_path(dest))

    def test_code_jupyter_notebook(self):
        """Test Jupyter notebooks are categorized correctly."""
        path = Path("analysis.ipynb")
        dest = categorize_file(path)
        self.assertIn("Code/Notebooks", normalize_path(dest))

    def test_document_pdf(self):
        """Test general PDFs are categorized correctly."""
        path = Path("report.pdf")
        dest = categorize_file(path)
        self.assertIn("Documents/PDFs", normalize_path(dest))

    def test_document_word(self):
        """Test Word documents are categorized correctly."""
        path = Path("letter.docx")
        dest = categorize_file(path)
        self.assertIn("Documents/Word_Docs", normalize_path(dest))

    def test_document_spreadsheet(self):
        """Test spreadsheets are categorized correctly."""
        path = Path("budget.xlsx")
        dest = categorize_file(path)
        self.assertIn("Documents/Spreadsheets", normalize_path(dest))

    def test_image_photo(self):
        """Test photos are categorized correctly."""
        path = Path("cat_photo.jpg")
        dest = categorize_file(path)
        self.assertIn("Images/Photos", normalize_path(dest))

    def test_image_screenshot(self):
        """Test screenshots are categorized correctly."""
        path = Path("screenshot_notes.png")
        dest = categorize_file(path)
        self.assertIn("Images/Screenshots", normalize_path(dest))

    def test_image_diagram(self):
        """Test diagrams are categorized correctly."""
        path = Path("diagram_flowchart.png")
        dest = categorize_file(path)
        self.assertIn("Images/Diagrams", normalize_path(dest))

    def test_image_wallpaper(self):
        """Test wallpapers are categorized correctly."""
        path = Path("wallpaper_nature.jpg")
        dest = categorize_file(path)
        self.assertIn("Images/Wallpapers", normalize_path(dest))

    def test_video_lecture(self):
        """Test lecture videos are categorized correctly."""
        path = Path("lecture_intro.mp4")
        dest = categorize_file(path)
        self.assertIn("Videos/Lectures", normalize_path(dest))

    def test_video_tutorial(self):
        """Test tutorial videos are categorized correctly."""
        path = Path("tutorial_howto.mp4")
        dest = categorize_file(path)
        self.assertIn("Videos/Tutorials", normalize_path(dest))

    def test_video_recording(self):
        """Test screen recordings are categorized correctly."""
        path = Path("recording_obs.mp4")
        dest = categorize_file(path)
        self.assertIn("Videos/Screen_Recordings", normalize_path(dest))

    def test_audio_podcast(self):
        """Test podcasts are categorized correctly."""
        path = Path("podcast_episode_1.mp3")
        dest = categorize_file(path)
        self.assertIn("Audio/Podcasts", normalize_path(dest))

    def test_audio_music(self):
        """Test music is categorized correctly."""
        path = Path("song_classic.mp3")
        dest = categorize_file(path)
        self.assertIn("Audio/Music", normalize_path(dest))

    def test_audio_voice_note(self):
        """Test voice notes are categorized correctly."""
        path = Path("voice_memo.wav")
        dest = categorize_file(path)
        self.assertIn("Audio/Voice_Notes", normalize_path(dest))

    def test_data_csv_raw(self):
        """Test raw CSV data is categorized correctly."""
        path = Path("dataset_raw.csv")
        dest = categorize_file(path)
        self.assertIn("Data/Datasets/Raw", normalize_path(dest))

    def test_data_json(self):
        """Test JSON data is categorized correctly."""
        path = Path("data.json")
        dest = categorize_file(path)
        self.assertIn("Data/JSON_XML", normalize_path(dest))

    def test_archive_zip(self):
        """Test ZIP archives are categorized correctly."""
        path = Path("project.zip")
        dest = categorize_file(path)
        self.assertIn("Archives/Compressed", normalize_path(dest))

    def test_app_windows_exe(self):
        """Test Windows executables are categorized correctly."""
        path = Path("installer.exe")
        dest = categorize_file(path)
        self.assertIn("Apps/Windows", normalize_path(dest))

    def test_design_figma(self):
        """Test Figma files are categorized correctly."""
        path = Path("mockup.fig")
        dest = categorize_file(path)
        self.assertIn("Design/Figma_Exports", normalize_path(dest))

    def test_unknown_file(self):
        """Test unknown file types are categorized as Unknown."""
        path = Path("weirdfile.xyz")
        dest = categorize_file(path)
        self.assertIn("_Unknown", normalize_path(dest))


class TestCategorizeSubject(unittest.TestCase):
    """Test subject detection for academic files."""

    def test_computer_science_subject(self):
        """Test CS subject detection."""
        path = Path("algorithm_sorting.pdf")
        dest = categorize_file(path)
        # Should detect Computer_Science in subject
        self.assertIn("Computer_Science", normalize_path(dest))

    def test_mathematics_subject(self):
        """Test Math subject detection."""
        path = Path("calculus_notes.pdf")
        dest = categorize_file(path)
        # Should detect Mathematics in subject
        self.assertIn("Mathematics", normalize_path(dest))

    def test_physics_subject(self):
        """Test Physics subject detection."""
        path = Path("physics_mechanics.pdf")
        dest = categorize_file(path)
        # Should detect Physics in subject
        self.assertIn("Physics", normalize_path(dest))

    def test_chemistry_subject(self):
        """Test Chemistry subject detection."""
        path = Path("chemistry_organic.pdf")
        dest = categorize_file(path)
        # Should detect Chemistry in subject
        self.assertIn("Chemistry", normalize_path(dest))


if __name__ == "__main__":
    unittest.main()

