#!/usr/bin/env python3

from pathlib import Path
import os
from typing import Union, TypeVar, Type

JEKYLL_ROOT = Path("../schrodlm.github.io/").resolve()
OBSIDIAN_ROOT = Path("..").resolve()

PUBLISH_DIR = OBSIDIAN_ROOT / "Publish"
OBSIDIAN_IMAGE_PATHS = OBSIDIAN_ROOT / "Assets" / "Images"
JEKYLL_IMAGE_PATHS = JEKYLL_ROOT / "assets" / "img"

#Check if directories exist:
assert JEKYLL_ROOT.is_dir()
assert OBSIDIAN_ROOT.is_dir()
assert PUBLISH_DIR.is_dir()
assert OBSIDIAN_IMAGE_PATHS.is_dir()
assert JEKYLL_IMAGE_PATHS.is_dir()

T = TypeVar('T', bound='BaseValidatedPath')

class BaseValidatedPath:
    """Base class for validated path wrappers."""
    _root: Path  # Must be set in child classes or via configure_root()

    def __init__(self, path: Union[str, Path]):
        self._path = Path(path).expanduser().absolute()
        self._validate()

    def _validate(self):
        """Ensure path is within the configured root."""
        try:
            if not self._path.is_relative_to(self.__class__._root):
                raise ValueError(f"Path {self._path} is outside {self.__class__.__name__} root")
        except (FileNotFoundError, RuntimeError) as e:
            raise ValueError(f"Invalid path: {e}")
    
    # Overrding root - for testing purposes
    @classmethod
    def configure_root(cls: Type[T], root: Union[str, Path]) -> None:
        """Configure the root directory for validation."""
        cls._root = Path(root).resolve()

    @property
    def path(self) -> Path:
        """Access the raw Path object when needed."""
        return self._path

    # Delegate all other attributes to the wrapped Path
    def __getattr__(self, name):
        return getattr(self._path, name)

class ObsidianPath(BaseValidatedPath):
    """Path guaranteed to be within the Obsidian vault."""
    _root = OBSIDIAN_ROOT

class JekyllPath(BaseValidatedPath):
    """Path guaranteed to be within the Jekyll site."""
    _root = JEKYLL_ROOT

# Example: "$PUBLISH_DIR/Posts" -> "$JEKYLL_DIR/_posts"
def get_jekyll_directory(publish_subdir: ObsidianPath, jekyll_root: JekyllPath = JEKYLL_ROOT, publish_dir: ObsidianPath = PUBLISH_DIR) -> JekyllPath:
    if publish_subdir.parent != publish_dir:
        raise RuntimeError(f"Provided directory \"{publish_subdir}\" is not part of publish directory")
    # All capital to lower-case + add "_" to the start
    jekyll_root = Path(jekyll_root / str("_" + publish_subdir.name.lower()))
    #3. Check if it exists in Jekyll dir structure
    if not jekyll_root.is_dir():
        raise RuntimeError(f"Directory {jekyll_root} does not exist in Jekyll directory.")
    return jekyll_root

def get_publish_subdirectories(publish_dir: ObsidianPath = PUBLISH_DIR):
    subdirectories = []
    for file in publish_dir.iterdir():
        if not file.is_dir():
            raise RuntimeError(f"File {file.name} located in the publish directory")
        subdirectories.append(file)
    return subdirectories

# DANGEROUS method, use with care!
# Usable only in this directory
def remove_contents_of(directory: JekyllPath):
    if not directory.is_relative_to(JEKYLL_ROOT):
        raise RuntimeError("Trying to remove contents outside of this project! Aborted.")

    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            (Path(root) / name).unlink()
        for name in dirs:
            (Path(root) / name).rmdir()

"""
Retrieves the publish files that will be converted to jekyll-friendly files and published to the web
- currently it does assume that Publish directory will not contain any subdirectories, if such a feature is wanted, it needs to be implemented here first and foremost
"""
def get_directory_md_files(directory: Path) -> list[Path]:
    return list(directory.glob("*.md"))
            

"""
Transform obsidian markdown files names to name parsable by jekyll 

Obsidian Note Title: Hello World!.md -> hello_word.md

NOTICE:
For Jekyll native '_posts' layout it must follow a specific naming convention: YYYY-MM-DD-title.markdown,
so a simple parsing of markdown's metadata is necessary in order to handle this convention.
"""
def slugify(filename: ObsidianPath):

    pass 

def transform_obsidian_to_jekyll():
    slugify(name)
    transform_references()
    images = get_referenced_images()
    pass 

# Can be in forms:
    #1. [[Reference]]
    #2. [[SMT#bit-vectors]]
    #3. [[RealReference | Text]] | [[RealReference| Text]] | [[RealReference |Text]]
def transform_references():
    # Fixed obsidian URLS to jekyll-friendly ones
        #If URL points to file not in publish directory -> remove the link, but leave the text
        #If URL points to file in publish directory -> transform the link
    #Slugify them
    pass

# Image reference can be in form:
    #1. ![[image.png]] // has to be in Assets/Image
def get_referenced_images():
    # Gets the paths of referenced images
    pass

def transfer_file(file, directory):
    pass

def transfer_images(images):
    pass

def main():
    publish_subdirectories = get_publish_subdirectories()

    for publish_subdirectory in publish_subdirectories:
        jekyll_subdirectory = get_jekyll_directory(publish_subdirectory)
        #1. prepare set of referenced images
        referenced_images = {}

        #2. remove contents of that jekkyl subdirectory
        remove_contents_of(jekyll_subdirectory)
        publish_files = get_directory_md_files(publish_subdirectory)
        
        #3. create jekyll-friendly files from the obsidian files and move them to appropriate places
        for publish_file in publish_files:
            jekyll_file, new_referenced_images = transform_obsidian_to_jekyll(publish_file)
            referenced_images += new_referenced_images

            transfer_file(jekyll_file, jekyll_subdirectory)

        #4. copy referenced images into image section
        transfer_images(referenced_images)