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
        self.test_dir = tempfile.mkdtemp()
        self.obsidian_publish_dir = os.path.join(self.test_dir, "Publish")
        self.obsidian_img_dir = os.path.join(self.test_dir, "Assets", "Images")
        self.jekyll_dir = os.path.join(self.test_dir, "schrodlm.github.io")
        self.jekyll_img_dir = os.path.join(self.jekyll_dir, "assets", "img")

        os.makedirs(self.obsidian_publish_dir)
        os.makedirs(self.jekyll_dir)
        os.makedirs(self.jekyll_img_dir)

        # Create test subdirectories
        self.subdir1 = os.path.join(self.obsidian_publish_dir, "subdir1")
        self.subdir2 = os.path.join(self.obsidian_publish_dir, "subdir2")
        os.makedirs(self.subdir1)
        os.makedirs(self.subdir2)

        # Create a test image
        with open(os.path.join(self.subdir1, "test-image.png"), "w") as f:
            f.write("fake image data")

        # Create test files with Obsidian links
        # File 1: References file 2 and has an image
        with open(os.path.join(self.subdir1, "file1.md"), "w") as f:
            f.write("""# File 1
            
This file references [[file2| reference]], [[file2 | reference]], [[file2 |reference]] and has an image:

![test-image.png](test-image.png)

Also references [[file2#chapter]].
""")
        
        # File 2: In a different subdirectory, references file 1
        with open(os.path.join(self.subdir2, "file2.md"), "w") as f:
            f.write("""# File 2
        This is file 2.
""")
          
    def tearDown(self):
        # Clean up temporary directories
        shutil.rmtree(self.test_dir)
    
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

if __name__ == "__main__":
    unittest.main()