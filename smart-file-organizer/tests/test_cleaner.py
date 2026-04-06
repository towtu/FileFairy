import unittest
from filename_cleaner import clean_filename


class TestFilenameCleaner(unittest.TestCase):
    """Test filename sanitization."""

    def test_lowercase_conversion(self):
        """Test lowercase conversion is applied."""
        cleaned = clean_filename("MyFile.TXT")
        self.assertEqual(cleaned, "myfile.txt")

    def test_space_replacement(self):
        """Test spaces are replaced with underscores."""
        cleaned = clean_filename("my file name.pdf")
        self.assertEqual(cleaned, "my_file_name.pdf")

    def test_special_characters_removed(self):
        """Test special characters are removed."""
        cleaned = clean_filename("file@#$%name.doc")
        self.assertEqual(cleaned, "filename.doc")

    def test_multiple_underscores_consolidated(self):
        """Test multiple underscores are consolidated to single."""
        cleaned = clean_filename("my___file___name.txt")
        self.assertEqual(cleaned, "my_file_name.txt")

    def test_hyphens_preserved(self):
        """Test hyphens are preserved."""
        cleaned = clean_filename("my-file-name.pdf")
        self.assertEqual(cleaned, "my-file-name.pdf")

    def test_alphanumeric_preserved(self):
        """Test alphanumeric characters are preserved."""
        cleaned = clean_filename("file123name456.doc")
        self.assertEqual(cleaned, "file123name456.doc")

    def test_extension_preserved(self):
        """Test file extension is preserved."""
        cleaned = clean_filename("MY FILE.DOCX")
        self.assertTrue(cleaned.endswith(".docx"))
        self.assertIn("my", cleaned)

    def test_empty_name_fallback(self):
        """Test fallback to 'file' when name is empty."""
        cleaned = clean_filename("@#$%.pdf")
        self.assertEqual(cleaned, "file.pdf")

    def test_no_extension(self):
        """Test file with no extension."""
        cleaned = clean_filename("MyFileName")
        self.assertEqual(cleaned, "myfilename")

    def test_complex_filename(self):
        """Test complex filename with multiple issues."""
        cleaned = clean_filename("My File (2024) [v1].pdf")
        # Should remove special chars, convert to lowercase, replace spaces
        self.assertTrue(cleaned.endswith(".pdf"))
        self.assertNotIn(" ", cleaned)
        self.assertNotIn("(", cleaned)
        self.assertNotIn(")", cleaned)
        self.assertNotIn("[", cleaned)
        self.assertNotIn("]", cleaned)

    def test_multiple_dots(self):
        """Test filename with multiple dots."""
        cleaned = clean_filename("my.file.name.pdf")
        # Should treat last dot as extension separator
        self.assertTrue(cleaned.endswith(".pdf"))

    def test_leading_trailing_underscores(self):
        """Test leading/trailing underscores from special char removal."""
        cleaned = clean_filename("_file_name_.txt")
        # Underscores should be preserved if not from space replacement
        self.assertIn("file", cleaned)
        self.assertTrue(cleaned.endswith(".txt"))

    def test_unicode_characters(self):
        """Test unicode characters are removed."""
        cleaned = clean_filename("filé_名前.txt")
        # Non-ASCII should be removed
        self.assertTrue(cleaned.endswith(".txt"))
        # Should contain alphanumeric and underscores only
        for char in cleaned:
            if char != '.':
                self.assertTrue(char.isalnum() or char in '-_')


if __name__ == "__main__":
    unittest.main()
