import unittest
from unittest.mock import patch, mock_open
import os
import shutil
import tempfile
from pathlib import Path
from obsidian_to_jekyll import *

class TestObsidianToJekyll(unittest.TestCase):
    def setUp(self):
        
        # Create temporary directories for testing
        self.test_dir = Path(tempfile.mkdtemp())
        
        self.obsidian_publish_dir = self.test_dir / "Publish"
        self.obsidian_img_dir = self.test_dir / "Assets" / "Images"
        self.jekyll_dir = self.test_dir / "schrodlm.github.io"
        self.jekyll_img_dir = self.jekyll_dir / "assets" / "img"

        self.obsidian_publish_dir.mkdir(parents=True, exist_ok=True)
        self.obsidian_img_dir.mkdir(parents=True, exist_ok=True)
        self.jekyll_dir.mkdir(parents=True, exist_ok=True)
        self.jekyll_img_dir.mkdir(parents=True, exist_ok=True)

        # Create jekyll subdirectory
        self.jekyll_subdir1 = self.jekyll_dir / "_posts"
        self.jekyll_subdir2 = self.jekyll_dir / "_projects"
        self.jekyll_subdir1.mkdir(parents=True, exist_ok=True)
        self.jekyll_subdir2.mkdir(parents=True, exist_ok=True)

        # Create publish subdirectories
        self.obsidian_subdir1 = self.obsidian_publish_dir / "Posts"
        self.obsidian_subdir2 = self.obsidian_publish_dir / "Projects"
        self.obsidian_subdir1.mkdir(parents=True, exist_ok=True)
        self.obsidian_subdir2.mkdir(parents=True, exist_ok=True)                    

        # Create a test image
        self.fake_image = self.obsidian_img_dir / "test-image.png"
        self.fake_image.write_text("""fake image data""")

        # Create test files with Obsidian links
        # File 1: References file 2 and has an image
        self.file1 = self.obsidian_subdir1 / "file1.md"
        self.file1.write_text("""# File 1
            
This file references [[file2| reference]], [[file2 | reference]], [[file2 |reference]] and has an image:

![test-image.png](test-image.png)

Also references [[file2#chapter]].
""")
        
        # File 2: In a different subdirectory, references file 1
        self.file2 = self.obsidian_subdir2 / "file2.md"
        self.file2.write_text("""# File 2
        This is file 2.
""")
          
    def tearDown(self):
        # Clean up temporary directories
        #shutil.rmtree(self.test_dir)
        pass
    
    # Test get_directory_files
    @patch('os.listdir')
    @patch('os.path.isdir')
    @patch('os.path.isfile')
    def test_get_directory_files(self, mock_isfile, mock_isdir, mock_listdir):
        mock_listdir.return_value = ['valid.md', 'invalid.txt', 'subdir']
        mock_isdir.side_effect = lambda x: x.endswith('subdir')
        mock_isfile.side_effect = lambda x: not x.endswith('subdir')
        
        directory_files = get_directory_files('/test/dir')
        directory_files == ['valid.md']
    
    def test_get_jekyll_directory(self):
        with self.subTest("Valid directory test"):
            got = self.obsidian_subdir1
            want = self.jekyll_subdir1
            self.assertEqual(want,get_jekyll_directory(got, self.jekyll_dir, self.obsidian_publish_dir))

        with self.subTest("Not created in Jekyll dir structure"):
            got = self.obsidian_publish_dir / "DoesNotExistsInJekyll"
            with self.assertRaises(RuntimeError):
                get_jekyll_directory(got, self.jekyll_dir, self.obsidian_publish_dir)
        
        with self.subTest("Invalid parent"):
            got = self.obsidian_img_dir / "Posts"
            with self.assertRaises(RuntimeError):
                get_jekyll_directory(got, self.jekyll_dir, self.obsidian_publish_dir)

if __name__ == "__main__":
    unittest.main()