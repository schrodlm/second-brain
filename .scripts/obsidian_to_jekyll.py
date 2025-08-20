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
OBSIDIAN_IMAGE_DIR = OBSIDIAN_ROOT / "Assets" / "Images"
JEKYLL_IMAGE_DIR = JEKYLL_ROOT / "assets" / "img"

#Check if directories exist:
assert JEKYLL_ROOT.is_dir()
assert OBSIDIAN_ROOT.is_dir()
assert PUBLISH_DIR.is_dir()
assert OBSIDIAN_IMAGE_DIR.is_dir()
assert JEKYLL_IMAGE_DIR.is_dir()
assert JEKYLL_IMAGE_DIR.is_relative_to(JEKYLL_ROOT)
assert OBSIDIAN_IMAGE_DIR.is_relative_to(OBSIDIAN_ROOT)


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


def transform_md_match(match: re.Match, src_dir: ObsidianPath = OBSIDIAN_IMAGE_DIR, dest_dir: JekyllPath = JEKYLL_IMAGE_DIR):
    """
    Transforms standard Markdown links and images - ![]() or []() - into Jekyll-compatible format.

    Handles the following cases:
    - Image references (![alt](path)): 
        * Copies images to destination directory
        * Updates paths to be relative to destination
        * Returns alt text if image unavailable
    - External links [](): Leaves unchanged
    - Document links [](): Leaves unchanged (per project requirements)

    Returns:
        Transformed markdown string or original string if no transformation needed

    Examples:
        # Local image transformation
        Input:  ![logo](images/logo.png)
        Output: ![logo]($(dst_dir)/images/logo.png)

        # External image (unchanged)
        Input:  ![logo](https://example.com/logo.png)
        Output: ![logo](https://example.com/logo.png)

        # Document link (unchanged per current requirements)
        Input:  [Readme](README.md)
        Output: [Readme](README.md)

        # Missing image returns alt text
        Input:  ![missing](nonexistent.png)
        Output: missing
    """
    is_image = match.group(1) == '!'
    alt_text = match.group(2)
    url = match.group(3)
    
    if is_image and not url.startswith(('http://', 'https://')):
        img_path = Path(url)
        src_path = src_dir / img_path
        dst_path = dest_dir / img_path
        
        if ensure_image_available(src_path, dst_path):
            rel_path = dst_path.relative_to(dest_dir)
            return f"![{alt_text}]({rel_path})"
        return alt_text
    return match.group(0)  # Leave external links and doc links unchanged

def transform_obsidian_match(match, src_dir: ObsidianPath = OBSIDIAN_IMAGE_DIR, dest_dir: JekyllPath = JEKYLL_IMAGE_DIR):
    """
    Transforms Obsidian-style links ([[ ]]) into Jekyll-compatible format.

    Args:
        match: re.Match object from Obsidian link pattern
        src_dir: Source directory for images (default: OBSIDIAN_IMAGE_DIR)
        dest_dir: Destination directory for images (default: JEKYLL_IMAGE_DIR)

    Returns:
        Transformed markdown string or display text

    Examples:
        # Obsidian image with dimensions
        Input:  ![[images/logo.png|200]]
        Output: ![Image](../assets/images/logo.png){:width="200"}

        # Obsidian document link with display text
        Input:  [[README.md|Readme File]]
        Output: Readme File

        # Obsidian image with alt text
        Input:  ![[logo.png|Company Logo]]
        Output: ![Company Logo](../assets/logo.png)
    """
    is_image = match.group(1) == '!'
    full_ref = match.group(2)
    if is_image:
        new_content, relative_src_path = transform_image_ref(full_ref, dest_dir, JEKYLL_ROOT)
        dst_path = dest_dir / relative_src_path
        src_path = src_dir / relative_src_path

        ensure_image_available(
            src_path,
            dst_path
        )
        return new_content
    else:
        return transform_md_ref(full_ref) #do nothing with non-image references
    
def transform_references(filepath: JekyllPath, src_dir: ObsidianPath = OBSIDIAN_IMAGE_DIR, dest_dir: JekyllPath = JEKYLL_IMAGE_DIR):
    """
    Transform Obsidian-style references to Jekyll-compatible format.
    Handles both document links and image references.

    Currently simply deletes document links. No complex linking for non-images is implemented as of now, 
    but may be implemented in the future.
    If this will ever be implemented: https://jekyllrb.com/docs/liquid/tags/#links this is the way to do it

    The only exceptions are images, which are transfered from their source to JEKYLL_IMAGE_DIR
        Image reference can be in form:
        1. ![Alt text](path/to/image.png)
        2. ![[image.png]]                           - has to be in image folder (specified in Obsidian config) 
        3. ![[path/to/image.png|200]]               - fixed width
        4. ![[path/to/image.png|200x100]]           - fixed width and height
        5. ![[path/to/image.png|My Alt Text]]       - alt text
        6. ![[path/to/image.png|My Alt Text|200]]   - alt text + resize
    """
    content = filepath.read_text(encoding='utf-8')

    # Patterns for different reference types
    obsidian_link_pattern = re.compile(r'(!?)\[\[([^\]\[]+)\]\]')  # ![[ ]] or [[ ]]
    md_link_pattern = re.compile(r'(!?)\[([^\]]+)\]\(([^)]+)\)')    # ![]() or []()
    # Transform all reference types
    content = md_link_pattern.sub(transform_md_match, content)
    content = obsidian_link_pattern.sub(transform_obsidian_match, content)

    filepath.write_text(content, encoding='utf-8')

