import unittest
from unittest.mock import patch, mock_open, Mock
import os
import shutil
import tempfile
from pathlib import Path
from obsidian_to_jekyll import *

class TestObsidianToJekyll(unittest.TestCase):
    def setUp(self):
        
        # Create temporary directories for testing
        self.obsidian_root = Path(tempfile.mkdtemp())
        
        self.obsidian_publish_dir = self.obsidian_root / "Publish"
        self.obsidian_img_dir = self.obsidian_root / "Assets" / "Images"
        self.jekyll_root = self.obsidian_root / "schrodlm.github.io"
        self.jekyll_img_dir = self.jekyll_root / "assets" / "img"

        ObsidianPath.configure_root(self.obsidian_root)
        JekyllPath.configure_root(self.jekyll_root)

        self.obsidian_publish_dir.mkdir(parents=True, exist_ok=True)
        self.obsidian_img_dir.mkdir(parents=True, exist_ok=True)
        self.jekyll_root.mkdir(parents=True, exist_ok=True)
        self.jekyll_img_dir.mkdir(parents=True, exist_ok=True)

        # Create jekyll subdirectory
        self.jekyll_subdir1 = self.jekyll_root / "_posts"
        self.jekyll_subdir2 = self.jekyll_root / "_projects"
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
        shutil.rmtree(self.obsidian_root)
        pass

    def test_path_validation(self):
            """Test the ObsidianPath and JekyllPath validation."""
            # Configure the paths for testing
            with patch('obsidian_to_jekyll.OBSIDIAN_ROOT', self.obsidian_root), \
                patch('obsidian_to_jekyll.JEKYLL_ROOT', self.jekyll_root):
                
                # --- Valid Paths ---
                with self.subTest("Valid ObsidianPath"):
                    valid_obsidian = ObsidianPath(self.obsidian_subdir1 / "file1.md")
                    self.assertTrue(valid_obsidian.exists())
                    
                with self.subTest("Valid JekyllPath"):
                    valid_jekyll = JekyllPath(self.jekyll_subdir1 / "post.md")
                    self.assertTrue(valid_jekyll.parent.exists())
                
                # --- Invalid Paths ---
                with self.subTest("Invalid ObsidianPath"):
                    with self.assertRaises(ValueError):
                        ObsidianPath(Path(tempfile.mkdtemp()))
                        
                with self.subTest("Invalid JekyllPath"):
                    with self.assertRaises(ValueError):
                        JekyllPath(self.obsidian_publish_dir / "outside_jekyll.md")

    def test_get_jekyll_directory(self):
        with self.subTest("Valid directory test"):
            got = self.obsidian_subdir1
            want = self.jekyll_subdir1
            self.assertEqual(want,get_jekyll_directory(got, self.jekyll_root, self.obsidian_publish_dir))

        with self.subTest("Not created in Jekyll dir structure"):
            got = self.obsidian_publish_dir / "DoesNotExistsInJekyll"
            with self.assertRaises(RuntimeError):
                get_jekyll_directory(got, self.jekyll_root, self.obsidian_publish_dir)
        
        with self.subTest("Invalid parent"):
            got = self.obsidian_img_dir / "Posts"
            with self.assertRaises(RuntimeError):
                get_jekyll_directory(got, self.jekyll_root, self.obsidian_publish_dir)

    def test_get_publish_subdirectories(self):
        with patch.object(Path, 'iterdir', return_value=[Path("subdir1"), Path("subdir2"), Path("subdir3")]):
            with self.subTest("Valid subdirectories"), patch.object(Path, 'is_dir', return_value=True):
                    subdirectories = get_publish_subdirectories(self.obsidian_publish_dir)
                    self.assertEqual(subdirectories, [Path('subdir1'), Path('subdir2'), Path('subdir3')], "Listed publish subdirectories are not correct.")
            
            with self.subTest("Publish dir contains files"), self.assertRaises(RuntimeError):
                get_publish_subdirectories(self.obsidian_publish_dir)
        
        with self.subTest("Unmocked"):
            subdirectories = get_publish_subdirectories(self.obsidian_publish_dir)
            self.assertEqual(subdirectories, [self.obsidian_subdir1, self.obsidian_subdir2], "Listed publish subdirectories are not correct.")
    
    def test_remove_contents_of(self):
        # This function has a safety check that depends on a global constant,
        # OBSIDIAN_DIR. We use `patch` to temporarily set this constant
        # to our main test directory for the duration of this test.
        with patch('obsidian_to_jekyll.JEKYLL_ROOT', self.obsidian_root):
            
            # --- Sub-test 1: Successful removal of contents ---
            with self.subTest("Successful removal of contents"):
                # Arrange: Create a directory structure to be deleted
                target_dir = Path(self.jekyll_subdir1 / "test_removal_directory")
                target_dir.mkdir()
                test_file = target_dir / "file_to_delete.md"
                test_file.write_text("some content")
                nested_dir = target_dir / "nested_dir"
                nested_dir.mkdir()
                nested_file = nested_dir / "nested_file.txt"
                nested_file.write_text("more content")

                # Act: Call the function to clear the directory
                remove_contents_of(target_dir)

                # Assert: The directory should still exist, but be empty
                self.assertTrue(target_dir.exists())
                self.assertEqual(list(target_dir.iterdir()), [], "Directory should be empty after removal")
                #Clean up
                shutil.rmtree(target_dir)

            
            # --- Sub-test 2: Safety check to prevent dangerous deletion ---
            with self.subTest("Safety check raises error for outside directory"):
                # Arrange: Create a separate temp directory outside the "safe" zone
                outside_dir = Path(tempfile.mkdtemp())
                # Add a file to it to ensure it's not empty
                (outside_dir / "do_not_delete.txt").touch()

                # Act & Assert: Expect a RuntimeError when trying to delete outside the safe zone
                with self.assertRaisesRegex(RuntimeError, "Trying to remove contents outside of this project! Aborted."):
                    remove_contents_of(outside_dir)

                # Assert that the outside directory and its contents were NOT deleted
                self.assertTrue((outside_dir / "do_not_delete.txt").exists())

                # Clean up
                shutil.rmtree(outside_dir)


    def test_get_directory_md_files(self):
        # Test 1: Basic functionality - finds markdown files in root directory
        with self.subTest("Finds markdown files in root directory"):
            # Arrange
            md_file1 = self.obsidian_publish_dir / "note1.md"
            md_file2 = self.obsidian_publish_dir / "note2.md"
            txt_file = self.obsidian_publish_dir / "text.txt"
            md_file1.touch()
            md_file2.touch()
            txt_file.touch()
            
            # Act
            result = get_directory_md_files(self.obsidian_publish_dir)
            
            # Assert
            self.assertEqual(len(result), 2)
            self.assertIn(md_file1, result)
            self.assertIn(md_file2, result)
            self.assertNotIn(txt_file, result)
            
            # Cleanup
            md_file1.unlink()
            md_file2.unlink()
            txt_file.unlink()

        # Test 2: Empty directory returns empty list
        with self.subTest("Empty directory returns empty list"):
            # Arrange
            empty_dir = self.obsidian_publish_dir / "empty_dir"
            empty_dir.mkdir()
            
            # Act
            result = get_directory_md_files(empty_dir)
            
            # Assert
            self.assertEqual(result, [])
            
            # Cleanup
            empty_dir.rmdir()

        # Test 3: No markdown files returns empty list
        with self.subTest("No markdown files returns empty list"):
            # Arrange
            no_md_dir = self.obsidian_publish_dir / "no_md_dir"
            no_md_dir.mkdir()
            txt_file = no_md_dir / "file.txt"
            csv_file = no_md_dir / "data.csv"
            txt_file.touch()
            csv_file.touch()
            
            # Act
            result = get_directory_md_files(no_md_dir)
            
            # Assert
            self.assertEqual(result, [])
            
            # Cleanup
            txt_file.unlink()
            csv_file.unlink()
            no_md_dir.rmdir()

        # Test 4: Should not follow symlinks
        with self.subTest("Should not follow symlinks"):
            # Arrange
            real_md = self.obsidian_publish_dir / "real.md"
            symlink_md = self.obsidian_publish_dir / "symlink.md"
            real_md.touch()
            symlink_md.symlink_to(real_md)
            
            # Act
            result = get_directory_md_files(self.obsidian_publish_dir)
            
            # Assert
            self.assertEqual(len(result), 2)  # Both the real file and symlink should be found
            self.assertIn(real_md, result)
            self.assertIn(symlink_md, result)
            
            # Cleanup
            real_md.unlink()
            symlink_md.unlink()


if __name__ == "__main__":
    unittest.main()