#!/usr/bin/env python3

import os
import unicodedata
import re

from typing import Union, TypeVar, Type, Optional
from pathlib import Path
from datetime import datetime

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

class PublishTransformError(Exception):
    """Exception raised when a file cannot be transformed for publishing."""
    
    def __init__(self, filepath: str, reason: str):
        """
        Args:
            file_path: Path to the file that failed transformation
            reason: Explanation of why the transformation failed
            original_exception: Optional original exception that caused the failure
        """
        self.filepath = filepath
        self.reason = reason
        message = f"Failed to transform '{filepath}': {reason}"
        super().__init__(message)

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
- currently it does assume that Publish subdirectories will not contain any nested subdirectories, if such a feature is wanted, it needs to be implemented here first and foremost
"""
def get_directory_md_files(directory: Path) -> list[Path]:
    return list(directory.glob("*.md"))



def read_md_metadata(markdown_path: Path):
    """Extract metadata from markdown file's front matter.

    Args:
        markdown_path: Path to a markdown file
    
    Returns:
        Dictionary containung the metadata key-value pairs.
        Returns empty dict if no metadata is found or file can't be read.
    """
    metadata = {}
    try:
        with markdown_path.open('r', encoding='utf-8') as file:
            lines = iter(file)

            #Find the opening "---"
            for line in lines:
                if line.strip() == "---":
                    break
            # No front matter found
            else:
                return metadata

            for line in lines:
                line = line.strip()
                if line == "---":
                    return metadata
                if not line or ':' not in line:
                    continue #Skip empty or invalid lines
                
                key,value = line.split(':', 1)
                metadata[key.strip()] = value.strip()
    except (IOError, UnicodeDecodeError):
        return {}
    return {}


def parse_date(date_str: str) -> Optional[datetime.date]:
    """
    Parse a date string in various formats into a datetime.date object.
    
    Supported formats:
    - YYYY-MM-DD (2024-12-20)
    - DD.MM.YYYY (20.12.2024)
    - DD/MM/YYYY (20/12/2024)
    - MM/DD/YYYY (12/20/2024)
    - Month DD, YYYY (December 20, 2024)
    - DD Month YYYY (20 December 2024)
    - YYYYMMDD (20241220)
    
    Returns:
        datetime.date object if parsing succeeds, None otherwise
    """
    if not date_str:
        return None
    date_str = date_str.strip()

    # Try common formats in order
    formats = [
        '%Y-%m-%d',    # 2024-12-20
        '%d.%m.%Y',    # 20.12.2024
        '%d/%m/%Y',    # 20/12/2024
        '%m/%d/%Y',    # 12/20/2024
        '%B %d, %Y',   # December 20, 2024
        '%d %B %Y',    # 20 December 2024
        '%Y%m%d',      # 20241220
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None

def slugify(filepath: ObsidianPath):
    """
    Transform a filename into a URL-safe slug following Jekyll conventions.
    
    Args:
        file_path: Path object or string filename to convert
        
    Returns:
        A sanitized filename with:
        - Only lowercase letters, numbers, and hyphens
        - No special characters or punctuation
        - Spaces converted to hyphens
        - Multiple hyphens collapsed
        - Leading/trailing hyphens removed
        
    Example:
        "Hello World!.md" -> "hello-world.md"
    NOTICE:
        For Jekyll native '_posts' layout it must follow a specific naming convention: YYYY-MM-DD-title.markdown,
        A simple parsing of markdown's metadata is necessary in order to handle this convention.
    """
    # Remove the file extension temporarily
    stem = Path(filepath).stem.strip()
    ext = Path(filepath).suffix.strip()
    
    # Normalize unicode characters (convert é to e, etc.)
    stem = unicodedata.normalize('NFKD', stem)
    
    # Convert to ASCII, ignoring non-ASCII chars
    stem = stem.encode('ascii', 'ignore').decode('ascii')
    
    # Replace various special characters with hyphens
    stem = re.sub(r'[^\w\s-]', '', stem)  # Remove remaining non-word chars
    stem = re.sub(r'[\s_-]+', '-', stem)  # Convert spaces/underscores to hyphens
    
    # Convert to lowercase and reattach extension
    slug = stem.lower() + ext.lower()

    # Special case for post layouts
    metadata = read_md_metadata(filepath)
    if metadata.get("layout") == "post":
        date_str = metadata.get("date")
        if not date_str:
            raise PublishTransformError(
                filepath=str(filepath),
                reason="Missing date field for post layout"
            )
        parsed_date = parse_date(date_str)
        if parsed_date is not None:
            date_prefix = f"{parsed_date.year:04d}-{parsed_date.month:02d}-{parsed_date.day:02d}"
            slug = f"{date_prefix}-{slug}"
        else:
            raise PublishTransformError(
                filepath=str(filepath),
                reason="Invalid date front matter provided for a post layout."
            )
            
    return slug

def transform_obsidian_to_jekyll(filepath: ObsidianPath):
    slugify(filepath)
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
        published = 0
        for publish_file in publish_files:
            try:
                jekyll_file, new_referenced_images = transform_obsidian_to_jekyll(ObsidianPath(publish_file))
                referenced_images += new_referenced_images
                transfer_file(jekyll_file, jekyll_subdirectory)

                print(f"Transfered {publish_file}. [{published}/{len(publish_files)}]")
            except PublishTransformError as e:
                print(f"Transfering failed for {e.filepath}")
                print(f"Reason: {e.reason}")

        #4. copy referenced images into image section
        transfer_images(referenced_images)