def transform_md_ref(full_ref: str) -> str:
    """
    Currently simply deletes document links and extracts alt text from reference if it exists.
    """
    parts = [part.strip() for part in full_ref.split('|')]
    for part in parts[1:]:
        if not (part.isdigit()):
            return part
    return ""

def transform_image_ref(full_ref: str, new_parent_dir: JekyllPath = JEKYLL_IMAGE_DIR, root: JekyllPath = JEKYLL_ROOT) -> str:
    """
    Transform Obsidian-style image references to standard Markdown.
    Handles all these cases:
    1. ![[image.png]]                   → ![Image](image.png)
    2. ![[image.png|200]]               → ![Image](image.png){:width="200"}
    3. ![[image.png|200x100]]           → ![Image](image.png){:width="200" height="100"}
    4. ![[image.png|alt text]]          → ![alt text](image.png)
    5. ![[image.png|alt text|200]]      → ![alt text](image.png){:width="200"}
    6. ![[subdir/image.png]]            → ![Image](subdir/image.png)
    7. ![[image.png|alt text|200x100]]  → ![alt text](image.png){:width="200" height="100"}
    """
    # Split into components and strip whitespace
    parts = [part.strip() for part in full_ref.split('|')]
    relative_img_path = Path(parts[0])
    
    # Default values
    alt_text = "Image"
    width = None
    height = None
    
    # Process additional parameters
    for part in parts[1:]:
        if 'x' in part and all(s.isdigit() for s in part.split('x')):
            # Case 3 & 7: Dimensions (200x100)
            width, height = part.split('x')[:2]
        elif part.isdigit():
            # Case 2 & 5: Single dimension (200)
            width = part
        else:
            # Case 4 & 5 & 7: Alt text (non-numeric)
            alt_text = part
    
    # Build the image tag - 
    img_tag = f"![{alt_text}](/{(new_parent_dir/relative_img_path).relative_to(root)})"

    # Add dimensions if specified
    if width and height:
        img_tag = f'{img_tag}{{:width="{width}" height="{height}"}}'
    elif width:
        img_tag = f'{img_tag}{{:width="{width}"}}'
    
    return img_tag, relative_img_path
    

def copy_file(src: Path, dst: Path):
    dst.write_bytes(src.read_bytes())

def ensure_image_available(obsidian_img_path: Path, jekyll_img_path: Path) -> bool:
    """Copy image if needed, returns success status"""
    if not obsidian_img_path.exists():
        raise PublishTransformError(obsidian_img_path, "Obsidian image path does not exist.")
    if not jekyll_img_path.parent.exists():
        jekyll_img_path.parent.mkdir(parents=True)
    copy_file(obsidian_img_path, jekyll_img_path)
    return True

def transfer_publish_file(source_filepath: ObsidianPath, target_directory: JekyllPath):
    jekyll_filename = slugify(source_filepath)

    try:
        dst = target_directory / jekyll_filename
        copy_file(source_filepath, dst)

        transform_references(dst)
    except PublishTransformError as e:
        #Remove the already copied file from the Jekyll directory
        dst.unlink()
        raise e

def main():
    print("Starting the trasnfer process...")
    publish_subdirectories = get_publish_subdirectories()
    print(f"Found {len(publish_subdirectories)} publish subdirectories: {publish_subdirectories}")

    for publish_subdirectory in publish_subdirectories:
        jekyll_subdirectory = get_jekyll_directory(publish_subdirectory)

        #2. remove contents of that jekkyl subdirectory
        remove_contents_of(jekyll_subdirectory)
        publish_files = get_directory_md_files(publish_subdirectory)
        
        #3. create jekyll-friendly files from the obsidian files and move them to appropriate places
        published = 0
        for publish_file in publish_files:
            try:
                transfer_publish_file(publish_file, jekyll_subdirectory)

                published = published+1
                print(f"Transfered {publish_file}. [{published}/{len(publish_files)}]")
            except PublishTransformError as e:
                print(f"Transfering failed for {e.filepath}")
                print(f"Reason: {e.reason}")

if __name__ == "__main__":
    main()
