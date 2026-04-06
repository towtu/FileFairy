import unittest
import tempfile
from pathlib import Path
import shutil
from config.settings import OUTPUT_FOLDER
from categorizer import categorize_file
from filename_cleaner import clean_filename
from conflict_resolver import resolve_conflict


def normalize_path(p):
    """Normalize path separators for comparison."""
    return str(p).replace("\\", "/")


class TestIntegrationWorkflow(unittest.TestCase):
    """Test complete file organization workflow."""

    def setUp(self):
        """Set up test directories."""
        self.temp_download_dir = tempfile.TemporaryDirectory()
        self.temp_output_dir = tempfile.TemporaryDirectory()
        self.download_dir = Path(self.temp_download_dir.name)
        self.output_dir = Path(self.temp_output_dir.name)

    def tearDown(self):
        """Clean up test directories."""
        self.temp_download_dir.cleanup()
        self.temp_output_dir.cleanup()

    def test_organize_single_file(self):
        """Test organizing a single file through the workflow."""
        # Create a test file
        test_file = self.download_dir / "lecture_slides.pdf"
        test_file.write_text("lecture content" * 1000)

        # Clean filename
        cleaned_name = clean_filename(test_file.name)
        cleaned_file = self.download_dir / cleaned_name

        # If name changed, simulate rename
        if cleaned_name != test_file.name:
            test_file = test_file.rename(cleaned_file)

        # Categorize
        dest_dir = categorize_file(test_file)

        # Resolve conflicts
        final_path = resolve_conflict(dest_dir, test_file.name)

        # Basic assertions
        norm_dest = normalize_path(dest_dir)
        self.assertIn("Academics", norm_dest)
        self.assertIn("Lectures", norm_dest)
        self.assertEqual(final_path.name, test_file.name)

    def test_organize_multiple_files(self):
        """Test organizing multiple files of different types."""
        files_to_test = [
            ("lecture_week1.pdf", "Academics/Lectures"),
            ("assignment_1.docx", "Academics/Assignments"),
            ("screenshot.png", "Images/Screenshots"),
            ("data.csv", "Data/Datasets"),
            ("script.py", "Code/Python"),
        ]

        for filename, expected_path in files_to_test:
            test_file = self.download_dir / filename
            test_file.write_text("x" * 11000)  # > 10KB

            dest_dir = categorize_file(test_file)
            norm_dest = normalize_path(dest_dir)
            self.assertIn(expected_path, norm_dest, 
                         f"File {filename} not categorized to {expected_path}")

    def test_duplicate_detection_workflow(self):
        """Test duplicate detection in workflow."""
        # Create two identical files
        file1 = self.download_dir / "file1.txt"
        file2 = self.download_dir / "file2.txt"

        identical_content = "identical content" * 1000
        file1.write_text(identical_content)
        file2.write_text(identical_content)

        # Both should have same content
        self.assertEqual(file1.read_text(), file2.read_text())

    def test_filename_cleaning_in_workflow(self):
        """Test filename cleaning is applied correctly."""
        # Create file with problematic name
        dirty_file = self.download_dir / "My File (2024) [v1].pdf"
        dirty_file.write_text("x" * 11000)

        # Clean it
        cleaned_name = clean_filename(dirty_file.name)

        # Check results
        self.assertTrue(cleaned_name.endswith(".pdf"))
        self.assertNotIn(" ", cleaned_name)
        self.assertNotIn("(", cleaned_name)
        self.assertNotIn(")", cleaned_name)
        self.assertNotIn("[", cleaned_name)
        self.assertNotIn("]", cleaned_name)

    def test_conflict_resolution_in_workflow(self):
        """Test conflict resolution when file already exists."""
        test_dir = Path(tempfile.mkdtemp())
        
        try:
            # Create existing file
            existing = test_dir / "file.txt"
            existing.write_text("existing")

            # Resolve conflict for same filename
            resolved = resolve_conflict(test_dir, "file.txt")

            # Should get numbered version
            self.assertEqual(resolved.name, "file_2.txt")
            self.assertEqual(resolved.parent, test_dir)
        finally:
            shutil.rmtree(test_dir)

    def test_academic_subject_detection(self):
        """Test academic subject detection in categorization."""
        test_cases = [
            ("algorithm_notes.pdf", "Computer_Science"),
            ("calculus_homework.pdf", "Mathematics"),
            ("physics_lab.pdf", "Physics"),
        ]

        for filename, expected_subject in test_cases:
            test_file = self.download_dir / filename
            test_file.write_text("x" * 11000)

            dest_dir = categorize_file(test_file)
            path_str = normalize_path(dest_dir)

            # Check if subject is in path
            if expected_subject in path_str:
                self.assertIn(expected_subject, path_str)

    def test_extension_based_categorization(self):
        """Test that extension-based categorization works."""
        extensions = [
            (".py", "Python"),
            (".js", "JavaScript"),
            (".html", "HTML"),
            (".csv", "Datasets"),
            (".json", "JSON_XML"),
            (".mp3", "Audio"),
            (".mp4", "Videos"),
        ]

        for ext, expected_category in extensions:
            test_file = self.download_dir / f"test{ext}"
            test_file.write_text("x" * 11000)

            dest_dir = categorize_file(test_file)
            path_str = normalize_path(dest_dir)
            self.assertIn(expected_category, path_str,
                         f"Extension {ext} not categorized to {expected_category}")

    def test_unknown_file_categorization(self):
        """Test that unknown files go to _Unknown folder."""
        test_file = self.download_dir / "weirdfile.xyz123"
        test_file.write_text("x" * 11000)

        dest_dir = categorize_file(test_file)
        self.assertIn("_Unknown", normalize_path(dest_dir))


if __name__ == "__main__":
    unittest.main()

