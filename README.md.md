## Publishing notes
This Obsidian vault automatically syncs published notes to a Jekyll repository (which will in turn generate a static site at: https://schrodlm.github.io/) using Git-hooks. When I commit changes to the `Publish/` directory on the master branch, the pre-commit hook will:

1. Convert Obsidian notes to Jekyll-compatible format
2. Update the Jekyll submodule with the converted content
3. Push changes to the Jekyll repository
4. Update the parent repository's submodule reference

### How to use it
1. Move notes you want to publish to the `Publish/` directory
2. Make your changes and stage them:
```
git add Publish/
```
3. Commit on the master branch:
 ```
git commit -m "Add new blog post about X"
```
4. The hook will automatically sync to Jekyll and push changes

### Prerequisites
- Python 3 with required dependencies

### Initial Setup
#### 1. Clone the Repository
```
git clone <your-obsidian-vault-repo>
cd <your-vault-name>
```
#### 2. Configure Git Hooks Path
This repository uses a shared `.githooks/` directory for Git hooks:

#### 3. Initialize Submodules
Initialize the Jekyll repository submodule:
```
git submodule update --init --recursive
```
### How It Works
The pre-commit hook automatically triggers when I commit changes to the master branch:
1. **Branch Check**: Only runs on the master branch
2. **Change Detection**: Monitors the Publish/ directory for changes
3. **Note Conversion**: Runs obsidian_to_jekyll.py to convert notes
4. **Submodule Update**: Commits and pushes changes to Jekyll repository
5. **Reference Update**: Updates parent repository's submodule pointer

### Working on Feature Branches
The hook only runs on master, so you can work freely on feature branches:
```
git checkout -b feature/new-post

# Make changes, commit normally
git commit -m "Draft: working on new post"
# Hook won't run - no Jekyll sync
```
When ready to publish:
```
git checkout master
git merge feature/new-post
# Hook runs and syncs to Jekyll
```
### New Device Setup
When setting up on a new device:
1. Clone the repository
```
git clone <your-repo>
cd <your-vault>
```
3. Configure hooks path:
 ```
git config core.hooksPath .githooks
``` 
3. Initialize submodules:
```
git submodule update --init --recursive
```
