import unittest
import tempfile
from pathlib import Path
from conflict_resolver import resolve_conflict


class TestConflictResolver(unittest.TestCase):
    """Test filename conflict resolution."""

    def setUp(self):
        """Set up test directory."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_dir = Path(self.temp_dir.name)

    def tearDown(self):
        """Clean up test directory."""
        self.temp_dir.cleanup()

    def test_no_conflict(self):
        """Test when file doesn't exist, returns same name."""
        target_filename = "newfile.txt"
        result = resolve_conflict(self.test_dir, target_filename)

        self.assertEqual(result.name, target_filename)
        self.assertEqual(result.parent, self.test_dir)

    def test_single_conflict(self):
        """Test single file conflict resolution."""
        # Create existing file
        existing = self.test_dir / "file.txt"
        existing.write_text("existing content")

        # Resolve conflict
        result = resolve_conflict(self.test_dir, "file.txt")

        # Should return file_2.txt
        self.assertEqual(result.name, "file_2.txt")
        self.assertEqual(result.parent, self.test_dir)

    def test_multiple_conflicts(self):
        """Test multiple file conflicts resolution."""
        # Create existing files
        (self.test_dir / "file.txt").write_text("1")
        (self.test_dir / "file_2.txt").write_text("2")
        (self.test_dir / "file_3.txt").write_text("3")

        # Resolve conflict
        result = resolve_conflict(self.test_dir, "file.txt")

        # Should return file_4.txt (next available)
        self.assertEqual(result.name, "file_4.txt")

    def test_conflict_with_different_extension(self):
        """Test file with same stem but different extension doesn't conflict."""
        # Create file with different extension
        (self.test_dir / "file.doc").write_text("different extension")

        # Resolve for .txt extension
        result = resolve_conflict(self.test_dir, "file.txt")

        # Should return file.txt (no conflict)
        self.assertEqual(result.name, "file.txt")

    def test_gap_in_numbering(self):
        """Test when there's a gap in numbering."""
        # Create files with gap
        (self.test_dir / "file.txt").write_text("1")
        (self.test_dir / "file_2.txt").write_text("2")
        # file_3.txt doesn't exist
        (self.test_dir / "file_4.txt").write_text("4")

        # Resolve conflict
        result = resolve_conflict(self.test_dir, "file.txt")

        # Should use next number (3), not fill the gap
        self.assertEqual(result.name, "file_3.txt")

    def test_complex_filename_conflict(self):
        """Test conflict with complex filename."""
        # Create existing file
        (self.test_dir / "document (1).pdf").write_text("content")

        # Resolve conflict
        result = resolve_conflict(self.test_dir, "document (1).pdf")

        # Should return document (1)_2.pdf
        self.assertEqual(result.name, "document (1)_2.pdf")

    def test_resolve_actual_path_creation(self):
        """Test that resolved path can actually be used to create file."""
        # Create existing file
        existing = self.test_dir / "file.txt"
        existing.write_text("existing")

        # Get conflict resolution
        new_path = resolve_conflict(self.test_dir, "file.txt")

        # Create new file at resolved path
        new_path.write_text("new content")

        # Both files should exist
        self.assertTrue(existing.exists())
        self.assertTrue(new_path.exists())
        self.assertNotEqual(existing, new_path)

    def test_many_conflicts(self):
        """Test with many conflicting files."""
        # Create 50 conflicting files
        for i in range(1, 51):
            if i == 1:
                (self.test_dir / "file.txt").write_text(f"content {i}")
            else:
                (self.test_dir / f"file_{i}.txt").write_text(f"content {i}")

        # Resolve conflict
        result = resolve_conflict(self.test_dir, "file.txt")

        # Should return file_51.txt
        self.assertEqual(result.name, "file_51.txt")

    def test_preserve_directory_path(self):
        """Test that returned path includes the target directory."""
        result = resolve_conflict(self.test_dir, "file.txt")

        # Returned path should be in the target directory
        self.assertEqual(result.parent, self.test_dir)
        self.assertTrue(str(self.test_dir) in str(result))


if __name__ == "__main__":
    unittest.main()
