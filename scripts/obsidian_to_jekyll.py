#!/usr/bin/env python3

PUBLISH_DIR = "../Publish"
JEKYLL_DIR = "../schrodlm.github.io"
OBSIDIAN_IMAGE_PATHS = "../Assets/Images"
JEKYLL_IMAGE_PATHS = f"$(JEKYLL_DIR)/assets/img"

def get_jekyll_directory(obsidian_directory):
    pass

def get_publish_subdirectories():
    pass

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