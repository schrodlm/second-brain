#!/usr/bin/env python3

from pathlib import Path

JEKYLL_DIR = Path("../schrodlm.github.io/").resolve()
OBSIDIAN_DIR = Path("..").resolve()

PUBLISH_DIR = OBSIDIAN_DIR / "Publish"
OBSIDIAN_IMAGE_PATHS = OBSIDIAN_DIR / "Assets" / "Images"
JEKYLL_IMAGE_PATHS = JEKYLL_DIR / "assets" / "img"

#Check if directories exist:
assert JEKYLL_DIR.is_dir()
assert OBSIDIAN_DIR.is_dir()
assert PUBLISH_DIR.is_dir()
assert OBSIDIAN_IMAGE_PATHS.is_dir()
assert JEKYLL_IMAGE_PATHS.is_dir()

# Example: "$PUBLISH_DIR/Posts" -> "$JEKYLL_DIR/_posts"
def get_jekyll_directory(obsidian_directory, jekyll_dir=JEKYLL_DIR, publish_dir=PUBLISH_DIR):
    if obsidian_directory.parent != publish_dir:
        raise RuntimeError(f"Provided directory \"{obsidian_directory}\" is not part of publish directory")
    publish_dirname = obsidian_directory.name
    # All capital to lower-case + add "_" to the start
    jekyll_dir = Path(jekyll_dir / str("_" + publish_dirname.lower()))
    #3. Check if it exists in Jekyll dir structure
    if not jekyll_dir.is_dir():
        raise RuntimeError(f"Directory {jekyll_dir} does not exist in Jekyll directory.")
    return jekyll_dir

def get_publish_subdirectories(publish_dir=PUBLISH_DIR):
    subdirectories = []
    for file in publish_dir.iterdir():
        if not file.is_dir():
            raise RuntimeError(f"File {file.name} located in the publish directory")
        subdirectories.append(file)
    return subdirectories

def remove_contents_of(directory):
    pass

# Skips subdirectories and files that are not markdown
def get_directory_files(directory):
    pass

#Makes the URLS and names jekyll friendly
def slugify():
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
        publish_files = get_directory_files(publish_subdirectory)
        
        #3. create jekyll-friendly files from the obsidian files and move them to appropriate places
        for publish_file in publish_files:
            jekyll_file, new_referenced_images = transform_obsidian_to_jekyll(publish_file)
            referenced_images += new_referenced_images

            transfer_file(jekyll_file, jekyll_subdirectory)

        #4. copy referenced images into image section
        transfer_images(referenced_images)