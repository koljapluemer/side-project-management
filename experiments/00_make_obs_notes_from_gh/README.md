# GitHub Repo to Obsidian Notes

This script automatically creates and updates Obsidian notes for your GitHub repositories, maintaining their archived status in the YAML frontmatter.

## Setup

1. Install required Python packages:
```bash
pip install pyyaml requests python-dotenv
```

2. Configure your GitHub credentials:
   - Copy `.env.example` to `.env`
   - Fill in your GitHub username and personal access token
   - To create a personal access token:
     1. Go to GitHub Settings -> Developer Settings -> Personal Access Tokens
     2. Generate a new token with 'repo' scope

3. (Optional) Modify the `OUTPUT_PATH` in the script to point to your Obsidian vault location

## Usage

Run the script:
```bash
python 00_make_obs_notes_from_gh.py
```

The script will:
- Fetch all your GitHub repositories
- Create/update markdown notes in your specified output directory
- Set the `is-archived` YAML property based on GitHub's repository status
- Preserve any existing note content and YAML frontmatter

## Features

- Automatically creates notes for new repositories
- Updates existing notes without losing content
- Preserves existing YAML frontmatter
- Handles edge cases (missing notes, invalid YAML, etc.)
