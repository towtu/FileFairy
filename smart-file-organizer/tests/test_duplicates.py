import unittest
import tempfile
from pathlib import Path
import sqlite3
from duplicate_detector import get_file_hash, is_duplicate, add_hash, remove_hash, init_db
from config.settings import HASHES_DB


class TestDuplicateDetector(unittest.TestCase):
    """Test duplicate detection functionality."""

    def setUp(self):
        """Set up test database and files."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file1 = Path(self.temp_dir.name) / "test1.txt"
        self.test_file2 = Path(self.temp_dir.name) / "test2.txt"
        self.test_file3 = Path(self.temp_dir.name) / "test3.txt"

        # Create test files with specific content
        self.test_file1.write_text("This is test content for file 1\n" + "x" * 10000)
        self.test_file2.write_text("This is test content for file 1\n" + "x" * 10000)  # Same as file1
        self.test_file3.write_text("This is different test content\n" + "y" * 10000)
        
        # Initialize and clean database for this test
        init_db()
        # Clear any existing hashes for our test files
        try:
            remove_hash(self.test_file1)
            remove_hash(self.test_file2)
            remove_hash(self.test_file3)
        except:
            pass  # If they don't exist, that's fine

    def tearDown(self):
        """Clean up test files."""
        self.temp_dir.cleanup()
        # Clean up test hashes from database
        try:
            remove_hash(self.test_file1)
            remove_hash(self.test_file2)
            remove_hash(self.test_file3)
        except:
            pass

    def test_get_file_hash(self):
        """Test that file hash is calculated correctly."""
        hash1 = get_file_hash(self.test_file1)
        hash2 = get_file_hash(self.test_file2)

        # Identical files should have same hash
        self.assertEqual(hash1, hash2)
        # Hash should be non-empty
        self.assertNotEqual(hash1, "")
        # Hash should be 32 chars (MD5)
        self.assertEqual(len(hash1), 32)

    def test_get_file_hash_different_files(self):
        """Test that different files have different hashes."""
        hash1 = get_file_hash(self.test_file1)
        hash3 = get_file_hash(self.test_file3)

        self.assertNotEqual(hash1, hash3)

    def test_get_file_hash_nonexistent_file(self):
        """Test handling of nonexistent files."""
        nonexistent = Path(self.temp_dir.name) / "nonexistent.txt"
        hash_val = get_file_hash(nonexistent)
        self.assertEqual(hash_val, "")

    def test_add_and_check_hash(self):
        """Test adding hash to database."""
        # Add hash to database
        add_hash(self.test_file1)

        # Same content file should be detected as duplicate
        self.assertTrue(is_duplicate(self.test_file2))

    def test_remove_hash(self):
        """Test removing hash from database."""
        # First add a hash
        add_hash(self.test_file1)
        # Verify it's there
        self.assertTrue(is_duplicate(self.test_file1))

        # Remove hash
        remove_hash(self.test_file1)

        # Verify removal worked by checking the database directly
        conn = sqlite3.connect(HASHES_DB)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM file_hashes WHERE filepath=?", (str(self.test_file1),))
        count = c.fetchone()[0]
        conn.close()
        self.assertEqual(count, 0, "Hash was not removed from database")

    def test_duplicate_detection_workflow(self):
        """Test complete workflow: add file, then detect duplicate."""
        # Add file 1 to database
        add_hash(self.test_file1)

        # File 2 has identical content, should now be detected as duplicate
        self.assertTrue(is_duplicate(self.test_file2))

        # File 3 has different content, should not be duplicate
        self.assertFalse(is_duplicate(self.test_file3))


if __name__ == "__main__":
    unittest.main()
